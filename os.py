import platform
import psutil
import netaddr # install with pip install netaddr
import netifaces # install with pip install netifaces

print(f"Architecture: {platform.architecture()}")
print(f"Network Name: {platform.node()}")
print(f"Operating system: {platform.system()}")

print()
print('RAM memory % used:', psutil.virtual_memory()[2])

print()
netifaces.interfaces()
adresse_ip = netifaces.ifaddresses('en0')[2][0]['addr']
netaddr_adresse_ip = netaddr.IPAddress(adresse_ip)
print(f"Mon ip est {netaddr_adresse_ip}")

print()
# Calling psutil.cpu_precent() for 4 seconds
print('The CPU usage is: ', psutil.cpu_percent(4))

