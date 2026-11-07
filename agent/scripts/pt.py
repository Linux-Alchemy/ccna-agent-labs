#!/usr/bin/env python3
"""Inspect Cisco Packet Tracer .pkt/.pka files.

  pt.py summary FILE            overview: devices, links, addressing, VLANs, routing, lint
  pt.py devices|links|addr|lint FILE
  pt.py device FILE NAME [--startup | --diff]   one device in detail (NAME or hostname)
  pt.py log FILE [-d DEV] [-g REGEX] [-n N]     CLI command history saved in the file
  pt.py xml FILE -o OUT.xml                     dump decrypted XML
  pt.py encode IN.xml OUT.pkt                   re-wrap (edited) XML as a .pkt/.pka
"""
import argparse
import difflib
import ipaddress
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pktcrypto  # noqa: E402

ABBR = [('TenGigabitEthernet', 'Te'), ('GigabitEthernet', 'Gi'), ('FastEthernet', 'Fa'),
        ('Ethernet', 'Eth'), ('Serial', 'Se'), ('Port-channel', 'Po'), ('Loopback', 'Lo')]


def short(ifname):
    for long_, s in ABBR:
        if ifname.startswith(long_):
            return s + ifname[len(long_):]
    return ifname


def canon(ifname):
    """Expand an abbreviated interface name (g0/1 -> GigabitEthernet0/1)."""
    m = re.match(r'([A-Za-z-]+)\s*([\d/.:]+)$', ifname.strip())
    if not m:
        return ifname
    head, num = m.group(1).lower(), m.group(2)
    for long_, s in ABBR + [('Vlan', 'vl')]:
        if long_.lower().startswith(head) or s.lower() == head:
            return long_ + num
    return ifname


# --- model ----------------------------------------------------------------

class Iface:
    def __init__(self, name):
        self.name = name
        self.desc = ''
        self.ips = []            # [IPv4Interface]
        self.dhcp = False
        self.shutdown = False
        self.mode = None         # 'access' | 'trunk' | None (dynamic/default)
        self.access_vlan = 1
        self.native_vlan = 1
        self.allowed = None
        self.nat = None
        self.helpers = []
        self.dot1q = None
        self.channel_group = None


class Device:
    def __init__(self, engine, ws):
        self.e = engine
        self.name = engine.findtext('NAME')
        t = engine.find('TYPE')
        self.kind = t.text
        self.model = t.get('model')
        self.power = engine.findtext('POWER') == 'true'
        self.ref = (engine.findtext('SAVE_REF_ID') or '').removeprefix('save-ref-id:')
        lg = ws.find('LOGICAL') if ws is not None else None
        self.xy = (lg.findtext('X'), lg.findtext('Y')) if lg is not None else None
        self.running = self._lines('RUNNINGCONFIG')
        self.startup = self._lines('STARTUPCONFIG')
        self.ios = bool(self.running)
        self.hostname = self.name  # IOS devices: replaced by config 'hostname'
        self.ifaces = {}
        self.cfg = {}
        self.vlans = {}
        self.host_ports = []
        if self.ios:
            parse_ios(self)
            v = engine.find('VLANS')
            if v is not None:
                self.vlans = {int(x.get('number')): x.get('name') for x in v}
        else:
            self._host()

    def _lines(self, tag):
        el = self.e.find(tag)
        return [l.text or '' for l in el] if el is not None else []

    def _host(self):
        self.gateway = self.e.findtext('GATEWAY') or ''
        self.dns = self.e.findtext('DNS_CLIENT/SERVER_IP') or ''
        for p in self.e.iter('PORT'):
            if p.find('MACADDRESS') is None:
                continue
            ip, mask = p.findtext('IP') or '', p.findtext('SUBNET') or ''
            dhcp = p.findtext('PORT_DHCP_ENABLE') == 'true'
            if not ip and not dhcp:
                continue
            itf = None
            if ip and mask:
                try:
                    itf = ipaddress.IPv4Interface(f'{ip}/{mask}')
                except ValueError:
                    pass
            self.host_ports.append({
                'type': (p.findtext('TYPE') or '').removeprefix('e'),
                'ip': itf, 'dhcp': dhcp, 'mac': p.findtext('MACADDRESS'),
                'gateway': p.findtext('PORT_GATEWAY') or self.gateway,
                'ipv6': p.findtext('IPV6_ENABLED') == 'true'})

    @property
    def label(self):
        return self.hostname if self.hostname == self.name else f'{self.hostname} ({self.name})'

    def ips(self):
        if self.ios:
            return [(i.name, ip) for i in self.ifaces.values() for ip in i.ips]
        return [(p['type'], p['ip']) for p in self.host_ports if p['ip']]


