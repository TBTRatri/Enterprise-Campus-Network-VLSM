import ipaddress
import os
import streamlit as st

st.set_page_config(
    page_title="Enterprise Campus Network & VLSM Explorer",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Enterprise Campus Network Architecture & VLSM Explorer")
st.markdown(
    "Interactive topology breakdown, Cisco IOS device configuration viewer, "
    "live **VLSM Subnet Allocation Engine**, and dynamic simulation playback."
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🎥 Simulation Walkthrough",
    "🧮 Interactive VLSM Engine",
    "🏢 VLAN & Campus Topology",
    "⚙️ Cisco IOS Config Viewer",
])

with tab1:
  st.subheader("🎥 Cisco Packet Tracer Dynamic Simulation")
  st.markdown(
      "Live packet flow tracing, ICMP ping testing, DHCP lease distribution, "
      "and OSPF routing convergence across the enterprise campus topology."
  )

  # Check for supported media files in repository root
  media_found = False

  # 1. Check for standard video formats
  for vfile in [
      "simulation.mp4",
      "demo.mp4",
      "packet_simulation.mp4",
      "simulation.webm",
      "demo.mov",
  ]:
    if os.path.exists(vfile):
      with open(vfile, "rb") as f:
        st.video(f.read())
      media_found = True
      break

  # 2. Check for animated GIF
  if not media_found:
    for gfile in ["simulation.gif", "demo.gif", "packet_simulation.gif"]:
      if os.path.exists(gfile):
        st.image(
            gfile,
            caption="Cisco Packet Tracer Dynamic Simulation (Animated Loop)",
            use_container_width=True,
        )
        media_found = True
        break

  # 3. Check for static PNG capture fallback
  if not media_found:
    for ifile in [
        "packet_simulation.png",
        "topology.png",
        "simulation.png",
        "demo.png",
    ]:
      if os.path.exists(ifile):
        st.image(
            ifile,
            caption="Cisco Packet Tracer Architecture & Simulation Snapshot",
            use_container_width=True,
        )
        media_found = True
        break

  # External stream or YouTube link fallback
  st.divider()
  external_video = st.text_input(
      "Stream external video walkthrough (YouTube / Vimeo / Direct URL):",
      placeholder="https://www.youtube.com/watch?v=...",
  )
  if external_video:
    st.video(external_video)
  elif not media_found:
    st.info(
        "Upload your video recording (`simulation.mp4`), an animated GIF (`simulation.gif`), "
        "or paste an external YouTube link above to activate dynamic playback."
    )

with tab2:
  st.subheader("Dynamic VLSM Subnet Calculator")
  st.write(
      "Simulate hierarchical campus network address allocations from a root CIDR block."
  )

  col1, col2 = st.columns([1, 2])

  with col1:
    base_network = st.text_input(
        "Major Network Block (CIDR):", value="192.168.0.0/22"
    )
    st.markdown("**Department Host Requirements:**")
    h_faculty = st.number_input(
        "Faculty & Academics VLAN", min_value=2, max_value=500, value=250
    )
    h_student = st.number_input(
        "Student Labs VLAN", min_value=2, max_value=500, value=120
    )
    h_admin = st.number_input(
        "Administration VLAN", min_value=2, max_value=250, value=60
    )
    h_server = st.number_input(
        "Data Center / Server Farm", min_value=2, max_value=100, value=25
    )
    h_wan = st.number_input(
        "Core-to-Edge WAN Links (PtP)", min_value=2, max_value=10, value=2
    )

  with col2:
    try:
      net = ipaddress.IPv4Network(base_network, strict=False)
      st.success(
          f"Base Address: {net.network_address} | Mask: {net.netmask} | Total"
          f" IPs: {net.num_addresses}"
      )

      subnets_req = [
          ("Faculty & Academics", h_faculty, 10),
          ("Student Labs", h_student, 20),
          ("Administration", h_admin, 30),
          ("Server Farm", h_server, 40),
          ("Core WAN Link", h_wan, 99),
      ]
      # Order descending for optimal VLSM allocation
      subnets_req.sort(key=lambda x: x[1], reverse=True)

      results = []
      current_ip = int(net.network_address)

      for name, hosts, vlan_id in subnets_req:
        needed = hosts + 2  # Network + Broadcast
        prefix = 32 - (needed - 1).bit_length()
        sub_net = ipaddress.IPv4Network(
            f"{ipaddress.IPv4Address(current_ip)}/{prefix}"
        )
        results.append({
            "VLAN": f"VLAN {vlan_id}",
            "Segment Name": name,
            "Hosts Req": hosts,
            "Prefix": f"/{prefix}",
            "Subnet Mask": str(sub_net.netmask),
            "Network Address": str(sub_net.network_address),
            "Usable Range": (
                f"{sub_net.network_address + 1} -"
                f" {sub_net.broadcast_address - 1}"
            ),
            "Broadcast": str(sub_net.broadcast_address),
        })
        current_ip += sub_net.num_addresses

      st.dataframe(results, use_container_width=True)
    except Exception as e:
      st.error(f"Invalid Network Allocation: {str(e)}")

