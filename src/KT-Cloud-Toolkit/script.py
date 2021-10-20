import server

# BD1 추가
# zone = 'KR-M'
# ipaddressid = '6b4320e3-9665-4504-b3fa-4a3e9a0539c0'
# protocol = 'tcp'
# startport = ['514','2560','3000','3100','6678','7000','8047','8083','8084','8085','8086','8444','8983','9020','20771']
#
# for i in range(0,len(startport)):
#     server.createFirewallRule(zone=zone, ipaddressid=ipaddressid, protocol=protocol, startport=startport[i], cidrlist='175.113.82.83/32')

zone = 'KR-M'
ipaddressid = '6b4320e3-9665-4504-b3fa-4a3e9a0539c0'
protocol = 'udp'
startport = ['162','514']

for i in range(0,len(startport)):
    server.createFirewallRule(zone=zone, ipaddressid=ipaddressid, protocol=protocol, startport=startport[i], cidrlist='175.113.82.83/32')