def parse_ios(dev):
    cfg = dev.cfg = {'routing': [], 'static': [], 'nat_pools': {}, 'nat_rules': [],
                     'dhcp_pools': {}, 'pw_encrypt': False, 'enable_password': False,
                     'enable_secret': False, 'line_pw': [], 'lines': {}, 'acls': set()}
    cur = None      # current block: ('if', Iface) | ('router', list) | ('dhcp', dict) | ('line', dict)
    for raw in dev.running:
        line = raw.rstrip()
        if not line.strip() or line.strip() == '!':
            cur = None if line.strip() == '!' else cur
            continue
        indented = line.startswith(' ')
        s = line.strip()
        if not indented:
            cur = None
            if s.startswith('hostname '):
                dev.hostname = s.split(None, 1)[1]
            elif s.startswith('interface '):
                i = Iface(s.split(None, 1)[1])
                dev.ifaces[i.name] = i
                cur = ('if', i)
            elif s.startswith('router '):
                block = [s]
                cfg['routing'].append(block)
                cur = ('router', block)
            elif s.startswith('ip route '):
                cfg['static'].append(s[len('ip route '):])
            elif s.startswith('ip nat pool '):
                cfg['nat_pools'][s.split()[3]] = s
            elif s.startswith('ip nat inside source'):
                cfg['nat_rules'].append(s)
            elif s.startswith('ip dhcp pool '):
                pool = {'name': s.split()[3], 'network': None, 'router': None}
                cfg['dhcp_pools'][pool['name']] = pool
                cur = ('dhcp', pool)
            elif s == 'service password-encryption':
                cfg['pw_encrypt'] = True
            elif s.startswith('enable password'):
                cfg['enable_password'] = True
            elif s.startswith('enable secret'):
                cfg['enable_secret'] = True
            elif s.startswith('line '):
                ln = {'password': False, 'login': False, 'transport': None}
                cfg['lines'][s[5:]] = ln
                cur = ('line', ln)
            elif s.startswith(('access-list ', 'ip access-list ')):
                cfg['acls'].add(s.split()[1] if s.startswith('access-list') else s.split()[3])
            continue
        if cur is None:
            continue
        kind, obj = cur
        if kind == 'router':
            obj.append(s)
        elif kind == 'dhcp':
            if s.startswith('network '):
                p = s.split()
                try:
                    obj['network'] = ipaddress.IPv4Network(f'{p[1]}/{p[2]}', strict=False)
                except (ValueError, IndexError):
                    pass
            elif s.startswith('default-router '):
                obj['router'] = s.split()[1]
        elif kind == 'line':
            if s.startswith('password '):
                obj['password'] = not s.startswith(('password 7 ', 'password 5 '))
            elif s.startswith('login'):
                obj['login'] = True
            elif s.startswith('transport input'):
                obj['transport'] = s.split()[2:]
        elif kind == 'if':
            i = obj
            p = s.split()
            if s.startswith('description '):
                i.desc = s[12:]
            elif s.startswith('ip address dhcp'):
                i.dhcp = True
            elif s.startswith('ip address ') and len(p) >= 4:
                try:
                    i.ips.append(ipaddress.IPv4Interface(f'{p[2]}/{p[3]}'))
                except ValueError:
                    pass
            elif s == 'shutdown':
                i.shutdown = True
            elif s.startswith('switchport mode '):
                i.mode = p[2] if p[2] in ('access', 'trunk') else None
            elif s.startswith('switchport access vlan '):
                i.access_vlan = int(p[3])
            elif s.startswith('switchport trunk native vlan '):
                i.native_vlan = int(p[4])
            elif s.startswith('switchport trunk allowed vlan '):
                i.allowed = ' '.join(p[4:])
            elif s.startswith('ip nat '):
                i.nat = p[2]
            elif s.startswith('ip helper-address '):
                i.helpers.append(p[2])
            elif s.startswith('encapsulation dot1Q '):
                i.dot1q = int(p[2])
            elif s.startswith('channel-group '):
                i.channel_group = p[1]


