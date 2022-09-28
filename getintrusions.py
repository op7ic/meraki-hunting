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

print("[+] Dumping IDS Intrusion Log")

with open('ids-intrusion-log.csv', 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['timestamp','network ID','network name','timezone','eventType','deviceMac','clientMac','srcIp','destIp','protocol','signature','ruleId','blocked','message']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing IDS intrusion log for %s" % (network_meta['name']))

        intrusion_events = dashboard.appliance.getNetworkApplianceSecurityEvents(networkId=x,timespan=2592000,total_pages=9999, perPage=1000)
        for event in intrusion_events:
            if event['eventType'] == 'IDS Alert':
                writer.writerow([event['ts'],x,network_meta['name'],network_meta['timeZone'],event['eventType'], 
                    event['deviceMac'],event['clientMac'],event['srcIp'],event['destIp'],event['protocol'],event['ruleId'],event['blocked'],event['message']
                    ])


with open('file-intrusion-log.csv', 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['timestamp','network ID','network name','timezone','eventType','clientName','clientMac',
    'clientIp','srcIp','destIp','protocol','uri','canonicalName','destinationPort','fileHash','fileType','disposition','action']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing file intrusion log for %s" % (network_meta['name']))
        intrusion_events = dashboard.appliance.getNetworkApplianceSecurityEvents(networkId=x,timespan=2592000,total_pages=9999, perPage=1000)
        for event in intrusion_events:
            if event['eventType'] == 'File Scanned':
                writer.writerow([event['ts'],x,network_meta['name'],network_meta['timeZone'],event['eventType'],event['clientName'],event['clientMac'],
                    event['clientIp'],event['srcIp'],event['destIp'],event['uri'],event['canonicalName'],event['destinationPort'],event['fileHash'],event['fileType'],event['disposition'],event['action']
                    ])

print("[+] Done. Happy hunting !")