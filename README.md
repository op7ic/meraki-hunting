# meraki-hunting

A collection of standalone scripts used to automate data extraction, assessment and threat hunting against [Meraki](https://developer.cisco.com/meraki/) networks.

# Usage

Install [meraki](https://pypi.org/project/meraki/) library: 
- pip install meraki 

Set your Meraki API key to an environment variable before running scripts:
- export MERAKI_DASHBOARD_API_KEY=XXXXXX

Execute specific script:

```python3 clientconnections.py```

# API Documentation
- See [official website](https://developer.cisco.com/meraki/) for latest API documentation.

# Description

- ```extract_all_clientconnections.py``` - enumerates all the networks in all organizations and extracts individual outbound connections for each host in last 30 days.
- ```extract_all_networkconnections.py``` - enumerates all the networks in all organizations and extracts outbound connections originating from each network in last 30 days.
- ```apstatus.py``` - enumerates networks in a selected organization and display current AP status that is different to online/no problems.
- ```clientconnections.py``` - enumerates networks in a selected organization and extracts individual outbound connections for each host in last 30 days.
- ```networkconnections.py``` - enumerates networks in a selected organization and extracts individual outbound connections from each network in last 30 days.
- ```topologyoverview.py``` - enumerates networks in a selected organization and extracts simple topology overview.
- ```loginoverview.py``` - enumerates networks in a selected organization and extracts an overview of login attempts to splash screen across last 90 days.
- ```getMXfirewallrules.py``` - enumerates networks in a selected organization and extracts an overview of applied [SD-WAN](https://meraki.cisco.com/products/security-sd-wan/) firewall rules for cellular, inbound, l3, l7 and port forwarding rules.

# Acknowledgments

- [Mitchell Wyatt](https://github.com/wyattmitchell/). Thanks for code review and improvement suggestions!
