# Chapter 1 — The Spare Room: Assignment

[Chapter summary](README.md) · [Build record](build-record.md) · [Troubleshooting](troubleshooting.md)

Read the [Field Briefing](README.md#field-briefing) for the business context. The completed checklist below reflects the accepted Chapter 1 build; detailed evidence and assistance are in the build record.

## Objectives

For this assignment to be successful, you must:

- Design an IPv4 addressing plan that supports the current office and leaves room for growth.
- Connect the workstation, development server and wireless access point.
- Apply consistent device naming and baseline device-access protection.
- Provide DHCP addressing and local DNS name resolution.
- Make the server’s HTTP test page accessible by name from the workstation and any included wireless client.
- Provide routed access to simulated external destinations using NAT.
- Demonstrate the required behaviour and save a reviewable Packet Tracer file.

## Equipment and Starting Conditions

Start with a blank Packet Tracer workspace.

| Device | Quantity | Role |
|---|---:|---|
| Edge router | 1 | Connect the home-office LAN to the simulated ISP and perform NAT. |
| Layer 2 switch | 1 | Connect the wired office devices; the submitted Switch-PT-Empty is accepted for this chapter’s basic switching requirements. |
| PC | 1 | Joe’s development workstation. |
| Server | 1 | Represent the development server, host the HTTP test page and provide local DNS. It may also host DHCP. |
| Wireless access point | 1 | Provide wireless access to the office LAN. |
| Smartphone | Optional | Represent Joe’s test phone and verify wireless connectivity. |
| ISP router | 1 | Provide the upstream connection and loopback interfaces representing external destinations. |

Choose router models with enough Ethernet interfaces for these roles.

The server represents the business’s development resources. Use Packet Tracer’s built-in services for the HTTP test site and local DNS. DHCP may run on the edge router or this server; choose one. You do not need to install a game, build system or file-sharing platform.

The ISP router and its loopbacks represent the internet. This lab does not connect to the real internet.

## Access and Required Parameters

| Item | Requirement |
|---|---|
| Office addressing | Use private IPv4 addresses. Keep infrastructure and the server static; use DHCP for the workstation and optional smartphone. |
| DHCP | Use one DHCP service on the office LAN. Supply the correct subnet mask, default gateway and local DNS server address; keep static addresses outside the lease pool. |
| DNS | Use the server’s built-in DNS service. Create an A record for `dev.kobold.test` pointing to the server’s fixed IPv4 address. |
| Address planning | Use VLSM where appropriate; leave unallocated space for future sites and segmentation. |
| ISP link addressing | Choose the edge-to-ISP subnet from `192.0.2.0/24`, `198.51.100.0/24` or `203.0.113.0/24`. |
| External destinations | Use ISP loopbacks `1.1.1.1/32` and `8.8.8.8/32` as agreed simulated reachability targets. They do not provide the corresponding real-world DNS services. |
| Office layout | One shared LAN for this chapter. |
| Routing | Use static/default routing as needed. |
| Translation | Allow office hosts to share the edge router’s ISP-facing address using NAT overload. |
| Test service | Enable HTTP on the development server; verify access by IP address and at `http://dev.kobold.test/koboldgaming.html`. |
| Credentials | Choose lab-only passwords and a wireless passphrase. |

DHCP stays on the single office LAN; no relay is needed in this chapter. DNS provides the local test-site record, not real internet name resolution. Departmental VLANs and remote-office connections are deferred to later assignments.

## Design Decisions

You choose:

- The private address block, subnet sizes and individual addresses.
- Whether DHCP runs on the edge router or server, and how the lease pool leaves room for static infrastructure addresses.
- How much address space to reserve for future growth.
- Device names, interface selections and descriptions.
- The wireless network name and passphrase.
- Lab credentials and a consistent naming scheme.

Be ready to explain why the addressing plan fits the current network and how it leaves room for expansion. The tutor will capture your reasoning and maintain the documentation.

## Section 1A — Establish the Home Office

### Task 1 — Plan the Network

**Objective:** Produce a coherent topology and addressing plan before configuring devices.

1. Identify the connections needed between the workstation, server, access point, switch, edge router and ISP router.
2. Select a private address block and allocate the office subnet. Set aside fixed addresses for infrastructure and the server, then define a non-overlapping DHCP lease range for clients. Identify the gateway and DNS settings DHCP must supply.
3. Leave room for separate, non-overlapping networks as the company grows. For this accepted chapter, exact remote-office and later segmentation allocations are deferred to the relevant expansion; do not build those networks now.
4. Allocate a separate subnet for the edge-to-ISP link from the documentation ranges. Use `1.1.1.1/32` and `8.8.8.8/32` for the two agreed simulated ISP destinations.
5. Identify each host’s default gateway and explain the intended path from the workstation to an external destination.

**Checkpoint:** Every planned interface or host has a valid fixed address or DHCP allocation where needed, subnets and address allocations do not overlap, and the growth allowance is identifiable.

### Task 2 — Assemble and Configure the Office

**Objective:** Establish a working wired LAN with consistent device configuration.

1. Place and cable the required equipment using suitable interfaces and cable types.
2. Assign meaningful hostnames to the IOS devices and descriptions to used interfaces.
3. Configure baseline device access: an enable secret, console and VTY authentication, password encryption, a login banner and idle timeouts. A 30-minute timeout is permitted for lab convenience; unchanged line defaults are also acceptable for this chapter.
4. Configure the office-facing router interface and the server’s fixed address, mask and gateway. The workstation will obtain its settings through DHCP in Task 3.
5. Configure a switch-management address and default gateway so the switch can be checked from the workstation.
6. Shut down unused switch ports, preserving ports allocated to the planned connections.
7. Save the IOS configurations.

**Checkpoint:** Required wired links are operational. The server can reach the office gateway and switch-management address using its fixed configuration.

### Task 3 — Provide DHCP and DNS

**Objective:** Give client devices automatic network settings and a usable name for the development server.

1. Enable one DHCP service on your chosen device and configure the planned lease range. Exclude all fixed infrastructure and server addresses from dynamic allocation.
2. Supply the office subnet mask, default gateway and local DNS server address through DHCP.
3. Set the workstation to obtain its network settings automatically. Verify the issued address is within the intended pool and the mask, gateway and DNS settings match the plan.
4. Inspect the DHCP lease or binding information available on your chosen device and relate it to the workstation’s address.
5. Enable DNS on the server and create the A record for `dev.kobold.test` using its fixed IPv4 address.
6. From the workstation, verify that the name resolves to the expected address. Confirm connectivity to the server, office gateway and switch-management address.

**Checkpoint:** The workstation has valid DHCP settings, the lease is evidenced, and the test-site name resolves to the server’s fixed address.

### Task 4 — Bring the Test Site and Wireless Access Online

**Objective:** Make the development service available to Joe’s devices.

1. Enable HTTP on the server. Use a simple page that identifies it as the Copper Kobold development site; a line of text is enough.
2. From the workstation, open `http://<server-IP>/koboldgaming.html` in the web browser, then open `http://dev.kobold.test/koboldgaming.html`. Confirm that both load the same page.
3. Configure the access point with your chosen SSID and WPA2-PSK security, using a compatible Packet Tracer model.
4. If including the smartphone, associate it with the wireless network and obtain its settings through DHCP. Verify its assigned address, mask, gateway and DNS server.
5. If included, use the smartphone to open `http://dev.kobold.test/koboldgaming.html` and verify access to the server’s HTTP page.
6. Save a Section 1A working copy.

**Checkpoint:** The workstation loads the correct page by IP address and name. If included, the smartphone associates successfully, receives valid DHCP settings and loads the page by name. Without a wireless client, wireless operation remains unverified.

**Stopping point:** Section 1A can be submitted for review before starting Section 1B.

## Section 1B — Connect Beyond the Spare Room

### Task 5 — Establish the Simulated ISP

**Objective:** Give the home office a working upstream path and identifiable external test destinations.

1. Configure and enable both ends of the edge-to-ISP link.
2. Create the two planned loopback interfaces on the ISP router.
3. Configure the edge router’s route for destinations outside its directly connected networks.
4. Verify reachability between the edge router and the ISP link address.
5. Verify that the edge router can reach both ISP loopbacks.

**Checkpoint:** The edge router has a valid upstream route and can reach both simulated external destinations.

### Task 6 — Provide Translated Access for Office Hosts

**Objective:** Allow private office hosts to reach the simulated external destinations through the edge router.

1. Configure NAT overload using the edge router’s ISP-facing address.
2. Limit the translation selection to the intended office address range.
3. Identify the correct inside and outside interfaces.
4. Generate traffic from the workstation and server to both ISP loopbacks.
5. Inspect the resulting translations and confirm that the private source addresses are translated as intended.
6. Repeat external reachability checks from the smartphone if it is included.

**Checkpoint:** Office hosts receive replies from both external destinations, and the edge router provides observable NAT evidence.

### Task 7 — Validate and Save the Completed Network

**Objective:** Demonstrate that external access works without disrupting the local network.

Run the following checks and retain the relevant results:

| Check | Test location | Expected result |
|---|---|---|
| Local host connectivity | Workstation and server | Both can reach each other and the office gateway. |
| DHCP | Workstation and optional smartphone; DHCP service | Clients receive valid, unique addresses and the planned mask, gateway and DNS settings. Lease evidence matches the clients; fixed addresses are excluded from allocation. |
| DNS | Workstation | `dev.kobold.test` resolves to the server’s fixed IPv4 address. |
| Switch management | Workstation | Switch-management address responds. |
| Development website | Workstation browser | Copper Kobold test page loads by IP address and at `http://dev.kobold.test/koboldgaming.html`. |
| Wireless service, if included | Smartphone | Associates successfully, receives DHCP settings and loads the test page by name. |
| External connectivity | Workstation, server and optional smartphone | Both ISP loopbacks respond. |
| Address translation | Edge router | Translations show the generated office traffic using the selected outside address. |
| Interface state | IOS devices | Required interfaces are operational; unused switch ports are administratively shut down. |
| Saved configuration | IOS devices and Packet Tracer file | Intended configurations are saved and the working file contains the completed build. |

Useful inspection commands include:

- `ipconfig /all` on the workstation — inspect the assigned address, mask, gateway and DNS server.
- `nslookup dev.kobold.test` on the workstation — verify the name resolves to the expected server address.
- `show ip dhcp binding` if using IOS DHCP, or the server’s DHCP lease view where available — inspect lease evidence. Packet Tracer Simulation-mode DHCP messages can provide evidence when a lease view is unavailable.
- `show ip interface brief` — check addressing and interface state.
- `show ip route` — inspect connected and configured routes.
- `show ip nat translations` — inspect translations while generating traffic.
- `show ip nat statistics` — inspect NAT activity and interface roles.
- `show interfaces status` — inspect switch-port state.
- `show startup-config` — confirm the saved configuration.

Save the final Packet Tracer file after completing these checks.

## Completion Check

- [x] The addressing plan is valid and includes an explained growth allowance.
- [x] Required equipment is connected and consistently named.
- [x] Baseline device-access configuration is present.
- [x] Clients receive correct DHCP settings, and fixed addresses are excluded from the lease pool.
- [x] Local DNS resolves `dev.kobold.test` to the server’s fixed address.
- [x] Wired connectivity and the development website work by IP address and name.
- [x] Wireless configuration is present; client testing is recorded as passed or not performed.
- [x] Required office hosts reach both ISP loopbacks.
- [x] NAT evidence supports the observed external connectivity.
- [x] Unused switch ports are shut down.
- [x] Configurations and the submitted Packet Tracer file are saved.
- [x] Tutor review has resolved outstanding findings.

## Submission and Review

Provide the saved working file’s path and the results of the required tests. A topology screenshot will also be needed for the accepted chapter record.

The tutor will inspect the saved network, compare it with this brief and review the behavioural evidence. Configuration inspection alone does not prove connectivity. Findings will come back as investigation pointers for you to work through.

The tutor maintains the [build record](build-record.md); you do not need to write a separate report.
