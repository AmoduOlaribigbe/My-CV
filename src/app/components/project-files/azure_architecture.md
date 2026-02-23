# Azure Secure Cloud Deployment Architecture
# Enterprise Web Application with Security Best Practices

## Overview
This document outlines a secure Azure cloud deployment for an enterprise web application with comprehensive security controls, monitoring, and backup.

---

## Architecture Diagram

```
                         Internet
                            |
                    [Azure Firewall]
                            |
                    [Application Gateway]
                      (WAF Enabled)
                            |
              ______________|______________
             |                             |
      [Load Balancer]              [Azure Bastion]
             |                             |
    _________|_________           [Management Subnet]
   |                   |                   |
[Web Tier VMs]   [Web Tier VMs]    [Jump Box VM]
   VMSS-1           VMSS-2
      |                   |
      |___________________|
                |
          [Internal LB]
                |
         [App Tier VMs]
           (Private)
                |
         [Azure SQL DB]
      (Private Endpoint)
                |
       [Azure Key Vault]
                |
    [Storage Account (Backup)]
                |
      [Log Analytics/Sentinel]
```

---

## Resource Group Structure

### Primary Resource Group: `enterprise-app-prod-rg`
- Location: East US
- Environment: Production
- Department: IT Infrastructure

---

## Network Configuration

### Virtual Network (VNet)
```
Name: enterprise-vnet
Address Space: 10.0.0.0/16

Subnets:
├── web-subnet (10.0.1.0/24)          - Web tier VMs
├── app-subnet (10.0.2.0/24)          - Application tier VMs
├── data-subnet (10.0.3.0/24)         - Database private endpoints
├── management-subnet (10.0.4.0/24)   - Bastion and jump box
├── AzureBastionSubnet (10.0.5.0/27)  - Azure Bastion (fixed name)
└── GatewaySubnet (10.0.6.0/27)       - VPN Gateway
```

### Network Security Groups (NSGs)

#### Web-Tier NSG
```
Name: web-nsg

Inbound Rules:
Priority | Name              | Port  | Protocol | Source      | Destination | Action
100      | Allow-HTTPS       | 443   | TCP      | Internet    | *           | Allow
110      | Allow-HTTP        | 80    | TCP      | Internet    | *           | Allow
120      | Allow-SSH         | 22    | TCP      | 10.0.4.0/24 | *           | Allow
200      | Deny-All-Inbound  | *     | *        | *           | *           | Deny

Outbound Rules:
Priority | Name                | Port  | Protocol | Source | Destination | Action
100      | Allow-App-Tier      | 8080  | TCP      | *      | 10.0.2.0/24 | Allow
110      | Allow-Internet      | *     | *        | *      | Internet    | Allow
200      | Deny-All-Outbound   | *     | *        | *      | *           | Deny
```

#### App-Tier NSG
```
Name: app-nsg

Inbound Rules:
Priority | Name              | Port  | Protocol | Source      | Destination | Action
100      | Allow-From-Web    | 8080  | TCP      | 10.0.1.0/24 | *           | Allow
110      | Allow-SSH         | 22    | TCP      | 10.0.4.0/24 | *           | Allow
200      | Deny-All-Inbound  | *     | *        | *           | *           | Deny

Outbound Rules:
Priority | Name                | Port  | Protocol | Source | Destination | Action
100      | Allow-SQL           | 1433  | TCP      | *      | 10.0.3.0/24 | Allow
110      | Allow-KeyVault      | 443   | TCP      | *      | AzureCloud  | Allow
200      | Deny-All-Outbound   | *     | *        | *      | *           | Deny
```

---

## Compute Resources

### Web Tier - Virtual Machine Scale Set (VMSS)
```
Name: web-vmss
VM Size: Standard_D2s_v3 (2 vCPU, 8GB RAM)
OS: Ubuntu 20.04 LTS
Min Instances: 2
Max Instances: 10
Autoscale Rules:
  - CPU > 75% for 5 min → Scale out by 1 instance
  - CPU < 25% for 10 min → Scale in by 1 instance

Security:
  - Managed Identity enabled
  - Disk encryption enabled
  - Boot diagnostics enabled
  - Automatic OS patching enabled
```

