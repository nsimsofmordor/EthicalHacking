#! /usr/bin/env python3

# mac-changer.py  -- script to change the MAC address with optparse and verify that is was changed using regex

import subprocess
import optparse
import re


def get_arguments():
    """Will get arguments based on the options the user uses"""

    parser = optparse.OptionParser()  # parser is the object of the optparse.OptionParser() class

    #                 |  name of option  || dest variable ||          help info            |
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac",       dest="new_mac",   help="New MAC address")

    # will parse the arguments as (value, args), so capture those values as tups
    (options, arguments) = parser.parse_args()

    if not options.interface:  # If no options are provided for interface
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:  # If no options are provided for MAC
        parser.error("[-] Please specify a new mac, use --help for more info")

    return options


def change_mac(interface_option, new_mac_option):
    """Will change the MAC address of the provided interface and new MAC"""

    print(f"[+] changing MAC address for {interface_option} to {new_mac_option}")

    subprocess.call(["ifconfig", interface_option, "down"])  # execute ifconfig on interface and shut it down
    subprocess.call(
        ["ifconfig", interface_option, "hw", "ether", new_mac_option])  # execute ifconfig on interface and change the mac address
    subprocess.call(["ifconfig", interface_option, "up"])  # execute ifconfig on interface and turn it on


def get_current_mac(interface):
    """Will get the current MAC address using subprocess.check_output() and Regex"""

    ifconfig_result = subprocess.check_output(["ifconfig", interface])  # returns the output of the executed command

    # Using Regex to look for the mac address  -- Pythex is a helpful website
    macRegex = re.compile(r'\w\w\:\w\w\:\w\w\:\w\w\:\w\w\:\w\w')  # create the regex object
    mac_address_search_result = macRegex.search(str(ifconfig_result))  # search for the pattern in ifconfig_result

    if mac_address_search_result:  # if a pattern is matched, return to main program
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()  # Call to our function, saves results as options

original_mac = get_current_mac(options.interface)  # Get the current MAC before any changed are made

change_mac(options.interface, options.new_mac)  # Change the MAC

new_mac = get_current_mac(options.interface)  # Get the new MAC  (you could just overwrite the current_mac)

if new_mac == options.new_mac:  # if the new mac is the same as the mac passed into the change_mac function
    print(f"[+] MAC address was successfully changed from {original_mac} to {new_mac}")
else:
    print("[-] MAC address did not get changed")





