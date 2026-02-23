# Multi-VLAN Enterprise Network Configuration
# Cisco Router Configuration for VLAN Segmentation

## Network Design

### VLANs:
- VLAN 10: HR Department (192.168.10.0/24)
- VLAN 20: Finance Department (192.168.20.0/24)
- VLAN 30: IT Department (192.168.30.0/24)
- VLAN 40: Guest Network (192.168.40.0/24)

### Security Considerations:
- Inter-VLAN routing controlled
- Guest network isolated
- ACLs prevent unauthorized access between departments

---

## Router Configuration

### Router Hostname and Basic Config
```
Router> enable
Router# configure terminal
Router(config)# hostname EnterpriseCoreRouter
EnterpriseCoreRouter(config)# enable secret StrongPassword123!
EnterpriseCoreRouter(config)# service password-encryption
```

### Sub-Interfaces for Router-on-a-Stick
```
EnterpriseCoreRouter(config)# interface g0/0
EnterpriseCoreRouter(config-if)# no shutdown
EnterpriseCoreRouter(config-if)# exit

! VLAN 10 - HR
EnterpriseCoreRouter(config)# interface g0/0.10
EnterpriseCoreRouter(config-subif)# encapsulation dot1Q 10
EnterpriseCoreRouter(config-subif)# ip address 192.168.10.1 255.255.255.0
EnterpriseCoreRouter(config-subif)# description HR-Department
EnterpriseCoreRouter(config-subif)# exit

! VLAN 20 - Finance
EnterpriseCoreRouter(config)# interface g0/0.20
EnterpriseCoreRouter(config-subif)# encapsulation dot1Q 20
EnterpriseCoreRouter(config-subif)# ip address 192.168.20.1 255.255.255.0
EnterpriseCoreRouter(config-subif)# description Finance-Department
EnterpriseCoreRouter(config-subif)# exit

! VLAN 30 - IT
EnterpriseCoreRouter(config)# interface g0/0.30
EnterpriseCoreRouter(config-subif)# encapsulation dot1Q 30
EnterpriseCoreRouter(config-subif)# ip address 192.168.30.1 255.255.255.0
EnterpriseCoreRouter(config-subif)# description IT-Department
EnterpriseCoreRouter(config-subif)# exit

! VLAN 40 - Guest
EnterpriseCoreRouter(config)# interface g0/0.40
EnterpriseCoreRouter(config-subif)# encapsulation dot1Q 40
EnterpriseCoreRouter(config-subif)# ip address 192.168.40.1 255.255.255.0
EnterpriseCoreRouter(config-subif)# description Guest-Network
EnterpriseCoreRouter(config-subif)# exit
```

### DHCP Configuration per VLAN
```
! DHCP Pool for HR (VLAN 10)
EnterpriseCoreRouter(config)# ip dhcp pool HR-POOL
EnterpriseCoreRouter(dhcp-config)# network 192.168.10.0 255.255.255.0
EnterpriseCoreRouter(dhcp-config)# default-router 192.168.10.1
EnterpriseCoreRouter(dhcp-config)# dns-server 8.8.8.8 8.8.4.4
EnterpriseCoreRouter(dhcp-config)# domain-name hr.enterprise.local
EnterpriseCoreRouter(dhcp-config)# exit

! DHCP Pool for Finance (VLAN 20)
EnterpriseCoreRouter(config)# ip dhcp pool FINANCE-POOL
EnterpriseCoreRouter(dhcp-config)# network 192.168.20.0 255.255.255.0
EnterpriseCoreRouter(dhcp-config)# default-router 192.168.20.1
EnterpriseCoreRouter(dhcp-config)# dns-server 8.8.8.8 8.8.4.4
EnterpriseCoreRouter(dhcp-config)# domain-name finance.enterprise.local
EnterpriseCoreRouter(dhcp-config)# exit

! DHCP Pool for IT (VLAN 30)
EnterpriseCoreRouter(config)# ip dhcp pool IT-POOL
EnterpriseCoreRouter(dhcp-config)# network 192.168.30.0 255.255.255.0
EnterpriseCoreRouter(dhcp-config)# default-router 192.168.30.1
EnterpriseCoreRouter(dhcp-config)# dns-server 8.8.8.8 8.8.4.4
EnterpriseCoreRouter(dhcp-config)# domain-name it.enterprise.local
EnterpriseCoreRouter(dhcp-config)# exit

! DHCP Pool for Guest (VLAN 40)
EnterpriseCoreRouter(config)# ip dhcp pool GUEST-POOL
EnterpriseCoreRouter(dhcp-config)# network 192.168.40.0 255.255.255.0
EnterpriseCoreRouter(dhcp-config)# default-router 192.168.40.1
EnterpriseCoreRouter(dhcp-config)# dns-server 8.8.8.8
EnterpriseCoreRouter(dhcp-config)# domain-name guest.enterprise.local
EnterpriseCoreRouter(dhcp-config)# lease 0 8 0
EnterpriseCoreRouter(dhcp-config)# exit

! Exclude gateway addresses from DHCP
EnterpriseCoreRouter(config)# ip dhcp excluded-address 192.168.10.1
EnterpriseCoreRouter(config)# ip dhcp excluded-address 192.168.20.1
EnterpriseCoreRouter(config)# ip dhcp excluded-address 192.168.30.1
EnterpriseCoreRouter(config)# ip dhcp excluded-address 192.168.40.1
```

