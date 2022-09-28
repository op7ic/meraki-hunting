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

print("[+] Dumping Login Events")
unique_client = {}
now = datetime.now()
timestampStr = now.strftime("%d-%m-%Y-%s")

with open('login-overview-%s.csv' % (timestampStr), 'w', newline='', encoding='utf-8') as f:
    csv_header =  ['network ID','network name','timezone','login', 'ssid', 'loginAt','gatewayDeviceMac','clientMac','clientId','authorization']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for x in networkIDs:
        network_meta = dashboard.networks.getNetwork(x)
        print("[+] Grabbing splash login events for %s" % (network_meta['name']))
        events = dashboard.networks.getNetworkSplashLoginAttempts(networkId=x, timespan=7776000)
        for ev in events:
            writer.writerow([x,network_meta['name'],network_meta['timeZone'],ev['login'],ev['ssid'],ev['loginAt'],ev['gatewayDeviceMac'],ev['clientMac'],ev['clientId'],ev['authorization'] ])

print("[+] Done. Happy hunting !")
