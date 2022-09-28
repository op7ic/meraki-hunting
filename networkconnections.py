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
import time

# Instructions:
# Set APIKEY in environment variable MERAKI_DASHBOARD_API_KEY.
# Install meraki via 'pip install meraki' command and run this python script

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

# ---- Begin Script ----

os.makedirs('./logs/', exist_ok=True)
dashboard = meraki.DashboardAPI(output_log=True, log_path="./logs/",log_file_prefix=os.path.basename(__file__), print_console=False)
selected_org, orgName = select_org(dashboard)

print("[+] Organization ID: %s " % (selected_org))

print("[+] Grabbing Network Device List")
devices = dashboard.organizations.getOrganizationNetworks(organizationId=selected_org,total_pages='all')
networkIDs = []
for a in devices:
	netID = a['id']
	if netID not in networkIDs:
		networkIDs.append(netID)

print("[+] Dumping Network Connections")
unique_client = {}
now = datetime.now()
timestampStr = now.strftime("%d-%m-%Y-%s")

with open('meraki-network-connections-%s.csv' %(timestampStr), 'w', newline='', encoding='utf-8') as f:
	csv_header =  ['network ID','network name','timezone','application', 'destination', 'port', 'protocol','numberof_flows','clients']
	writer = csv.writer(f)
	writer.writerow(csv_header)
	for x in networkIDs:
		time.sleep(3)
		print("[+] Writing Traffic Log From Network ID %s " % (x))
		try:
			network_meta = dashboard.networks.getNetwork(x)
			available_connections = dashboard.networks.getNetworkTraffic(networkId=x, timespan=2592000,total_pages=9999, perPage=1000)
			for at in available_connections:
				if (at['destination'] != None):
					writer.writerow([x,network_meta['name'],network_meta['timeZone'],at['application'],at['destination'],at['port'],at['protocol'],at['flows'],at['numClients'] ])
		except:
			pass
print("[+] Done. Happy hunting !")