### Access Control Lists (ACLs) for Security
```
! ACL to block Guest VLAN from accessing internal networks
EnterpriseCoreRouter(config)# access-list 100 deny ip 192.168.40.0 0.0.0.255 192.168.10.0 0.0.0.255
EnterpriseCoreRouter(config)# access-list 100 deny ip 192.168.40.0 0.0.0.255 192.168.20.0 0.0.0.255
EnterpriseCoreRouter(config)# access-list 100 deny ip 192.168.40.0 0.0.0.255 192.168.30.0 0.0.0.255
EnterpriseCoreRouter(config)# access-list 100 permit ip any any

! Apply ACL to Guest VLAN interface
EnterpriseCoreRouter(config)# interface g0/0.40
EnterpriseCoreRouter(config-subif)# ip access-group 100 in
EnterpriseCoreRouter(config-subif)# exit

! ACL to restrict HR and Finance communication
EnterpriseCoreRouter(config)# access-list 110 deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
EnterpriseCoreRouter(config)# access-list 110 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
EnterpriseCoreRouter(config)# access-list 110 permit ip any any

EnterpriseCoreRouter(config)# interface g0/0.10
EnterpriseCoreRouter(config-subif)# ip access-group 110 in
EnterpriseCoreRouter(config-subif)# exit
```

---

## Switch Configuration

### Basic Switch Setup
```
Switch> enable
Switch# configure terminal
Switch(config)# hostname EnterpriseSwitch
EnterpriseSwitch(config)# enable secret StrongPassword123!
```

### VLAN Creation
```
EnterpriseSwitch(config)# vlan 10
EnterpriseSwitch(config-vlan)# name HR-Department
EnterpriseSwitch(config-vlan)# exit

EnterpriseSwitch(config)# vlan 20
EnterpriseSwitch(config-vlan)# name Finance-Department
EnterpriseSwitch(config-vlan)# exit

EnterpriseSwitch(config)# vlan 30
EnterpriseSwitch(config-vlan)# name IT-Department
EnterpriseSwitch(config-vlan)# exit

EnterpriseSwitch(config)# vlan 40
EnterpriseSwitch(config-vlan)# name Guest-Network
EnterpriseSwitch(config-vlan)# exit
```

