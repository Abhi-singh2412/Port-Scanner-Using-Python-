import subprocess
import ipaddress

# first i will create an function that will help me to identify open devices in network 
def discover_devices(subnet_cidr):
    print(f"DISCOVERING ACTIVE HOSTS ON {subnet_cidr}...")

    result = subprocess.run(['nmap','-sn',subnet_cidr,'-oG','-'],
                            capture_output=True, text=True) # what this capture output tre does is capture the output of the command as a string
    active_hosts = [] # this is an empty list to store the active hosts 
    for line in result.stdout.splitlines():
        if 'Status: Up' in line:
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

# now this is my second function to scan for active ports for those identified devices 

def scan_ports(host):
    print(f"SCANNING TOP 1000 TCP PORTS ON {host}...")

    result = subprocess.run(['nmap','-p-','--open',host],
                            capture_output=True, text=True)
    
    open_ports = []
    for line in result.stdout.splitlines(): # what this will do is split the output into lines

        line = line.strip() # what this will do is remove any leading or trailing whitespace
        if line.endswith("open"):
            parts = line.split() # what this will do is split the line into parts based on whitespace

            if parts:
                port = parts[0].split('/')[0] # what this will do is split the first part of the line by '/' and take the first element (the port number)
                open_ports.append(port)
    return open_ports


if __name__ == "__main__":
    subnet = "172.20.10.0/28"
    active_hosts = discover_devices(subnet)
    print(f"ACTIVE HOSTS: {active_hosts}")

    for device in active_hosts:
        open_ports = scan_ports(device)
        if open_ports:
            print(f"DEVICE {device} HAS OPEN PORTS: {open_ports}")
        else:
            print(f"DEVICE {device} HAS NO OPEN PORTS.")    

