import ipaddress

my_ip = "172.16.8.40"
prefix = 24

net = ipaddress.ip_network(f"{my_ip}/{prefix}", strict=False)

print(net.netmask)
print(net.network_address)
print(net.broadcast_address)
