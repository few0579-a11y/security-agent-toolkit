import ipaddress

parent = ipaddress.ip_network("192.168.50.0/24")

for sub in parent.subnets(new_prefix=25):
    print(sub)