### App Tier - Virtual Machines
```
Name: app-vm-{1,2}
VM Size: Standard_D4s_v3 (4 vCPU, 16GB RAM)
OS: Ubuntu 20.04 LTS
Availability: Availability Set (2 fault domains, 5 update domains)

Security:
  - Managed Identity enabled
  - Disk encryption enabled
  - Azure Backup enabled (daily)
```

---

## Database

### Azure SQL Database
```
Name: enterprise-sql-db
Tier: Standard S2 (50 DTUs)
Pricing: $75/month

Security Configuration:
├── Private Endpoint enabled (no public access)
├── Transparent Data Encryption (TDE) enabled
├── Advanced Data Security enabled
├── Auditing enabled (Log Analytics)
├── Threat Detection enabled
└── Firewall: Deny all public access

Backup:
├── Automated backups: 7-day retention
├── Long-term retention: Monthly for 12 months
└── Geo-redundant storage enabled
```

---

## Security Services

### Azure Key Vault
```
Name: enterprise-keyvault
Tier: Premium (HSM-backed keys)

Stored Secrets:
├── SQL-Connection-String
├── Storage-Account-Key
├── API-Keys
└── SSL-Certificates

Access Policies:
├── Web VMSS Managed Identity: Get, List secrets
├── App VMs Managed Identity: Get, List secrets
└── Admin Group: Full permissions

Security:
├── Soft delete enabled (90 days)
├── Purge protection enabled
├── Private endpoint enabled
└── Network access: Selected networks only
```

### Azure Bastion
```
Name: enterprise-bastion
Tier: Standard
Purpose: Secure RDP/SSH access without public IPs

Configuration:
├── Dedicated subnet: AzureBastionSubnet
├── Public IP: Static, Standard SKU
├── Native client support enabled
└── IP-based connection enabled
```

### Application Gateway (WAF)
```
Name: enterprise-appgw
Tier: WAF V2
SKU: Standard

WAF Configuration:
├── Mode: Prevention
├── Rule Set: OWASP 3.2
├── Custom rules enabled
└── Bot protection enabled

Backend Pools:
└── Web-VMSS (automatic discovery)

Health Probe:
├── Protocol: HTTPS
├── Path: /health
└── Interval: 30 seconds
```

---

## Monitoring & Logging

### Log Analytics Workspace
```
Name: enterprise-logs
Retention: 90 days

Data Sources:
├── VM Insights (all VMs)
├── NSG Flow Logs
├── SQL Audit Logs
├── Key Vault Audit Logs
└── Activity Logs
```

### Azure Monitor
```
Alerts Configured:
├── VM CPU > 80% for 10 minutes
├── SQL DTU > 80% for 5 minutes
├── Storage > 90% capacity
├── Failed login attempts > 5
└── NSG rule modifications

Action Groups:
├── Email: security-team@enterprise.com
├── SMS: +1-XXX-XXX-XXXX
└── Webhook: Incident management system
```

### Azure Sentinel
```
Name: enterprise-sentinel
Data Connectors:
├── Azure Activity
├── Azure SQL
├── Azure Firewall
└── Office 365

Analytics Rules:
├── Suspicious login activity
├── Privilege escalation attempts
├── Data exfiltration detection
└── Brute force attacks
```

---

## Backup & Disaster Recovery

### Azure Backup
```
Recovery Services Vault: enterprise-backup-vault

Backup Policies:
Web VMs:
  ├── Frequency: Daily at 2:00 AM UTC
  ├── Retention: 30 days daily, 12 weeks weekly
  └── Instant restore: 5 days

App VMs:
  ├── Frequency: Daily at 3:00 AM UTC
  ├── Retention: 30 days daily, 12 weeks weekly, 12 months monthly
  └── Instant restore: 5 days

SQL Database:
  ├── Point-in-time restore: 7 days
  ├── Long-term retention: Monthly for 12 months
  └── Geo-redundant: Enabled
```

