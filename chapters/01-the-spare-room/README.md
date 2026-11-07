# Chapter 1: The Spare Room

> **Status:** assignment drafted; not built or accepted.

[Project overview](../../README.md) · [Troubleshooting record](troubleshooting.md)

## The business change

A solo developer is building a mobile game from home. They need a workstation, a server for builds and a test website, Wi-Fi for a test device, and reliable internet access. The budget is small, but the business intends to hire: the addressing plan should leave room for growth.

## Assignment

Design and build the home-office network in Packet Tracer. Make the addressing, naming and configuration decisions yourself. The tutor reviews your submission and maintains this record.

### Required equipment

| Device | Role |
|---|---|
| Edge router | Connect the LAN to the simulated ISP using NAT. |
| 2960 switch | Connect the home-office LAN. |
| PC | Development workstation. |
| Server | Store builds and provide the game's HTTP test site. |
| Wireless access point | Connect a wireless test device. |
| Smartphone (optional) | Test client for Wi-Fi and the game website. |
| ISP router | Simulate external hosts using loopback interfaces. |

### Requirements and constraints

- Plan addressing with VLSM and room for additional sites and future segmentation; explain the allocation choices.
- Use static host addresses for this chapter. Add only services needed by this assignment.
- Use documentation address ranges for the simulated ISP: `192.0.2.0/24`, `198.51.100.0/24` or `203.0.113.0/24`.
- Choose consistent device names and interface descriptions. Small easter eggs are welcome.
- Configure baseline device access protection: hostname, enable secret, console/VTY authentication, password encryption, banner and idle timeout. Describe used interfaces and shut unused switch ports.
- Save every device configuration. Use lab-only credentials.

The goals are a justified addressing plan, working local and external connectivity, basic NAT, and a network that can be extended without starting over.

## Topology and lab

**Topology screenshot:** pending — [placeholder](topology.png.placeholder). The actual screenshot will be embedded here once the network exists.

**Accepted Packet Tracer file:** pending — [placeholder](network.pkt.placeholder). This will be the accepted Chapter 1 snapshot; exercises will use separate copies.

**Baseline identity:** not assigned.

## Design response

Pending Matt's build. The tutor will capture the addressing table, naming choices, growth allowance and design reasoning from the work and conversation.

| Device / interface | Address / prefix | Purpose |
|---|---|---|
| Pending | Pending | No configuration has been built yet. |

## Review and acceptance

All checks are currently pending.

| Requirement | Evidence required | Result |
|---|---|---|
| Wired hosts reach each other | Actual Packet Tracer connectivity checks | Pending |
| Wi-Fi works if a wireless test device is included | Association and connectivity from that device | Pending |
| Workstation and included test device reach the server's HTTP site | Actual application test | Pending |
| Hosts reach the ISP loopbacks | Actual connectivity checks from applicable clients/server | Pending |
| LAN traffic is translated | Router NAT translations after generating traffic | Pending |
| Addressing, access protection and saved configurations match the brief | Saved-state inspection and configuration comparison | Pending |
| Configuration findings are resolved | Lint leads reviewed against the design; no unexplained errors/warnings | Pending |
| Baseline is preserved | Accepted file, hash and version/tag recorded | Pending |

Lint alone cannot establish connectivity. Planned chapter limitations are recorded as such rather than presented as production-grade security.

## Troubleshooting

[No exercises have been run yet.](troubleshooting.md) After acceptance, the tutor can offer an optional addressing or gateway exercise on a copy.