with tab3:
  st.subheader("Enterprise Campus Network Topology")
  st.markdown("""
  - **Core Layer:** High-speed redundant multi-layer switches running **OSPF Area 0** routing.
  - **Distribution Layer:** Redundant gateway routers managing **Inter-VLAN Routing (Router-on-a-Stick)** and DHCP relay agents.
  - **Access Layer:** End-user edge switches with port security and isolated 802.1Q trunk links.
  """)

  st.table([
      {
          "VLAN ID": 10,
          "Name": "Faculty_Staff",
          "Subnet": "192.168.0.0/24",
          "Gateway": "192.168.0.1",
      },
      {
          "VLAN ID": 20,
          "Name": "Student_Labs",
          "Subnet": "192.168.1.0/25",
          "Gateway": "192.168.1.1",
      },
      {
          "VLAN ID": 30,
          "Name": "Administration",
          "Subnet": "192.168.1.128/26",
          "Gateway": "192.168.1.129",
      },
      {
          "VLAN ID": 40,
          "Name": "Server_Farm",
          "Subnet": "192.168.1.192/27",
          "Gateway": "192.168.1.193",
      },
      {
          "VLAN ID": 99,
          "Name": "WAN_Link",
          "Subnet": "192.168.1.224/30",
          "Gateway": "192.168.1.225",
      },
  ])

with tab4:
  st.subheader("Cisco IOS Production Configurations")
  device = st.selectbox(
      "Select Device Configuration:",
      ["Core-Router-R1", "Distribution-SW1", "Edge-Switch-SW2"],
  )

  if device == "Core-Router-R1":
    st.code(
        """! Router-on-a-Stick & OSPF Routing Configuration
interface GigabitEthernet0/0/0.10
 encapsulation dot1Q 10
 ip address 192.168.0.1 255.255.255.0
!
interface GigabitEthernet0/0/0.20
 encapsulation dot1Q 20
 ip address 192.168.1.1 255.255.255.128
!
router ospf 1
 router-id 1.1.1.1
 network 192.168.0.0 0.0.3.255 area 0
!""",
        language="bash",
    )
  elif device == "Distribution-SW1":
    st.code(
        """! DHCP Pool Setup & SVI
ip dhcp excluded-address 192.168.0.1 192.168.0.10
ip dhcp pool FACULTY_POOL
 network 192.168.0.0 255.255.255.0
 default-router 192.168.0.1
 dns-server 8.8.8.8
!
interface Vlan10
 ip address 192.168.0.2 255.255.255.0
!""",
        language="bash",
    )
  else:
    st.code(
        """! 802.1Q Trunking & Port Security
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40
!
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 20
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation restrict
!""",
        language="bash",
    )