class Link:
    def __init__(self, el, byref):
        c = el.find('CABLE')
        ports = [x.text for x in c.findall('PORT')]
        self.a = byref.get((c.findtext('FROM') or '').removeprefix('save-ref-id:'))
        self.b = byref.get((c.findtext('TO') or '').removeprefix('save-ref-id:'))
        self.ap, self.bp = (ports + ['?', '?'])[:2]
        self.media = el.findtext('TYPE', '').removeprefix('e')
        self.cable = c.findtext('TYPE', '').removeprefix('e')
        self.functional = c.findtext('FUNCTIONAL') != 'false'

    def ends(self):
        return [(self.a, self.ap), (self.b, self.bp)]


class Topology:
    def __init__(self, path):
        self.path = path
        raw = Path(path).read_bytes()
        self.root = ET.fromstring(pktcrypto.decode(raw)) if raw[:1] != b'<' else ET.fromstring(raw)
        self.version = self.root.findtext('VERSION')
        self.devices = [Device(d.find('ENGINE'), d.find('WORKSPACE'))
                        for d in self.root.findall('./NETWORK/DEVICES/DEVICE')]
        byref = {d.ref: d for d in self.devices}
        self.links = [Link(l, byref) for l in self.root.findall('./NETWORK/LINKS/LINK')]
        seen = {}
        for d in self.devices:
            seen[d.hostname] = seen.get(d.hostname, 0) + 1
        for d in self.devices:
            d.disp = f'{d.hostname}/{d.name}' if seen[d.hostname] > 1 else d.hostname

    def find(self, name):
        n = name.lower()
        for key in (lambda d: d.name, lambda d: d.disp, lambda d: d.hostname):
            hits = [d for d in self.devices if key(d).lower() == n]
            if len(hits) == 1:
                return hits[0]
            if hits:
                raise SystemExit(f'{name!r} is ambiguous: ' + ', '.join(d.disp for d in hits))
        raise SystemExit(f'no device named {name!r}; try: ' + ', '.join(d.disp for d in self.devices))

    def peer(self, dev, port):
        for l in self.links:
            if l.a is dev and l.ap == port:
                return l.b, l.bp, l
            if l.b is dev and l.bp == port:
                return l.a, l.ap, l
        return None


# --- lint -----------------------------------------------------------------

def _norm_cfg(lines):
    skip = ('Building configuration', 'Current configuration', '!')
    return [l.rstrip() for l in lines if l.strip() and not l.strip().startswith(skip)]


def _port_ip(dev, port):
    if dev.ios:
        i = dev.ifaces.get(port)
        return i.ips[0] if i and i.ips else None
    ips = [p['ip'] for p in dev.host_ports if p['ip']]
    return ips[0] if len(ips) == 1 else None


HOST_KINDS = {'Pc', 'Server', 'Laptop', 'Printer', 'TabletPC', 'Pda', 'IPPhone', 'SMARTPHONE'}


def _linked(topo, dev):
    return any(dev in (l.a, l.b) for l in topo.links)


