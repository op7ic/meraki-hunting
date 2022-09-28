##########################################################
# Author      : Jerzy 'Yuri' Kramarz (op7ic)             #
# Version     : 1.0                                      #
# Type        : Python                                   #
# Description : See README.md for details                #
# License     : See LICENSE for details                  #
########################################################## 

import csv
from datetime import datetime
import meraki
import os

# Instructions:
# Set APIKEY in environment variable MERAKI_DASHBOARD_API_KEY.
# Install meraki via 'pip install meraki' command

def select_org(dashboard):
    # Fetch and select the organization
    print('[+] Fetching organizations...')
    organizations = dashboard.organizations.getOrganizations()
    organizations.sort(key=lambda x: x['name'])
    counter = 0
    print('[+] Select organization to query:')
    for organization in organizations:
        orgName = organization['name']
        print(f'{counter} - {orgName}')
        counter+=1
    isDone = False
    while isDone == False:
        selected = input('[+] Select the organization ID you would like to query: ')
        try:
            if int(selected) in range(0,counter):
                isDone = True
            else:
                print('\tInvalid Organization Number\n')
        except:
            print('\tInvalid Organization Number\n')
    return(organizations[int(selected)]['id'], organizations[int(selected)]['name'])

os.makedirs('./logs/', exist_ok=True) 
dashboard = meraki.DashboardAPI(output_log=True, log_path="./logs/",log_file_prefix=os.path.basename(__file__), print_console=False)
selected_org, orgName = select_org(dashboard)

print("[+] Organization ID: %s " % (selected_org))

print("[+] Grabbing Network Device List")
devices = dashboard.organizations.getOrganizationDevicesAvailabilities(organizationId=selected_org)
networkIDs = []
for a in devices:
    if (a['status'] == 'online'):
        netID = a['network']['id']
        if netID not in networkIDs:
            networkIDs.append(netID)

print("[+] Dumping Cellular Firewall Rules")

with open('cellular-firewall-rules.csv', 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['network ID','firewall rule type','network name','timezone','policy', 'protocol', 'destCidr','destPort','srcCidr','srcPort','syslogEnabled','comment']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing cellular firewall rules for %s" % (network_meta['name']))
        try:
            cell_events = dashboard.appliance.getNetworkApplianceFirewallCellularFirewallRules(networkId=x)
            for rules in cell_events['rules']:
                writer.writerow([x,'CellularFirewallRules',network_meta['name'],network_meta['timeZone'],rules['policy'],rules['protocol'],rules['destCidr'],rules['destPort'],rules['srcCidr'],rules['srcPort'],rules['syslogEnabled'],rules['comment']])
        except:
            pass

print("[+] Dumping Inbound Firewall Rules")

with open('inbound-firewall-rules.csv', 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['network ID','firewall rule type','network name','timezone','policy', 'protocol', 'destCidr','destPort','srcCidr','srcPort','syslogEnabled','comment']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing inbound firewall rules for %s" % (network_meta['name']))
        try:
            inbound_events = dashboard.appliance.getNetworkApplianceFirewallInboundFirewallRules(networkId=x)
            for rules in inbound_events['rules']:
                writer.writerow([x,'InboundFirewallRules',network_meta['name'],network_meta['timeZone'],rules['policy'],rules['protocol'],rules['destCidr'],rules['destPort'],rules['srcCidr'],rules['srcPort'],rules['syslogEnabled'],rules['comment']])
        except:
            pass

print("[+] Dumping Layer 3 Firewall Rules")

with open('l3-firewall-rules.csv', 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['network ID','firewall rule type','network name','timezone','policy', 'protocol', 'destCidr','destPort','srcCidr','srcPort','syslogEnabled','comment']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing l3 firewall rules for %s" % (network_meta['name']))
        try:
            l3_events = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(networkId=x)
            for rules in l3_events['rules']:
                writer.writerow([x,'L3FirewallRules',network_meta['name'],network_meta['timeZone'],rules['policy'],rules['protocol'],rules['destCidr'],rules['destPort'],rules['srcCidr'],rules['srcPort'],rules['syslogEnabled'],rules['comment']])
        except:
            pass


print("[+] Dumping Layer 7 Firewall Rules")

with open('l7-firewall-rules.csv', 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['network ID','firewall rule type','network name','timezone','policy', 'type', 'value']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing l7 firewall rules for %s" % (network_meta['name']))
        try:
            l7_events = dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(networkId=x)
            for rules in l7_events['rules']:
                writer.writerow([x,'L7FirewallRules',network_meta['name'],network_meta['timeZone'],rules['policy'],rules['type'],rules['value']])
        except:
            pass

print("[+] Dumping Firewall Port Forwarding Rules")

with open('port-fw-firewall-rules.csv', 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['network ID','firewall rule type','network name','timezone','lanIp', 'allowedIps', 'protocol','publicPort','localPort','uplink','name']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing port forwarding firewall rules for %s" % (network_meta['name']))
        try:
            l7_events = dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(networkId=x)
            for rules in l7_events['rules']:
                writer.writerow([x,'portForwardingRules',network_meta['name'],network_meta['timeZone'],rules['lanIp'],rules['allowedIps'],rules['protocol'], rules['publicPort'], rules['localPort'] , rules['uplink'], rules['name']  ])
        except:
            pass

print("[+] Done. Happy hunting !")