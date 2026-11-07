"""Encode/decode Cisco Packet Tracer .pkt/.pka files <-> XML. Pure Python, stdlib only.

PT 7+ container (reverse-engineered by the pka2xml project):
  file = obfuscate1( TwofishEAX( obfuscate2( be32(len(xml)) + zlib(xml) ) ) )
  key = 0x89 * 16, nonce = 0x10 * 16, empty header, 16-byte tag appended.
PT 5/6 legacy container: byte[i] ^ (len - i), then be32 size + zlib.
"""
import zlib

# --- Twofish (128-bit key only; that's all PT uses) ------------------------

_Q0T = [[0x8,0x1,0x7,0xD,0x6,0xF,0x3,0x2,0x0,0xB,0x5,0x9,0xE,0xC,0xA,0x4],
        [0xE,0xC,0xB,0x8,0x1,0x2,0x3,0x5,0xF,0x4,0xA,0x6,0x7,0x0,0x9,0xD],
        [0xB,0xA,0x5,0xE,0x6,0xD,0x9,0x0,0xC,0x8,0xF,0x3,0x2,0x4,0x7,0x1],
        [0xD,0x7,0xF,0x4,0x1,0x2,0x6,0xE,0x9,0xB,0x3,0x0,0x8,0x5,0xC,0xA]]
_Q1T = [[0x2,0x8,0xB,0xD,0xF,0x7,0x6,0xE,0x3,0x1,0x9,0x4,0x0,0xA,0xC,0x5],
        [0x1,0xE,0x2,0xB,0x4,0xC,0x3,0x7,0x6,0xD,0xA,0x5,0xF,0x9,0x0,0x8],
        [0x4,0xC,0x7,0x5,0x1,0x6,0x9,0xA,0x0,0xE,0xD,0x8,0x2,0xB,0x3,0xF],
        [0xB,0x9,0x5,0x1,0xC,0x3,0xD,0xE,0x6,0x4,0x7,0xF,0x2,0x0,0x8,0xA]]
_MDS = [[0x01,0xEF,0x5B,0x5B],[0x5B,0xEF,0xEF,0x01],[0xEF,0x5B,0x01,0xEF],[0xEF,0x01,0xEF,0x5B]]
_RS = [[0x01,0xA4,0x55,0x87,0x5A,0x58,0xDB,0x9E],[0xA4,0x56,0x82,0xF3,0x1E,0xC6,0x68,0xE5],
       [0x02,0xA1,0xFC,0xC1,0x47,0xAE,0x3D,0x19],[0xA4,0x55,0x87,0x5A,0x58,0xDB,0x9E,0x03]]
_M32 = 0xFFFFFFFF


def _ror4(x, n):
    return ((x >> n) | (x << (4 - n))) & 0xF


def _q(t, x):
    a, b = x >> 4, x & 0xF
    a, b = a ^ b, a ^ _ror4(b, 1) ^ ((8 * a) & 0xF)
    a, b = t[0][a], t[1][b]
    a, b = a ^ b, a ^ _ror4(b, 1) ^ ((8 * a) & 0xF)
    a, b = t[2][a], t[3][b]
    return (b << 4) | a


_Q0 = [_q(_Q0T, x) for x in range(256)]
_Q1 = [_q(_Q1T, x) for x in range(256)]


def _gfmul(a, b, poly):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x100:
            a ^= poly
        b >>= 1
    return r


def _rol(x, n):
    return ((x << n) | (x >> (32 - n))) & _M32


def _ror(x, n):
    return ((x >> n) | (x << (32 - n))) & _M32


def _bytes(w):
    return [(w >> (8 * i)) & 0xFF for i in range(4)]


def _sboxes(L):
    l0, l1 = _bytes(L[0]), _bytes(L[1])
    return [lambda y: _Q1[_Q0[_Q0[y] ^ l1[0]] ^ l0[0]],
            lambda y: _Q0[_Q0[_Q1[y] ^ l1[1]] ^ l0[1]],
            lambda y: _Q1[_Q1[_Q0[y] ^ l1[2]] ^ l0[2]],
            lambda y: _Q0[_Q1[_Q1[y] ^ l1[3]] ^ l0[3]]]


def _h(x, L):
    s, y = _sboxes(L), _bytes(x)
    out = 0
    for i in range(4):
        v = 0
        for j in range(4):
            v ^= _gfmul(_MDS[i][j], s[j](y[j]), 0x169)
        out |= v << (8 * i)
    return out


