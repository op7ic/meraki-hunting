##########################################################
# Author      : Jerzy 'Yuri' Kramarz (op7ic)             #
# Version     : 1.0                                      #
# Type        : Python                                   #
# Description : meraki-hunt.  See README.md for details  #
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

print("[+] Dumping Client Connections")
unique_client = {}
now = datetime.now()
timestampStr = now.strftime("%d-%m-%Y-%s")

with open('meraki-client-connections-%s.csv' % (timestampStr), 'w', newline='', encoding='utf-8') as f:
    csv_header = ['timestamp', 'clientID', 'sourceIP', 'sourceMac',
                  'destinationIP', 'application', 'protocol', 'destinationPort']
    writer = csv.writer(f)
    writer.writerow(csv_header)
    try:
        for x in networkIDs:
            available_clients = dashboard.networks.getNetworkClients(networkId=x, total_pages=9999, perPage=1000)
            # print(available_clients)
            for ac in available_clients:
                try:
                    client_applications = dashboard.networks.getNetworkClientsApplicationUsage(networkId=x, clients=ac['mac'],ssidNumber=0, timespan=2592000)
                    for apps in client_applications:
                        try:
                            clientID = apps['clientId']
                            clientIP = apps['clientIp']
                            clientMac = apps['clientMac']
                            unique_client[clientID] = {}
                            print("[+] Writing Traffic Log From Network: %s Client IP: %s Client ID: %s Client MAC:%s" %(x, clientIP, clientID, clientMac))
                            clientHistory = dashboard.networks.getNetworkClientTrafficHistory(networkId=x, clientId=clientID)
                            for ch in clientHistory:
                                if clientID in unique_client:
                                    writer.writerow([ch['ts'], clientID, clientIP, clientMac,
                                                ch['destination'], ch['application'], ch['protocol'], ch['port']])
                        except:
                            pass
                except:
                    pass
    except:
        pass
    finally:
        pass


print("[+] Done. Happy hunting !")

