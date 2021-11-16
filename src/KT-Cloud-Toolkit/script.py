import server

###############################   특정 사양의 VM을 생성하기   ################################
# zone(String, Required) : [KR-CA, KR-CB, KR-M, KR-M2]
zone = '위의 zone 정보 참고하여 입력'

# 생성하려는 ZONE에서 사용가능한 VM 사양들 리스트 출력
json_data = server.listAvailableProductTypes(zone=zone)
for data in json_data['listavailableproducttypesresponse']['producttypes']:
    print(data)

# name = ['SWEB-01', 'SWEB-02', 'SWAS-01', 'SWAS-02']
name = ['생성할 VM들의 이름 입력']

for data in name:
    print(server.deployVirtualMachine(zone=zone, productcode='출력된 VM 사양 목록에서 원하는 사양을 찾아 productid 값 찾아서 입력', name=data))
#############################################################################################





############################   하나의 대상 VM에 여러 포트포워딩 룰 추가하기   ############################
# zone(String, Required) : [KR-CA, KR-CB, KR-M, KR-M2]
zone = '위의 zone 정보 참고하여 입력'

ipaddressid = '방화벽 설정 대상 공인IP의 ID 입력(콘솔 -> 공인IP -> 상세정보확인)'

vmid = '포트포워딩 설정 대상 VM의 id(콘솔 -> 서버 -> 상세정보확인)'

# port = {'12':'12','211':'112','3332':'344'}
port = {'공인 IP 포트' : '사설 IP 포트'}

protocol = '프로토콜 입력'

for p in port.items():
    print(server.createPortForwardingRule(zone=zone, ipaddressid=ipaddressid, publicport=p[0], privateport=p[1], protocol=protocol, vmid=vmid, cidrlist='출발지 CIDR 정보 입력'))
#############################################################################################





#########################   특정 zone 의 포트포워딩 정보 모두 삭제   ##########################
# zone(String, Required) : [KR-CA, KR-CB, KR-M, KR-M2]
zone = '위의 zone 정보 참고하여 입력'
json_data = server.listPortForwardingRules(zone=zone)

ruleId = []
for temp in json_data['listportforwardingrulesresponse']['portforwardingrule']:
    ruleId.append(temp['id'])

print(ruleId)

for rule in ruleId:
    print(server.deletePortForwardingRule(zone=zone, id=rule))
############################################################################################





#################################   방화벽 포트 다중 설정   ##################################
# zone(String, Required) : [KR-CA, KR-CB, KR-M, KR-M2]
zone = '위의 zone 정보 참고하여 입력'

ipaddressid = '방화벽 설정 대상 공인IP의 ID 입력(콘솔 -> 공인IP -> 상세정보확인)'

protocol = '프로토콜 입력(소문자)'

# startport = ['514','2560','3000','3100','6678','7000','8047','8083','8084','8085','8086','8444','8983','9020','20771']
startport = ['추가할 포트번호 입력, 숫자가 아닌 문자열로 입력']

for i in range(0,len(startport)):
    server.createFirewallRule(zone=zone, ipaddressid=ipaddressid, protocol=protocol, startport=startport[i], cidrlist='출발지 CIDR 정보 입력')
#############################################################################################
