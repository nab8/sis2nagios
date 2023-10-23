#!/usr/bin/env python3
"""This file queries the SIS API to create Nagios configuration."""
from main import fetch_sis_api, Device, Site
import config
import fileinput
import ipaddress
import math
import os.path

sites = {}
equipment = {}

# Populate devices
for model in config.modelname:
    device_count_fetch = fetch_sis_api(
        'equipment',
        {
            'ownercode': config.ownercode,
            'modelname': model,
            'page[size]': 1
            }
        )
    device_count = device_count_fetch['meta']['pagination']['count']
    device_pages = math.ceil(device_count/config.page_size)
    i = 1
    # Fetch each page
    while i <= device_pages:
        device_fetch = fetch_sis_api(
            'equipment',
            {
                'ownercode': config.ownercode,
                'modelname': model,
                'page[number]': i
                }
            )
        i += 1
        for device in device_fetch['data']:
            # Check for public IP to use
            ipv4address = ""
            for address in device["attributes"]['equipips']:
                if (ipaddress.ip_address(address['ipv4address']).is_global
                        or ipv4address == ""):
                    ipv4address = address['ipv4address']
            # Only create config if there is an IPv4 Address
            if ipv4address != "":
                try:
                    lookupcode = (device['relationships']['equipinstalls']
                                        ['data'][0]['lookupcode'])
                    equipment[device["id"]] = Device(
                        id=device["id"],
                        model=model,
                        address=ipv4address,
                        lookupcode=lookupcode,
                        host_name=lookupcode+"_"+model.replace(" ", "_")
                        )
                except KeyError:
                    pass

# Populate sites & initialize devices
# Determine number of sites
site_count_fetch = fetch_sis_api(
    'site-epochs',
    {'netcode': config.ownercode, 'page[size]': 1}
    )
site_count = site_count_fetch['meta']['pagination']['count']
site_pages = math.ceil(site_count/config.page_size)
i = 1
# Fetch each page
while i <= site_pages:
    site_fetch = fetch_sis_api(
        'site-epochs',
        {'netcode': config.ownercode, 'page[number]': i}
        )
    i += 1
    # Populate sites
    for site in site_fetch['data']:
        try:
            sites[site['attributes']['lookupcode']] = Site(
                site['id'],
                site['attributes']['lookupcode'],
                site['attributes']['latitude'],
                site['attributes']['longitude']
                )
        except KeyError:
            pass

# Create Configs
for item in equipment:
    file_path = config.nagios_path+"/"+equipment[item].host_name+".cfg"
    if os.path.isfile(file_path):
        for line in fileinput.FileInput(file_path, inplace=1):
            if line.startswith("\t_id"):
                line = "\t_id\t"+equipment[item].id+"\n"
            elif line.startswith("\thost_name"):
                line = "\thost_name\t"+equipment[item].host_name+"\n"
            elif line.startswith("\t_model"):
                line = "\t_model\t"+equipment[item].model+"\n"
            elif line.startswith("\tuse"):
                line = "\tuse\t"+equipment[item].model+"-template\n"
            elif line.startswith("\taddress"):
                line = "\taddress\t"+equipment[item].address+"\n"
            elif line.startswith("\t_latitude"):
                if (equipment[item].lookupcode in sites and
                        sites[equipment[item].lookupcode].latitude != ""):
                    line = "\t_latitude\t"+str(
                        sites[equipment[item].lookupcode].latitude
                        )+"\n"
            elif line.startswith("\t_longitude"):
                if (equipment[item].lookupcode in sites and
                        sites[equipment[item].lookupcode].longitude != ""):
                    line = "\t_longitude\t"+str(
                        sites[equipment[item].lookupcode].longitude
                        )+"\n"
            print(line, end="")
    else:
        # Create new file
        f = open(file_path, "w")
        f.write("define host{\n")
        f.write("\t_id\t"+equipment[item].id+"\n")
        f.write("\thost_name\t"+equipment[item].host_name+"\n")
        f.write("\t_model\t"+equipment[item].model+"\n")
        f.write("\tuse\t"+equipment[item].model+"-template\n")
        # If a site is missing we leave longitude & latitude empty
        if equipment[item].lookupcode in sites:
            f.write("\t_latitude\t"+str(
                sites[equipment[item].lookupcode].latitude)+"\n"
                )
            f.write("\t_longitude\t"+str(
                sites[equipment[item].lookupcode].longitude
                )+"\n")
        else:
            f.write("\t_latitude\n")
            f.write("\t_longitude\n")
        f.write("\taddress\t"+equipment[item].address+"\n")
        f.write("}\n")
        f.close()
