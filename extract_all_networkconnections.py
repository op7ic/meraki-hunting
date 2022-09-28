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
import time

# Instructions:
# Set APIKEY in environment variable MERAKI_DASHBOARD_API_KEY.
# Install meraki via 'pip install meraki' command

os.makedirs('./logs/', exist_ok=True)
dashboard = meraki.DashboardAPI(output_log=True, log_path="./logs/",
                                log_file_prefix=os.path.basename(__file__), print_console=False)
organizations = dashboard.organizations.getOrganizations()[0]['id']

print("[+] Organization ID: %s " % (organizations))

print("[+] Grabbing Network Device List")
devices = dashboard.organizations.getOrganizationNetworks(organizationId=organizations,total_pages='all')
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
		print("Network ID %s " % (x))
		try:
			network_meta = dashboard.networks.getNetwork(x)
			available_connections = dashboard.networks.getNetworkTraffic(networkId=x, timespan=2592000,total_pages=9999, perPage=1000)
			for at in available_connections:
				if (at['destination'] != None):
					writer.writerow([x,network_meta['name'],network_meta['timeZone'],at['application'],at['destination'],at['port'],at['protocol'],at['flows'],at['numClients'] ])
		except:
			pass
print("[+] Done. Happy hunting !")