class Twofish:
    def __init__(self, key):
        if len(key) != 16:
            raise ValueError('only 128-bit keys supported')
        m = [int.from_bytes(key[4 * i:4 * i + 4], 'little') for i in range(4)]
        me, mo = [m[0], m[2]], [m[1], m[3]]
        S = []
        for i in range(2):
            blk = key[8 * i:8 * i + 8]
            s = []
            for row in _RS:
                v = 0
                for c in range(8):
                    v ^= _gfmul(row[c], blk[c], 0x14D)
                s.append(v)
            S.append(s[0] | s[1] << 8 | s[2] << 16 | s[3] << 24)
        self.K = []
        rho = 0x01010101
        for i in range(20):
            a = _h(2 * i * rho & _M32, me)
            b = _rol(_h((2 * i + 1) * rho & _M32, mo), 8)
            self.K.append((a + b) & _M32)
            self.K.append(_rol((a + 2 * b) & _M32, 9))
        sb = _sboxes([S[1], S[0]])
        # Key-dependent g() lookup tables: column j of MDS times sbox_j(x).
        self.T = [[sum(_gfmul(_MDS[i][j], sb[j](x), 0x169) << (8 * i) for i in range(4))
                   for x in range(256)] for j in range(4)]

    def _g(self, x):
        T = self.T
        return T[0][x & 0xFF] ^ T[1][(x >> 8) & 0xFF] ^ T[2][(x >> 16) & 0xFF] ^ T[3][x >> 24]

    def encrypt(self, blk):
        K, g = self.K, self._g
        r0, r1, r2, r3 = (int.from_bytes(blk[4 * i:4 * i + 4], 'little') ^ K[i] for i in range(4))
        for r in range(16):
            t0, t1 = g(r0), g(_rol(r1, 8))
            f0 = (t0 + t1 + K[2 * r + 8]) & _M32
            f1 = (t0 + 2 * t1 + K[2 * r + 9]) & _M32
            r2, r3 = _ror(r2 ^ f0, 1), _rol(r3, 1) ^ f1
            r0, r1, r2, r3 = r2, r3, r0, r1
        out = (r2 ^ K[4], r3 ^ K[5], r0 ^ K[6], r1 ^ K[7])
        return b''.join(w.to_bytes(4, 'little') for w in out)


# --- EAX mode (CMAC + CTR) ------------------------------------------------

def _xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def _dbl(b):
    n = int.from_bytes(b, 'big') << 1
    if n >> 128:
        n = (n ^ 0x87) & ((1 << 128) - 1)
    return n.to_bytes(16, 'big')


def _cmac(tf, msg):
    k1 = _dbl(tf.encrypt(bytes(16)))
    k2 = _dbl(k1)
    if msg and len(msg) % 16 == 0:
        last = _xor(msg[-16:], k1)
        body = msg[:-16]
    else:
        tail = len(msg) % 16
        body = msg[:len(msg) - tail]
        last = _xor(msg[len(body):] + b'\x80' + bytes(15 - tail), k2)
    x = bytes(16)
    for i in range(0, len(body), 16):
        x = tf.encrypt(_xor(x, body[i:i + 16]))
    return tf.encrypt(_xor(x, last))


def _omac(tf, t, msg):
    return _cmac(tf, bytes(15) + bytes([t]) + msg)


def _ctr(tf, start, data):
    ctr = int.from_bytes(start, 'big')
    out = bytearray(len(data))
    for i in range(0, len(data), 16):
        ks = tf.encrypt(ctr.to_bytes(16, 'big'))
        ctr = (ctr + 1) & ((1 << 128) - 1)
        chunk = data[i:i + 16]
        out[i:i + len(chunk)] = _xor(chunk, ks)
    return bytes(out)


KEY = bytes([0x89] * 16)
NONCE = bytes([0x10] * 16)


def eax_decrypt(data, key=KEY, nonce=NONCE, verify=True):
    tf = Twofish(key)
    ct, tag = data[:-16], data[-16:]
    n = _omac(tf, 0, nonce)
    if verify and _xor(_xor(n, _omac(tf, 1, b'')), _omac(tf, 2, ct)) != tag:
        raise ValueError('EAX tag mismatch')
    return _ctr(tf, n, ct)


def eax_encrypt(pt, key=KEY, nonce=NONCE):
    tf = Twofish(key)
    n = _omac(tf, 0, nonce)
    ct = _ctr(tf, n, pt)
    return ct + _xor(_xor(n, _omac(tf, 1, b'')), _omac(tf, 2, ct))


# --- Container ------------------------------------------------------------

def _unwrap(payload):
    size = int.from_bytes(payload[:4], 'big')
    xml = zlib.decompress(payload[4:])
    if len(xml) != size:
        raise ValueError(f'size header {size} != decompressed {len(xml)}')
    return xml


def decode(data, verify=True):
    """Return the XML bytes inside a .pkt/.pka file."""
    n = len(data)
    try:
        s1 = bytes(data[n - 1 - i] ^ ((n - i * n) & 0xFF) for i in range(n))
        s2 = eax_decrypt(s1, verify=verify)
        m = len(s2)
        return _unwrap(bytes(s2[i] ^ ((m - i) & 0xFF) for i in range(m)))
    except (ValueError, zlib.error) as modern_err:
        try:  # PT 5/6 legacy format
            return _unwrap(bytes(data[i] ^ ((n - i) & 0xFF) for i in range(n)))
        except (ValueError, zlib.error):
            raise ValueError(f'not a recognised Packet Tracer file ({modern_err})') from None


def encode(xml):
    """Wrap XML bytes as a PT 7+ .pkt/.pka file."""
    payload = len(xml).to_bytes(4, 'big') + zlib.compress(xml, 9)
    m = len(payload)
    s2 = bytes(payload[i] ^ ((m - i) & 0xFF) for i in range(m))
    s1 = eax_encrypt(s2)
    n = len(s1)
    out = bytearray(n)
    for i in range(n):
        out[n - 1 - i] = s1[i] ^ ((n - i * n) & 0xFF)
    return bytes(out)


def selftest():
    assert Twofish(bytes(16)).encrypt(bytes(16)).hex() == '9f589f5cf6122c32b6bfec2f2ae8c35a'
    xml = b'<PACKETTRACER5><VERSION>selftest</VERSION></PACKETTRACER5>'
    assert decode(encode(xml)) == xml
