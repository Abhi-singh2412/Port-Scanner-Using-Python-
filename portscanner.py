import subprocess
import ipaddress

# first i will create an function that will help me to identify open devices in network 
def discover_devices(subnet_cidr):
    print(f"DISCOVERING ACTIVE HOSTS ON {subnet_cidr}...")

    result = subprocess.run(['nmap','-sn',subnet_cidr,'-oG','-'],
                            capture_output=True, text=True) # what this capture output tre does is capture the output of the command as a string
    active_hosts = [] # this is an empty list to store the active hosts 
    for line in result.stdout.splitlines():
        if 'Status:Up' in line:
            # extract the IP address from the line
            parts = line.split()
            for part in parts:
                try:
                    ipaddress.ip_address(part) # what this line does is it tries to convert the part to an IP address
                    active_hosts.append(part)
                    break
                except ValueError:
                    continue 

    return active_hosts  

