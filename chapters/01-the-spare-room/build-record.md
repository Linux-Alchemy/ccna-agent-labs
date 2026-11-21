# Chapter 1 — The Spare Room: Build Record

[Chapter summary](README.md) · [Assignment](assignment.md) · [Troubleshooting](troubleshooting.md)

**Current outcome:** Accepted on 2026-11-21. This record preserves the design, evidence, assistance and dated review history. Earlier pending findings describe their state at the time; the [final acceptance](#chapter-1-accepted--2026-11-21) closes the review.

## Baseline Identity

[View the topology](README.md#topology-and-accepted-lab).

- **Accepted chapter file:** [spare-room.pkt](spare-room.pkt) — Matt’s original filename; preserve unchanged and use local copies for further work or troubleshooting.
- **Baseline version:** `chapter-1-v1`.
- **Baseline SHA-256:** `059548ee5c6adecccd14b34f98054eb7c3615d6e1361158a6e1134d59e8c0b3f`.
- **Accepted:** 2026-11-21, based on saved-state inspection and Matt’s reported Packet Tracer tests.

## Design Response

Matt chose the standard private network `192.168.0.0/24` and intentionally kept this first home-office chapter on one shared LAN without departmental VLANs. He noted that a typical small home setup might combine routing, switching and wireless in one device; separate devices here expose those configurations for hands-on practice.

The next expansion will integrate additional networks as the company grows and Joe needs more developers. The accepted growth approach leaves future sites on separate, non-overlapping networks; exact subnet reservations have not been selected and are deferred to that expansion. No specific future allocations are attributed to Matt. The `/24` provides 254 usable addresses, with only a small portion currently used.

The table records the accepted implementation:

| Component | Saved configuration |
|---|---|
| RT01 office interface | 192.168.0.1/24 |
| SW01 management | 192.168.0.2/24; gateway 192.168.0.1 |
| Server0 | 192.168.0.3/24; gateway 192.168.0.1; DNS-client setting 192.168.0.3 |
| DHCP | RT01 pool KOBOLD-NET: 192.168.0.0/24; .1, .2 and .3 excluded; gateway .1 and DNS .3 |
| Client DNS fields | PC0 and phone both use 192.168.0.3 |
| DNS and HTTP | Server0 services enabled; dev.kobold.test → 192.168.0.3; koboldgaming.html present |
| Wireless | KoboldNetwork; active AP/phone authentication, encryption and nonempty key match; successful phone access by name reported |
| ISP link | RT01 203.0.113.1/30 ↔ ISP-RTR 203.0.113.2/30 |
| ISP loopbacks | 1.1.1.1/32 and 8.8.8.8/32; explicitly retained as isolated simulated destinations |
| Upstream routing/NAT | Default via 203.0.113.2; overload on Gi0/0, inside Gi1/0; ACL 1 matches 192.168.0.0/24 |

## Review and Acceptance

**Progress reported 2026-11-14:** Matt has drawn and labelled the topology and performed some baseline configuration on the switch and both routers. Task 2 is nearly complete; the working file is saved as `spare-room.pkt`.

**Focused inspection 2026-11-16:** Matt reports workstation address `169.254.39.206` and requests a nudge. The saved file has PC0 configured as a DHCP client and an RT01 DHCP pool whose network/mask matches its LAN interface. This is configuration evidence, not proof that a lease exchange succeeds. No network configuration was changed; the live failure cause and all behavioural acceptance checks remain unverified.

**Investigation pointer supplied:** “Use Simulation mode, filter for DHCP and ARP, then request DHCP again on the workstation. Follow the exchange: does its Discover reach RT01, and does an Offer come back? Tell me the last DHCP message you see and which device it reaches.”

This is assistance with the learner's build, not a sabotage exercise. Full chapter review remains pending.

**DHCP follow-up 2026-11-16:** Matt supplied router PING_CONFLICT messages for `192.0.2.2` and `192.0.2.3` and identified that only the router address had been excluded, leaving the statically addressed switch and server in the lease range. The tutor prompted comparison of static addresses with DHCP exclusions: “Does DHCP know about every address you’ve already given to a device, or only some of them?” After Matt proposed correcting the exclusions, the tutor advised: “Exclude the fixed addresses, then renew PC0’s lease and check that it gets an unused address.”

Matt reports PC0 continued receiving `.2` and the router terminal froze; after closing and reopening Packet Tracer, PC0 obtained a DHCP address and responded to a router ping. The latest lease address/settings and revised exclusions have not been inspected, and the cause of the freeze is not established. DHCP recovery is learner-reported, not full Task 3 acceptance. Matt also reports configuring NAT overload, which is part of Task 6; external reachability and translation verification remain pending.

**DNS and HTTP follow-up 2026-11-16:** Matt recognised that the simulated ISP loopback did not provide a DNS service. The tutor confirmed that the DHCP DNS option should point to the local DNS server, explained that an A record maps a name to an IPv4 address, and distinguished the HTTP filename from the DNS name. Matt reported successful PC0 name resolution to `192.0.2.3`, phone access to `http://192.0.2.3/koboldgaming.html`, and a phone ping to `1.1.1.1`. The phone still held DNS address `1.1.1.1`; after the tutor advised obtaining a fresh DHCP lease, Matt reported that renewal restored access by name at `dev.kobold.test`.

Matt now considers the build complete. These are learner-reported tests, not full chapter acceptance. Confirm the latest saved submission, then inspect it against the brief and identify remaining behavioural evidence. The reported hostname differs from the brief's `dev.copperkobold.test`; reconcile it during review rather than silently changing the requirement. NAT verification, all required source/destination checks, design reasoning and the topology capture remain to be assessed.

### Submission review — 2026-11-16

Matt confirmed all latest changes were saved to `spare-room.pkt`. Reviewed SHA-256: `859fba44adeced210a2b72af8a7e451758c652d7ec6a4fdc404d919186c2bc2a`. The file was inspected only; no configuration was changed.

| Requirement / area | Evidence and finding | Result |
|---|---|---|
| DHCP configuration | Fixed addresses .1–.3 excluded; pool gateway and local DNS match the saved LAN/server configuration | Saved-state check passes; final client lease evidence pending |
| DNS / HTTP service | Enabled, with an A record and custom HTML file; user reports successful phone access by name after renewal | Function reported; chosen name/path differ from the brief and need agreement |
| Saving IOS configuration | Running and startup configs identical on RT01, ISP-RTR and SW01 | Pass |
| Addressing constraints / growth | Compare saved LAN and loopback allocations with Task 1 and required address categories; future reservations and reasoning not yet supplied | Needs review |
| NAT selection | Compare the address range selected by ACL 1 with the office subnet required by Task 6 | Needs review; translation evidence pending |
| Wireless | Compare saved access-point and phone settings with Task 4’s SSID/security requirement | Needs review |
| Device baseline | Check used switch-port descriptions and authentication coverage across every VTY range against Task 2; confirm intended idle-timeout behaviour | Needs review |
| Connectivity and NAT behaviour | Existing reports cover selected pings and website/name access, not the full test matrix | Remaining evidence pending |
| Topology capture | No actual image submitted | Pending |

Lint returned no ERROR/WARN entries and one INFO about SW01 VTY transport. That result does not override the requirement checks above. Review pointers supplied cover address categories, NAT selection scope, wireless settings and baseline completeness; no corrective configuration commands were provided. No accepted baseline created.

### Resume review — 2026-11-21

At Matt's request for a clear issue/action breakdown, re-inspected the current saved working file (SHA-256 `a430110dcb631c0b84a5dc19ca31a00a38ec97bfab2d8703a4e2343b801b0935`). The previously flagged address categories, NAT selection scope, wireless settings and baseline completeness still need attention. Current DNS record and client DNS settings are present; behaviour has not been retested. No network configuration changed.

The resume checklist explains the required address-category changes and dependent settings, NAT scope alignment, wireless security, interface descriptions/all VTY ranges, and final test evidence. Idle-timeout behaviour requires confirmation rather than assuming an omitted command means no timeout. Also reconcile the existing generic switch model with the brief's 2960 specification and the chosen website name/path with the brief before acceptance; do not require a hardware rebuild solely for an unreviewed model difference. Matt requested direct explanations of the outstanding work; no CLI repair script was supplied.

**Guided wireless setup — 2026-11-21:** Matt requested direct help configuring the access point. Tutor supplied GUI steps for the AP wireless interface (SSID, WPA2-PSK, passphrase and AES), matching phone settings, and DHCP/gateway/website checks. Setup and verification remain learner work and are not yet reported complete; record this as guided assistance. No lab configuration was edited by the tutor.

### Wireless and renumbering follow-up — 2026-11-21

Matt confirmed the lab was saved after configuring the WAP and reported phone website access by name plus successful pings from each device to other endpoints. Reviewed SHA-256: `27a713abfdbce3fd10c4fe5b7264ce4a184da36147b9063800eb7d07b188dd84`. File inspection was read-only.

**Confirmed improvements:** LAN is now private 192.168.0.0/24; router DHCP network/exclusions/options and server DNS record follow the new addresses; NAT selection matches the LAN; used switch ports have descriptions; RT01 VTY 5–15 now has a password. AP and phone active SSID/authentication/encryption/key match (KoboldNetwork, saved auth/encryption enums 4/4); phone association and service access are learner-reported. All three IOS running/startup configurations match. Unused switch ports remain shut down.

**Remaining checks:** SW01's saved default gateway references the old subnet; PC0's saved DNS field references the old server address (confirm current lease and browser/name behaviour); Server0's own DNS-client field still points at the simulated ISP loopback. SW01 VTY 5–15 still lacks a password/local-user authentication. Loopbacks remain outside the assigned documentation ranges. Confirm effective idle timeouts. Hostname/path and generic switch-model variations still need explicit agreement against the brief.

**Evidence remaining:** Matt's successful pings are recorded as reported results; exact source/destination coverage and NAT translations were not observed. Obtain translation output while client traffic runs, confirm both loopbacks were tested from required hosts and switch management return-path connectivity, capture the topology and record growth reservations/reasoning. Do not infer a successful NAT table or complete acceptance from a general ping report. No accepted baseline created.

**Learner update — 2026-11-21:** Matt reports completing the SW01 gateway, PC0 DNS, Server0 DNS-client and SW01 VTY authentication items. These changes have not yet been re-inspected. He asks for clarification of ISP loopbacks and says idle timeouts have not been covered in his course. Tutor clarified that the loopback addresses are functional simulated destinations; the issue is compliance with the brief's addressing convention, not broken routing. Tutor explained idle CLI session timeouts and Cisco's documented ten-minute default. Proposed retaining the isolated simulation loopbacks as a documented exception and using default idle timeouts rather than adding new configuration work; no requirement exception has yet been agreed or applied.

### Configuration closeout review — 2026-11-21

Matt confirmed the latest changes were saved and explicitly approved retaining the ISP loopbacks. Inspected SHA-256: `1aea7817ec0f36a7961860263a167ed140e881fab6318bab335503790e36a6a0`. The source file was not modified.

**Configuration review passes:** SW01 now uses gateway 192.168.0.1; PC0, the phone and Server0 use local DNS 192.168.0.3; SW01 VTY 5–15 now has a password and login configured. DHCP exclusions/options, the server A record, matching AP/phone wireless settings, subnet-aligned NAT selection, upstream default route, used-port descriptions and unused-port shutdowns remain present. Running/startup configurations match on all three IOS devices. Lint reports no ERROR/WARN entries; Telnet transport on later VTY ranges remains a lab limitation, not a new SSH-only requirement.

**Timeout choice:** Matt deliberately chose 30 minutes to reduce interruptions while working in the lab and would normally use a shorter interval elsewhere. Saved `exec-timeout 30 0` appears on RT01 console and VTY 5–15, plus SW01 console and VTY 0–15. RT01 VTY 0–4 and ISP-RTR lines retain defaults; the 30-minute choice is not applied universally, and no universal override is required.

**Brief reconciled:** Keep 1.1.1.1/32 and 8.8.8.8/32 as explicitly approved isolated ISP destinations; documentation-range requirements still apply to the WAN link. Accept the existing dev.kobold.test/koboldgaming.html naming and generic Layer 2 switch as functionally equivalent design choices for this chapter. Active assignment text now matches those choices; historical review entries are retained.

**Next:** Matt can take the topology screenshot now. Final acceptance still needs the actual image, NAT translation evidence, identification of the reported ping-test coverage and the addressing-growth reservations/reasoning. No repeated tests are required where Matt can identify already successful checks; configuration inspection does not fabricate their outputs. No accepted baseline created yet.

### Chapter 1 accepted — 2026-11-21

**Final submission:** `059548ee5c6adecccd14b34f98054eb7c3615d6e1361158a6e1134d59e8c0b3f`. The saved file changed after the preceding check; a fresh summary/lint and comparison confirmed the reviewed IOS running/startup, DNS, HTTP and wireless configuration blocks were unchanged. Latest client/server addressing remains consistent. The accepted `network.pkt` is a byte-for-byte copy of this submission.

**Learner-run test confirmation:** Matt explicitly confirmed NAT translation from all endpoints to the ISP loopback addresses and successful endpoint ping testing. This closes the previously requested PC0/server/phone coverage of both simulated ISP destinations. Earlier live reports established DHCP assignment and website access by IP and name, including the phone after renewal. The tutor accepts these as Matt’s reported execution evidence; no CLI output capture was supplied and the tutor did not independently execute Packet Tracer tests.

**Topology and reasoning:** Matt supplied the real topology screenshot now embedded above and explained the shared `/24`, absence of departmental VLANs, separate devices for configuration practice and planned integration of future networks. Exact future subnet allocations are deferred as a recorded design decision, rather than invented. The original requirement to preselect reservations is reconciled in Task 1 accordingly.

| Acceptance area | Evidence | Outcome |
|---|---|---|
| Addressing and growth | Private LAN, separate documentation-range WAN, agreed simulated loopbacks; learner’s design explanation and deferred future allocations | Accepted |
| Device baseline and saved state | Inspected access configuration, used-port descriptions, unused-port shutdowns, lab timeouts, matching IOS running/startup configs | Accepted |
| DHCP, DNS and HTTP | Inspected settings plus Matt’s successful client/service tests | Accepted |
| Wireless | Matching saved AP/phone SSID/security/key and Matt’s successful association/website test | Accepted with guided setup recorded |
| Local/external reachability and NAT | Inspected routing/NAT configuration plus Matt’s explicit all-endpoint ping/translation confirmation | Accepted on learner-reported tests |
| Topology and baseline preservation | Actual screenshot; unchanged source copied to versioned network.pkt with SHA-256 | Accepted |

Matt designed, configured, diagnosed and repaired the network. The tutor supplied the assignment, investigation pointers, requested explanations and guided wireless setup, reviewed saved state and maintained records. This was an assisted learning build, not a claim of an unaided assessment. No sabotage exercise has been run. The next action is optional troubleshooting on a separate copy, or agreeing Chapter 2 when Matt is ready.

## File organisation — 2026-11-21

The accepted chapter file retains Matt’s original name, `spare-room.pkt`. The redundant `network.pkt` copy was removed from the current tree. Baseline bytes, SHA-256 and the `chapter-1-v1` tag are unchanged; historical entries naming `network.pkt` describe the earlier layout. The newer unaccepted working save was preserved privately before consolidating the filenames.

Completed troubleshooting reports link their own clearly named before/after lab files. These are distinct exercise evidence, not additional chapter baselines.