### Azure Site Recovery
```
Target Region: West US (DR site)
Replication:
├── App VMs: Continuous replication
├── SQL Database: Auto-failover group
└── RTO: 2 hours, RPO: 15 minutes
```

---

## Cost Optimization

### Monthly Cost Estimate

| Resource | Configuration | Est. Monthly Cost |
|----------|--------------|-------------------|
| VMs (Web VMSS) | 2x D2s_v3 | $140 |
| VMs (App Tier) | 2x D4s_v3 | $280 |
| Azure SQL DB | Standard S2 | $75 |
| Application Gateway | WAF V2 | $250 |
| Azure Bastion | Standard | $140 |
| Load Balancer | Standard | $20 |
| Storage Account | 500GB | $10 |
| Key Vault | Premium | $5 |
| Log Analytics | 10GB/day | $150 |
| Azure Backup | 500GB | $50 |
| **Total** | | **~$1,120/month** |

### Cost Savings:
- Reserved Instances: 40% savings on VMs (~$168/month savings)
- Auto-shutdown non-prod VMs: 70% savings on dev/test
- Right-sizing: Continuous monitoring and adjustment

---

## Deployment Scripts

### Azure CLI - Resource Group & VNet
```bash
#!/bin/bash

# Variables
RG_NAME="enterprise-app-prod-rg"
LOCATION="eastus"
VNET_NAME="enterprise-vnet"

# Create Resource Group
az group create --name $RG_NAME --location $LOCATION

# Create Virtual Network
az network vnet create \
  --resource-group $RG_NAME \
  --name $VNET_NAME \
  --address-prefix 10.0.0.0/16 \
  --subnet-name web-subnet \
  --subnet-prefix 10.0.1.0/24

# Create additional subnets
az network vnet subnet create \
  --resource-group $RG_NAME \
  --vnet-name $VNET_NAME \
  --name app-subnet \
  --address-prefix 10.0.2.0/24

az network vnet subnet create \
  --resource-group $RG_NAME \
  --vnet-name $VNET_NAME \
  --name data-subnet \
  --address-prefix 10.0.3.0/24
```

### ARM Template - NSG Configuration
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Network/networkSecurityGroups",
      "apiVersion": "2021-02-01",
      "name": "web-nsg",
      "location": "[resourceGroup().location]",
      "properties": {
        "securityRules": [
          {
            "name": "Allow-HTTPS",
            "properties": {
              "priority": 100,
              "direction": "Inbound",
              "access": "Allow",
              "protocol": "Tcp",
              "sourcePortRange": "*",
              "destinationPortRange": "443",
              "sourceAddressPrefix": "Internet",
              "destinationAddressPrefix": "*"
            }
          }
        ]
      }
    }
  ]
}
```

---

## Security Compliance

### Compliance Standards
- [ ] CIS Azure Foundations Benchmark
- [ ] NIST Cybersecurity Framework
- [ ] ISO 27001
- [ ] GDPR (if applicable)

### Security Checklist
- [x] No public IPs on VMs (Bastion only)
- [x] NSGs on all subnets
- [x] Private endpoints for PaaS services
- [x] Encryption at rest (TDE, disk encryption)
- [x] Encryption in transit (TLS 1.2+)
- [x] Managed identities (no hardcoded credentials)
- [x] Key Vault for secrets management
- [x] WAF enabled with OWASP rules
- [x] DDoS Protection Standard
- [x] Monitoring and alerting configured
- [x] Backup and DR tested
- [x] RBAC properly configured
- [x] Azure Policy enforced
- [x] Audit logging enabled

---

## Maintenance & Operations

### Patching Schedule
- **OS Updates**: Automated monthly (2nd Saturday, 2:00 AM)
- **Application Updates**: Monthly maintenance window
- **SQL Updates**: Automated (Microsoft managed)

### Backup Testing
- **Monthly**: Restore test of one VM
- **Quarterly**: Full DR drill with failover
- **Annually**: Complete disaster recovery simulation

---

**Architecture Design by: Olaribigbe Amodu**  
**Role: Azure Solutions Architect**  
**Date: February 2026**  
**Version: 1.0**