def lint(topo):
    out = []

    def add(sev, where, msg):
        out.append((sev, where, msg))

    all_ips = {}
    for d in topo.devices:
        for ifn, ip in d.ips():
            all_ips.setdefault(str(ip.ip), []).append(f'{d.disp} {short(ifn)}')
    for ip, owners in all_ips.items():
        if len(owners) > 1:
            add('ERROR', ip, 'duplicate IP: ' + ', '.join(owners))

    for d in topo.devices:
        if not d.power:
            add('WARN', d.disp, 'device is powered off')
        if d.ios:
            run, start = _norm_cfg(d.running), _norm_cfg(d.startup)
            if not start:
                add('WARN', d.disp, 'startup-config empty - never saved (copy run start)')
            elif run != start:
                n = sum(1 for x in difflib.ndiff(start, run) if x[:1] in '+-')
                add('WARN', d.disp, f'unsaved changes: running differs from startup ({n} lines)')
            c = d.cfg
            sec = []
            plain = [ln for ln, v in c['lines'].items() if v['password']]
            if plain and not c['pw_encrypt']:
                sec.append(f'plaintext passwords on {", ".join(plain)} (no service password-encryption)')
            if c['enable_password'] and not c['enable_secret']:
                sec.append('enable password instead of enable secret')
            telnet = [ln for ln, v in c['lines'].items()
                      if ln.startswith('vty') and v['login'] and v['transport'] != ['ssh']]
            if telnet:
                sec.append(f'telnet allowed on {", ".join(telnet)}')
            if sec:
                add('INFO', d.disp, 'security: ' + '; '.join(sec))
            used = ' '.join(c['nat_rules'])
            for pool in c['nat_pools']:
                if f' pool {pool}' not in used:
                    add('INFO', d.disp, f'NAT pool {pool} defined but not used by any nat rule')
            if c['nat_rules']:
                nats = {i.nat for i in d.ifaces.values()}
                for side in ('inside', 'outside'):
                    if side not in nats:
                        add('ERROR', d.disp, f'NAT rules present but no interface is "ip nat {side}"')
            mine = {str(ip.ip) for _, ip in d.ips()}
            for p in c['dhcp_pools'].values():
                if p['router'] and p['router'] not in all_ips:
                    add('WARN', d.disp, f'DHCP pool {p["name"]} default-router {p["router"]} is not configured on any device')
                if p['network'] and p['router'] and ipaddress.IPv4Address(p['router']) not in p['network']:
                    add('ERROR', d.disp, f'DHCP pool {p["name"]} default-router {p["router"]} outside {p["network"]}')
            for i in d.ifaces.values():
                if i.mode == 'access' and d.vlans and i.access_vlan not in d.vlans:
                    add('WARN', d.disp, f'{short(i.name)} access vlan {i.access_vlan} not in VLAN database')
        else:
            if not d.host_ports and d.kind in HOST_KINDS and _linked(topo, d):
                add('WARN', d.disp, 'connected but has no IP address and DHCP off')
            for p in d.host_ports:
                ip, gw = p['ip'], p['gateway']
                if p['dhcp'] or not ip:
                    continue
                if not gw or gw == '0.0.0.0':
                    add('WARN', d.disp, f'{ip} has no default gateway')
                    continue
                try:
                    gwa = ipaddress.IPv4Address(gw)
                except ValueError:
                    continue
                if gwa not in ip.network:
                    add('ERROR', d.disp, f'gateway {gw} is outside its subnet {ip.network}')
                elif gw not in all_ips:
                    add('WARN', d.disp, f'gateway {gw} is not configured on any device')

    for l in topo.links:
        if not (l.a and l.b):
            continue
        where = f'{l.a.disp} {short(l.ap)} <-> {l.b.disp} {short(l.bp)}'
        if not l.functional:
            add('ERROR', where, 'cable marked non-functional (wrong cable type?)')
        for dev, port in l.ends():
            i = dev.ifaces.get(port) if dev.ios else None
            if i and i.shutdown:
                add('ERROR', where, f'{dev.disp} {short(port)} is shutdown')
        ia, ib = _port_ip(l.a, l.ap), _port_ip(l.b, l.bp)
        if ia and ib and ia.network != ib.network:
            # Mask mismatch where each still sees the other as on-link "works", but is wrong.
            sev = 'WARN' if ia.ip in ib.network and ib.ip in ia.network else 'ERROR'
            add(sev, where, f'subnet mismatch: {ia.with_prefixlen} vs {ib.with_prefixlen}')
        if l.a.kind == 'Switch' and l.b.kind == 'Switch' and l.a.ios and l.b.ios:
            sa, sb = l.a.ifaces.get(l.ap), l.b.ifaces.get(l.bp)
            if sa and sb:
                modes = {sa.mode, sb.mode}
                if modes == {'access', 'trunk'}:
                    add('ERROR', where, 'trunk/access mismatch')
                elif sa.mode == sb.mode == 'access' and sa.access_vlan != sb.access_vlan:
                    add('WARN', where, f'access VLAN mismatch {sa.access_vlan} vs {sb.access_vlan}')
                elif 'trunk' in modes and None not in modes and sa.native_vlan != sb.native_vlan:
                    add('WARN', where, f'native VLAN mismatch {sa.native_vlan} vs {sb.native_vlan}')
    order = {'ERROR': 0, 'WARN': 1, 'INFO': 2}
    return sorted(dict.fromkeys(out), key=lambda x: order[x[0]])


# --- output ---------------------------------------------------------------

