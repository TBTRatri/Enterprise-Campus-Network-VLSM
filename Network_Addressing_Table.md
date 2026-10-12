# Enterprise Campus Network — IP Addressing & Gateway Table

This document outlines the IP scheme, subnet masks, default gateways, and dedicated servers allocated across all departments and link pools partitioned from the root `16.69.0.0/16` network.

---

## 1. Gateway & Server Allocation Table

| Device / Host Name | IP Address | Subnet Mask | Default Gateway | Function / Description |
| :--- | :--- | :--- | :--- | :--- |
| **CSE Gateway** | `16.69.0.1` | `255.255.255.0` | `N/A` | Default Gateway for CSE LAN (`/24`) |
| **BBS Gateway** | `16.69.1.1` | `255.255.255.0` | `N/A` | Default Gateway for BBS LAN (`/24`) |
| **MNS Gateway** | `16.69.2.1` | `255.255.255.0` | `N/A` | Default Gateway for MNS LAN (`/24`) |
| **BIL Gateway** | `16.69.3.1` | `255.255.255.128` | `N/A` | Default Gateway for BIL LAN (`/25`) |
| **EEE Gateway** | `16.69.3.129` | `255.255.255.128` | `N/A` | Default Gateway for EEE LAN (`/25`) |
| **LAW Gateway** | `16.69.4.1` | `255.255.255.192` | `N/A` | Default Gateway for LAW LAN (`/26`) |
| **CSE DNS Server** | `16.69.0.10` | `255.255.255.0` | `16.69.0.1` | Campus Primary DNS Server |
| **CSE Web Server** | `16.69.0.20` | `255.255.255.0` | `16.69.0.1` | Departmental Web Host |
| **MNS Web Server** | `16.69.2.20` | `255.255.255.0` | `16.69.2.1` | Departmental Web Host |
| **CSE Mail Server** | `16.69.0.30` | `255.255.255.0` | `16.69.0.1` | Departmental Mail Host |
| **BBS Mail Server** | `16.69.1.30` | `255.255.255.0` | `16.69.1.1` | Departmental Mail Host |
| **MNS Mail Server** | `16.69.2.30` | `255.255.255.0` | `16.69.2.1` | Departmental Mail Host |
| **BIL Mail Server** | `16.69.3.30` | `255.255.255.128` | `16.69.3.1` | Departmental Mail Host |
| **EEE Mail Server** | `16.69.3.150` | `255.255.255.128` | `16.69.3.129` | Departmental Mail Host |
| **LAW Mail Server** | `16.69.4.30` | `255.255.255.192` | `16.69.4.1` | Departmental Mail Host |

---

## 2. Point-to-Point WAN Links & Backbone Pool

| WAN Segment | Subnet Allocated | CIDR | Usable Subnet Range | Router Interfaces |
| :--- | :--- | :--- | :--- | :--- |
| **Core Switch Backbone** | `16.69.4.64` | `/29` | `16.69.4.65 - 16.69.4.70` | CSE (`g0/0`), EEE (`g0/0`), BBS (`g0/0`) |
| **CSE – MNS WAN** | `16.69.4.72` | `/30` | `16.69.4.73 - 16.69.4.74` | `R-CSE s0/0/0` <-> `R-MNS s0/0/0` |
| **CSE – LAW WAN** | `16.69.4.76` | `/30` | `16.69.4.77 - 16.69.4.78` | `R-CSE s0/0/1` <-> `R-LAW s0/0/0` |
| **CSE – BIL WAN** | `16.69.4.80` | `/30` | `16.69.4.81 - 16.69.4.82` | `R-CSE s0/1/0` <-> `R-BIL s0/0/0` |
| **LAW – BIL Redundant Link** | `16.69.4.84` | `/30` | `16.69.4.85 - 16.69.4.86` | `R-LAW s0/0/1` <-> `R-BIL s0/0/1` |
