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


os.makedirs('./logs/', exist_ok=True) 
dashboard = meraki.DashboardAPI(output_log=True, log_path="./logs/",
                                log_file_prefix=os.path.basename(__file__), print_console=False)
organizations = dashboard.organizations.getOrganizations()[0]['id']

print("[+] Organization ID: %s " % (organizations))

print("[+] Grabbing Network Device List")
devices = dashboard.organizations.getOrganizationDevicesAvailabilities(organizationId=organizations)
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
                            print(clientIP, clientID, clientMac)
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

