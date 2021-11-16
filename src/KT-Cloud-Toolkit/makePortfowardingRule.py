import server

# Console > Server > Tier에서 Tier id 항목 확인
external = '9d716c43-a517-46bc-bf96-9e242efe8496'
dmz = '36e926d2-609b-4d26-a084-042941dce178'
private = '01c0f413-0bfb-4bf0-8263-38306adc4dc5'

# * Args:
# - zone(String, Required) : [KR-CA, KR-CB, KR-M, KR-M2]
# - ipaddressid(String, Required) : 공인 IP
# - privateport(String, Required) : 포트포워딩 대상 VM 포트
# - protocol(String, Required) : TCP or UDP
# - publicport(String, Required) : public port
# - vmid(String, Required): VM id to update.

ips = server.listPublicIpAddresses(zone='KR-M2')['listpublicipaddressesresponse']['publicips']
pubip = '211.34.228.16'
data = {}

vmip = ['172.16.21.11','172.16.21.12','172.16.21.31']

for temp in ips:
    if temp['ip']==pubip:
        data = temp['virtualips']

for temp2 in data:
    for x in vmip:
        if temp2['vmguestip']==x and temp2['privateport']=='10080':
            print(temp2)