def table(rows, header):
    rows = [header] + [[str(c) for c in r] for r in rows]
    w = [max(len(r[i]) for r in rows) for i in range(len(header))]
    lines = ['  '.join(c.ljust(w[i]) for i, c in enumerate(r)).rstrip() for r in rows]
    lines.insert(1, '  '.join('-' * x for x in w))
    return '\n'.join(lines)


def show_devices(t):
    rows = []
    for d in t.devices:
        note = '' if d.power else 'POWERED OFF'
        if d.ios and not _norm_cfg(d.startup):
            note = (note + ' unsaved').strip()
        rows.append([d.disp, '' if d.name in d.disp else d.name, d.kind, d.model, note])
    print(table(rows, ['hostname', 'pt-name', 'type', 'model', 'notes']))


def _end_str(dev, port):
    s = f'{dev.disp if dev else "?"} {short(port)}'
    ip = _port_ip(dev, port) if dev else None
    return s + (f' [{ip.with_prefixlen}]' if ip else '')


def show_links(t):
    rows = [[_end_str(l.a, l.ap), _end_str(l.b, l.bp), l.cable or l.media,
             '' if l.functional else 'NON-FUNCTIONAL'] for l in t.links]
    print(table(rows, ['end A', 'end B', 'cable', '']))


def show_addr(t):
    rows = []
    for d in t.devices:
        if d.ios:
            for i in d.ifaces.values():
                if i.ips or i.dhcp:
                    for ip in i.ips or [None]:
                        rows.append([d.disp, short(i.name), ip.with_prefixlen if ip else 'dhcp',
                                     str(ip.network) if ip else '', '', 'down' if i.shutdown else '',
                                     i.desc])
        else:
            if not d.host_ports and _linked(t, d):
                rows.append([d.disp, '', 'unconfigured', '', '', '', ''])
            for p in d.host_ports:
                rows.append([d.disp, p['type'], p['ip'].with_prefixlen if p['ip'] else 'dhcp',
                             str(p['ip'].network) if p['ip'] else '', p['gateway'] if not p['dhcp'] else '',
                             '', f'dns {d.dns}' if d.dns else ''])
    print(table(rows, ['device', 'iface', 'address', 'network', 'gateway', 'state', 'note']))


def show_switching(t):
    for d in t.devices:
        if not (d.ios and d.kind == 'Switch'):
            continue
        extra = {k: v for k, v in d.vlans.items() if k not in (1, 1002, 1003, 1004, 1005)}
        trunks = [short(i.name) + (f' native {i.native_vlan}' if i.native_vlan != 1 else '')
                  + (f' allowed {i.allowed}' if i.allowed else '')
                  for i in d.ifaces.values() if i.mode == 'trunk']
        access = {}
        for i in d.ifaces.values():
            if i.access_vlan != 1 and i.mode != 'trunk':
                access.setdefault(i.access_vlan, []).append(short(i.name))
        print(f'{d.disp}: vlans {extra or "default only"}')
        if trunks:
            print('  trunks: ' + ', '.join(trunks))
        for v, ps in sorted(access.items()):
            print(f'  vlan {v}: ' + ', '.join(ps))


def show_routing(t):
    for d in t.devices:
        if not d.ios or d.kind == 'Switch' and not d.cfg['routing'] and not d.cfg['static']:
            continue
        c = d.cfg
        if not (c['routing'] or c['static'] or c['nat_rules'] or c['dhcp_pools']):
            continue
        print(f'{d.disp}:')
        for b in c['routing']:
            print('  ' + b[0] + ': ' + '; '.join(b[1:]))
        for s in c['static']:
            print('  ip route ' + s)
        for r in c['nat_rules']:
            print('  ' + r)
        for p in c['dhcp_pools'].values():
            print(f'  dhcp pool {p["name"]}: {p["network"]} gw {p["router"]}')
        subs = [f'{short(i.name)} dot1q {i.dot1q}' for i in d.ifaces.values() if i.dot1q]
        if subs:
            print('  subinterfaces: ' + ', '.join(subs))


def show_lint(t):
    f = lint(t)
    if not f:
        print('no findings')
    for sev, where, msg in f:
        print(f'{sev:5}  {where}: {msg}')


