# Chapter 1 — The Spare Room

> **Company:** Copper Kobold Games
>
> **Status:** Accepted — 2026-11-21. Baseline `chapter-1-v1`.
>
> **Starting point:** New Packet Tracer network

[Project overview](../../README.md) · [Assignment](assignment.md) · [Build record](build-record.md) · [Troubleshooting](troubleshooting.md)

## Field Briefing

Joe Park has a day job, a spare room and an idea that won’t leave him alone: *Banners of Ashvale*, a mobile fantasy strategy RPG about small kingdoms, grumpy orc warlords and a kobold mascot who keeps stealing your gold. Joe names the company after the kobold. It feels like a joke at the time.

The spare room has a workstation, a small development server humming in the closet, and Joe’s old phone with the cracked screen—now officially “the test device.” Joe needs a dependable network for development, access to the game’s test website and connectivity beyond the home office. Client devices should receive their network settings automatically, and the test site should be reachable by name.

There’s no staff yet and no need for an elaborate network. However, Joe has the familiar sticky note on his monitor: *build it like you’ll need more someday.*

Your assignment is to design and build Copper Kobold’s first network.

## Topology and Accepted Lab

![Copper Kobold Games Chapter 1 topology: home-office LAN, wireless phone and simulated ISP](topology.png)

[Download the accepted Packet Tracer lab](spare-room.pkt) · Baseline **`chapter-1-v1`** · [Baseline identity](build-record.md#baseline-identity)

## Outcome and Review

Copper Kobold’s first network is accepted. A shared private LAN connects Joe’s workstation, development server and wireless test phone. It provides DHCP addressing, local DNS, the game’s HTTP test page and NAT overload through a simulated ISP.

Matt kept the office on one `/24` without departmental VLANs and used separate routing, switching and wireless devices to practise their configurations. Future sites will use separate networks, with exact allocations decided during expansion.

Review included saved-configuration checks and Matt’s reported successful connectivity, website and NAT tests. The tutor did not independently run Packet Tracer tests. The main lessons were excluding static addresses from DHCP, directing clients to the local DNS service and renewing leases after changing DNS settings. Wireless setup was guided; Matt performed all network configuration and repairs.

See the [design and addressing table](build-record.md#design-response) and [full review and acceptance evidence](build-record.md#review-and-acceptance) for details.

[T001 — Workstation cannot reach the development server](troubleshooting/T001.md) is resolved without diagnostic hints. Matt checked the client, identified the server addressing issue and verified his repair. Further exercises are listed in the [troubleshooting index](troubleshooting.md); the accepted baseline remains unchanged.