### Access Ports Configuration
```
! HR Department Ports (Example: F0/1-8)
EnterpriseSwitch(config)# interface range f0/1-8
EnterpriseSwitch(config-if-range)# switchport mode access
EnterpriseSwitch(config-if-range)# switchport access vlan 10
EnterpriseSwitch(config-if-range)# spanning-tree portfast
EnterpriseSwitch(config-if-range)# exit

! Finance Department Ports (F0/9-16)
EnterpriseSwitch(config)# interface range f0/9-16
EnterpriseSwitch(config-if-range)# switchport mode access
EnterpriseSwitch(config-if-range)# switchport access vlan 20
EnterpriseSwitch(config-if-range)# spanning-tree portfast
EnterpriseSwitch(config-if-range)# exit

! IT Department Ports (F0/17-20)
EnterpriseSwitch(config)# interface range f0/17-20
EnterpriseSwitch(config-if-range)# switchport mode access
EnterpriseSwitch(config-if-range)# switchport access vlan 30
EnterpriseSwitch(config-if-range)# spanning-tree portfast
EnterpriseSwitch(config-if-range)# exit

! Guest Network Ports (F0/21-24)
EnterpriseSwitch(config)# interface range f0/21-24
EnterpriseSwitch(config-if-range)# switchport mode access
EnterpriseSwitch(config-if-range)# switchport access vlan 40
EnterpriseSwitch(config-if-range)# spanning-tree portfast
EnterpriseSwitch(config-if-range)# exit
```

### Trunk Port to Router
```
EnterpriseSwitch(config)# interface g0/1
EnterpriseSwitch(config-if)# switchport mode trunk
EnterpriseSwitch(config-if)# switchport trunk allowed vlan 10,20,30,40
EnterpriseSwitch(config-if)# exit
```

### Port Security (Optional but Recommended)
```
! Example: Secure HR port
EnterpriseSwitch(config)# interface f0/1
EnterpriseSwitch(config-if)# switchport port-security
EnterpriseSwitch(config-if)# switchport port-security maximum 2
EnterpriseSwitch(config-if)# switchport port-security violation restrict
EnterpriseSwitch(config-if)# switchport port-security mac-address sticky
EnterpriseSwitch(config-if)# exit
```

---

## Verification Commands

### Router Verification
```
! Show interface status
EnterpriseCoreRouter# show ip interface brief

! Show sub-interfaces
EnterpriseCoreRouter# show interfaces trunk

! Show routing table
EnterpriseCoreRouter# show ip route

! Show DHCP bindings
EnterpriseCoreRouter# show ip dhcp binding

! Show ACLs
EnterpriseCoreRouter# show access-lists
```

### Switch Verification
```
! Show VLAN configuration
EnterpriseSwitch# show vlan brief

! Show trunk status
EnterpriseSwitch# show interfaces trunk

! Show port status
EnterpriseSwitch# show interfaces status

! Show port security
EnterpriseSwitch# show port-security
```

### Connectivity Testing
```
! From HR PC (VLAN 10)
PC> ipconfig
PC> ping 192.168.10.1
PC> ping 192.168.30.1

! From Guest PC (VLAN 40) - Should NOT reach internal VLANs
PC> ping 192.168.10.1  (Should FAIL)
PC> ping 8.8.8.8       (Should SUCCEED - Internet access)
```

---

## Network Topology

```
                    Internet
                        |
                 [ISP Router]
                        |
              [EnterpriseCoreRouter]
                        |
                   G0/0 (Trunk)
                        |
             [EnterpriseSwitch]
          __________|__________
         |          |          |          |
     VLAN 10    VLAN 20    VLAN 30    VLAN 40
       (HR)    (Finance)    (IT)      (Guest)
     F0/1-8    F0/9-16   F0/17-20   F0/21-24
```

---

## Security Benefits

1. **Network Segmentation**: Each department isolated in separate broadcast domain
2. **Access Control**: ACLs prevent unauthorized inter-VLAN communication
3. **Guest Isolation**: Guest network cannot access internal resources
4. **Port Security**: Prevents MAC flooding and unauthorized device connections
5. **Scalability**: Easy to add new VLANs and departments

---

## Testing Checklist

- [ ] All VLANs created on switch
- [ ] Trunk port configured between switch and router
- [ ] Sub-interfaces configured on router
- [ ] DHCP pools working for each VLAN
- [ ] Devices in same VLAN can communicate
- [ ] Devices in different VLANs can/cannot communicate (as per ACL)
- [ ] Guest VLAN isolated from internal networks
- [ ] Guest VLAN has Internet access
- [ ] Port security preventing unauthorized MAC addresses

---

**Configuration by: Olaribigbe Amodu**  
**Purpose: Enterprise Network Security Lab**  
**Date: February 2026**