def cmd_summary(t, a):
    kinds = {}
    for d in t.devices:
        kinds[d.kind] = kinds.get(d.kind, 0) + 1
    print(f'# {Path(t.path).name}  (Packet Tracer {t.version})')
    print(f'{len(t.devices)} devices ({", ".join(f"{v} {k}" for k, v in kinds.items())}), {len(t.links)} links\n')
    for title, fn in [('Devices', show_devices), ('Links', show_links), ('Addressing', show_addr),
                      ('Switching', show_switching), ('Routing / NAT / DHCP', show_routing),
                      ('Lint', show_lint)]:
        print(f'## {title}')
        fn(t)
        print()


def cmd_device(t, a):
    d = t.find(a.name)
    print(f'# {d.label}  {d.kind} {d.model}  power={"on" if d.power else "OFF"}')
    print('\n## Connections')
    for l in t.links:
        for (x, xp), (y, yp) in [(l.ends()[0], l.ends()[1]), (l.ends()[1], l.ends()[0])]:
            if x is d:
                print(f'  {short(xp):10} -> {_end_str(y, yp)}  ({l.cable or l.media})')
    if not d.ios:
        print(f'\n## Host settings\n  gateway {d.gateway or "-"}  dns {d.dns or "-"}')
        for p in d.host_ports:
            print(f'  {p["type"]}: {"dhcp" if p["dhcp"] else p["ip"]}  mac {p["mac"]}  gw {p["gateway"]}'
                  + ('  ipv6' if p['ipv6'] else ''))
        return
    if a.diff:
        diff = list(difflib.unified_diff(_norm_cfg(d.startup), _norm_cfg(d.running),
                                         'startup-config', 'running-config', lineterm=''))
        print('\n## startup -> running diff\n' + ('\n'.join(diff) or '  (identical)'))
        return
    which = 'startup' if a.startup else 'running'
    lines = d.startup if a.startup else d.running
    print(f'\n## {which}-config')
    print('\n'.join(lines) if lines else '  (empty)')


def cmd_log(t, a):
    logs = t.root.find('COMMAND_LOGS')
    rx = re.compile(a.grep, re.I) if a.grep else None
    dev = t.find(a.device) if a.device else None
    rows = []
    for e in (logs if logs is not None else []):
        try:
            f = bytes.fromhex(e.text or '').decode(errors='replace').split('\0')
        except ValueError:
            continue
        f += [''] * (5 - len(f))
        when, name, prompt, typed, expanded = f[:5]
        if dev and name != dev.name:
            continue
        if rx and not rx.search(typed + ' ' + expanded):
            continue
        try:
            when = datetime.strptime(when, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
        tail = f'   [{expanded}]' if expanded and expanded.strip() != typed.strip() else ''
        rows.append(f'{when}  {prompt} {typed}{tail}')
    if a.n:
        rows = rows[-a.n:]
    print('\n'.join(rows) if rows else '(no matching log entries)')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    for name in ('summary', 'devices', 'links', 'addr', 'lint'):
        sp.add_parser(name).add_argument('file')
    p = sp.add_parser('device')
    p.add_argument('file'); p.add_argument('name')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--startup', action='store_true'); g.add_argument('--diff', action='store_true')
    p = sp.add_parser('log')
    p.add_argument('file'); p.add_argument('-d', '--device'); p.add_argument('-g', '--grep')
    p.add_argument('-n', type=int, help='last N entries')
    p = sp.add_parser('xml')
    p.add_argument('file'); p.add_argument('-o', '--out', required=True)
    p = sp.add_parser('encode')
    p.add_argument('xml'); p.add_argument('out')
    a = ap.parse_args()

    if a.cmd == 'xml':
        Path(a.out).write_bytes(pktcrypto.decode(Path(a.file).read_bytes()))
        print(f'wrote {a.out}')
        return
    if a.cmd == 'encode':
        data = Path(a.xml).read_bytes()
        ET.fromstring(data)  # refuse to wrap malformed XML
        Path(a.out).write_bytes(pktcrypto.encode(data))
        print(f'wrote {a.out}')
        return
    t = Topology(a.file)
    {'summary': cmd_summary, 'device': cmd_device, 'log': cmd_log,
     'devices': lambda t, a: show_devices(t), 'links': lambda t, a: show_links(t),
     'addr': lambda t, a: show_addr(t), 'lint': lambda t, a: show_lint(t)}[a.cmd](t, a)


if __name__ == '__main__':
    main()
