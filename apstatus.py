##########################################################
# Author      : Jerzy 'Yuri' Kramarz (op7ic)             #
# Version     : 1.0                                      #
# Type        : Python                                   #
# Description : meraki-hunt.  See README.md for details  #
# License     : See LICENSE for details                  #
########################################################## 

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
dashboard = meraki.DashboardAPI(output_log=True, log_path="./logs/", log_file_prefix=os.path.basename(__file__), print_console=False)
selected_org, orgName = select_org(dashboard)
print(f"[+] Organization ID: {selected_org}")

print("[+] Grabbing Network Device List")
devices = dashboard.organizations.getOrganizationDevicesAvailabilities(organizationId=selected_org)
networkIDs = []
for a in devices:
	if (a['status'] == 'alerting' or a['status'] == 'dormant' or a['status'] == 'offline'):
		print("Status: %s MAC: %s Name: %s Network ID: %s" % (a['status'], a['mac'], a['name'], a['network']['id']))