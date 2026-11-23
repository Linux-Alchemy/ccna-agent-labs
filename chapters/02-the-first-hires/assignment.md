# Chapter 2 — The First Hires

[Chapter summary and field briefing](README.md#field-briefing) · [Build record](build-record.md)

Joe wants Marcus and Lena to be able to open the development build and the deployment build of *Banners of Ashvale* from home. Use the existing headquarters (HQ) internet exit for this version of the assignment.

## Objectives

- Connect two independently addressed home LANs to HQ using static routing.
- Make development and deployment available by name from all three developers’ desks.
- Give both home workstations access to the simulated internet through HQ using NAT overload.
- Demonstrate that Joe’s existing wired and wireless clients still have their Chapter 1 services.

## Equipment and Starting Conditions

Open the [accepted Spare Room lab](../01-the-spare-room/spare-room.pkt), tagged `chapter-1-v1`. Use **File → Save As** to create your Chapter 2 working file before making changes.

| Component | Starting state and role |
|---|---|
| HQ network | Retain RT01, SW01, Joe’s workstation, the DNS/development server, the access point and Joe’s test phone. |
| Simulated ISP | Retain the existing ISP router, WAN link and two external loopbacks. |
| Home offices | Add one router and one wired workstation at each home. A LAN switch is optional for a single workstation. |
| Site connections | Provide one routed point-to-point link from each home router to HQ. These links stand in for established site-to-site VPNs. Packet Tracer carries ordinary routed traffic on them. |
| Deployment server | Add one server to the HQ LAN. A distinct HTTP page represents the build ready for testing. |

Check available interfaces before cabling. Choose compatible modules or an HQ routing layout that can accommodate both new links as well as the existing LAN and ISP paths.

## Access and Required Parameters

| Item | Requirement |
|---|---|
| Existing addressing | Retain the HQ LAN `192.168.0.0/24`, gateway `.1`, switch management `.2`, DNS/development server `.3`, and ISP link `203.0.113.0/30`. |
| New addressing | Allocate a distinct, non-overlapping private IPv4 subnet to each home LAN and each transit link. Static settings are sufficient for home workstations. |
| HQ services | Keep HQ DHCP for Joe’s clients. Give deployment a fixed address excluded from DHCP. All three desks must use HQ DNS to resolve both sites. |
| Development | Retain `http://dev.kobold.test/koboldgaming.html`. |
| Deployment | Use `deploy.kobold.test` and record the page path if it is different from the site root. The page must identify itself as deployment. |
| External access | Use static/default routes and HQ NAT overload. External test destinations are `1.1.1.1` and `8.8.8.8`. The HQ ISP-facing address is `203.0.113.1`. |
| Device access | Retain existing HQ access settings. Use lab-only credentials on new routers. |

## Design Decisions

You choose the new subnet sizes and addresses, router models, interfaces, hostnames and route entries. Be ready to explain how HQ finds each home LAN on the return trip, and how the deployment server’s address stays available when a DHCP client requests a lease. The tutor records your reasoning.

## Part A — Connect the home offices

### Task 1 — Plan the expansion

**Objective.** Produce a layout you can cable and an address plan you can test.

1. Sketch the existing HQ LAN and ISP link. Label the subnets already in use and identify where the two new links can terminate at HQ.
2. Add Marcus’s and Lena’s workstations and home routers to the sketch. Label the port at each end of each planned link.
3. Choose four private subnets, one for each home LAN and one for each transit link. Check their address ranges against each other and the existing network.
4. Assign each new router interface an address and mask. For each workstation, record its address, mask, local gateway and HQ DNS address.
5. Choose a free address on the HQ LAN for deployment. Check it against the fixed addresses and active DHCP bindings before reserving it.
6. Follow a packet on your sketch from Marcus to the HQ server and back. Then follow one from Lena to the ISP loopback and back. Identify where routing decisions occur and where the external traffic will be translated.

**Checkpoint.** Every new segment has its own subnet, every link has a pair of available interfaces, and you can identify the next hop for each routed leg.

### Task 2 — Bring Marcus online

**Objective.** Establish the first working home-to-HQ connection.

1. Place Marcus’s router and workstation. Cable his LAN, then connect his router’s transit port to the planned HQ port.
2. Name the home router and set its lab access credentials. Address and enable its LAN interface.
3. Enter Marcus’s planned IP address, mask, gateway and DNS server on his workstation. Ping his gateway from the workstation.
4. Address and enable both ends of the Marcus–HQ transit link. From Marcus’s router, ping the peer address at HQ.
5. Set up Marcus’s route towards the HQ LAN. On the HQ side, provide a return route to Marcus’s LAN. Inspect the routing tables for both destinations.
6. From Marcus’s workstation, ping the development server at `192.168.0.3`. Resolve `dev.kobold.test` and check that the answer matches the address you pinged.
7. Open `http://dev.kobold.test/koboldgaming.html` in Marcus’s browser and confirm that Joe’s development page loads.

**Checkpoint.** Marcus can load Joe’s existing development page from home.

### Task 3 — Bring Lena online

**Objective.** Add the second home while keeping Marcus connected.

1. Place and cable Lena’s workstation and router using the ports in your plan. Connect her transit link to HQ.
2. Name her router, set its lab access credentials, and address and enable the LAN interface.
3. Apply Lena’s workstation settings. From her desk, ping her local gateway.
4. Address and enable both ends of Lena’s transit link. From her router, ping its HQ peer.
5. Provide Lena’s route to the HQ LAN and HQ’s return route to her LAN. Check that HQ can still route to Marcus’s subnet.
6. From Lena’s desk, ping `192.168.0.3`, resolve `dev.kobold.test` and open the development page by name.
7. Reopen the same URL from Marcus’s workstation. Save the IOS configurations and Chapter 2 file at this Part A checkpoint.

**Checkpoint.** Both developers can open the development page by name. This is a suitable stopping point for a partial review.

## Part B — Deliver the deployment site and internet access

### Task 4 — Publish a separate deployment build

**Objective.** Give the team a recognisable deployment page at a stable name.

1. Exclude the planned deployment address from the HQ DHCP pool before assigning it to the server.
2. Cable the deployment server to an available HQ switch port. Enable the port if it was shut down in Chapter 1.
3. Set the server’s fixed address, mask, HQ gateway and DNS server. From Joe’s workstation, ping its new address.
4. Enable HTTP and create a page that identifies the deployment build. From Joe’s browser, open it by IP address and record the page path.
5. On the existing HQ DNS server, add an A record for `deploy.kobold.test`. From Joe’s workstation, look up that name and compare the result with the address tested in step 3.
6. Open the deployment page by name from Joe’s desk using the same path. Open the development URL alongside it and confirm the pages are distinguishable.
7. From each home workstation, open both URLs and check which build each serves.

**Checkpoint.** Each desk can select either build by name and tell which one is open.

### Task 5 — Route home internet traffic through HQ

**Objective.** Let both hires use Joe’s existing ISP connection.

1. Inspect the route each home router would use for `1.1.1.1` and `8.8.8.8`. Configure the external path through its HQ peer where needed.
2. At HQ, verify the route towards the ISP and the return routes towards both home LANs.
3. On the HQ edge, identify where traffic from each home enters and where it leaves for the ISP. Apply the NAT inside and outside roles appropriate to those interfaces.
4. Extend the existing overload selection to include both home LANs as well as Joe’s LAN. Use the existing ISP-facing address for translation.
5. From Marcus’s workstation, ping both loopbacks. While the traffic is active, inspect the HQ NAT table and identify Marcus’s inside-local and inside-global addresses.
6. Generate the same traffic from Lena’s workstation. Find her translation and confirm that both homes share the HQ outside address.

**Checkpoint.** Both loopbacks reply at each home. For each home workstation, you can identify its private source address and the translated HQ address.

### Task 6 — Validate and save the expanded network

**Objective.** Demonstrate that the new capabilities and existing services work together.

1. At Marcus’s and Lena’s desks, verify the gateway and HQ server checks in the table. At HQ, identify the routes back to their LANs.
2. At each of the three desks, open the development and deployment URLs. Record which page appears for each name.
3. Check the home internet and NAT results against the table. Reuse Task 5 results if they describe the final configuration.
4. At Joe’s desk and on the phone, check their DHCP settings and open the development site. From Joe’s desk, also ping the office gateway and switch management address.
5. From each original HQ endpoint listed below, test both ISP destinations and verify its translation at the edge. Record the source, destination and result of each test.
6. Save the IOS configurations on changed devices, save the Chapter 2 file and capture the labelled topology for review.

| Check | Test location | Expected result |
|---|---|---|
| Home routes | Both home workstations and HQ router(s) | Each workstation reaches its gateway and HQ server. Route entries account for both return paths. |
| Both builds | Joe’s, Marcus’s and Lena’s workstations | Both names resolve to their respective HQ addresses. Each URL opens the intended page. |
| External path and NAT | Both home workstations, HQ edge | Both loopbacks reply from each home. Routing or a trace shows the HQ exit. Translations map each workstation to `203.0.113.1`. |
| HQ addressing and local service | Joe’s workstation and wireless phone | Each has a valid DHCP lease and HQ DNS. Both open the development site by name. Joe’s workstation can also reach the office gateway and switch management address. |
| Existing HQ internet service | Joe’s workstation, original development server and phone | Each reaches both ISP loopbacks. The HQ edge still translates their traffic. |

Useful checks include `ipconfig /all` at a workstation, `show ip route` on a router and `show ip nat translations` at the HQ edge while a client generates traffic. The Packet Tracer browser verifies that the named service serves the expected page.

**Checkpoint.** The test results identify each source, its destination and the observed result, and the saved lab is ready for review.

## Completion Check

- [ ] Both home LANs have distinct addressing and working routes to and from HQ.
- [ ] All three developers can open the development and deployment pages by name.
- [ ] Both homes reach both ISP loopbacks through HQ, with translation verified.
- [ ] The retained Chapter 1 client, service and external-access checks pass.
- [ ] IOS configurations, the Chapter 2 working file and the labelled topology are saved.
- [ ] Tutor review has resolved outstanding findings.

## Submission and Review

Send the saved file path, labelled topology capture and test results. Include the deployment URL and your addressing and routing choices. A short account of what you observed is sufficient. The tutor inspects the saved configuration, reviews your Packet Tracer results and maintains the [build record](build-record.md).
