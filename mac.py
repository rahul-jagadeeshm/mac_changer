import subprocess
import optparse
import re
from banner import banners



 #this function is used for displaying available network interfaces lil eth0 ,wlan, lo, 
 
def show_interfaces():

    print("Display Available Network Interfaces :")
    
    avilable_network = subprocess.check_output(["ls", "/sys/class/net"])
    
    print(avilable_network)


def args():

    parser = optparse.OptionParser()

    parser.add_option("-i","--interface", dest="network_interface",help="Interface to change it's mac address")

    parser.add_option("-m", "--mac", dest="new_mac", help=" New mac address to change it's current mac address")

    parser.add_option("-s", "--show_interfaces", dest="show_interfaces",help="Use '-s show' to see the available interfaces")

    (options, arguments) = parser.parse_args()

    if options.show_interfaces == "show":
        show_interfaces()
       

    else:

        if not options.network_interface:
            parser.error("[-] please specify network interface  , use --help for more info. ")

        elif not options.new_mac:
            parser.error("[-] please specify  a new mac address  , use --help for more info. ")

        return options


def change_mac(network_interface, new_mac):

    banners()

    print("changing current  mac address for " + " " + network_interface + "  " + "to" + " " + new_mac)

    subprocess.call(["sudo", "ifconfig", network_interface, "down"])
    subprocess.call(["sudo", "ifconfig", network_interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", network_interface, "up"])



def get_current_mac(network_interface):

    ifconfig_result = subprocess.check_output(["ifconfig", network_interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_search_result:
        
        return mac_search_result.group(0)
    else:
        print("[-] could not read MAC address ")  
    
    


options = args()

  
current_mac = get_current_mac(options.network_interface)

print("Current MAC = " + str(current_mac))

change_mac(options.network_interface, options.new_mac)

current_mac = get_current_mac(options.network_interface)

if current_mac == options.new_mac:

    print("[-] MAC adress was successfully changes to " + current_mac)
else:
    print("[-] MAC address did not get changed")    
