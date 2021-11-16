import server

# 명령어                 파라미터 (Enterprise Security 사용자)                     필수여부
# Name	                Description	Required
# action	            Firewall 규칙(allow/deny)	                            TRUE
# dstnetworkid	        Firewall 규칙 설정할 목적지 network ID	                    TRUE
# srcnetworkid	        Firewall 규칙 설정할 출발지 network ID          	        TRUE
# dstip	                Firewall 규칙 설정할 ACL 상 목적지 IP (ex: 0.0.0.0/32)
# * srcnetworkid가 external network id일 경우 미입력   	                        FALSE
# srcip	                Firewall 규칙 설정할 ACL 상 출발지 IP (ex: 0.0.0.0/32)   	TRUE
# startport	            Firewall 규칙의 시작 포트        	                        FALSE
# endport	            Firewall 규칙의 끝 포트 	                                FALSE
# protocol	            Firewall 규칙에 대한 프로토콜. [ TCP| UDP| ICMP| ALL]	    TRUE
# virtualipid	        포트포워딩 ID
# * srcnetworkid가 external network id일 경우 필수입력	                            FALSE


# Console > Server > Tier에서 Tier id 항목 확인
external = '9d716c43-a517-46bc-bf96-9e242efe8496'
dmz = '36e926d2-609b-4d26-a084-042941dce178'
private = '01c0f413-0bfb-4bf0-8263-38306adc4dc5'



# 특정 포트포워딩 정책 찾기
data = server.listPortForwardingRules(zone='KR-M2')['listportforwardingrulesresponse']['portforwardingrule']

print(data)

# 출발지, 도착지 IP 정의
srcip = ['218.146.32.8/32']
targetIp = ['172.16.11.11','172.16.11.12','172.16.21.11','172.16.21.12']

result = []

for temp in data:
    # 서버의 사설 ip와 서버쪽 포트포워딩된 포트, 그리고 zone을 조건으로 넣어서 result에 추가
    if(temp['vmguestip'] in targetIp and temp['privateport']=='22' and temp['networkid']==dmz):
        result.append(temp)
        print(temp)

# 서버 사설 IP순으로 정책 정렬
result = sorted(result, key=lambda x : x['vmguestip'])
print(result)

ruleid = []

# result에서 포트포워딩 룰 id값을만을 따로 제외하여 ruleid에 추가
for temp in result:
    ruleid.append(temp['id'])

print(ruleid)

# 소스 ip와 룰 id를 이용해 for문을 돌려서 정책 추가
for src in srcip:
    for dst in ruleid:
        print(server.createFirewallRule(zone='KR-M2', protocol='tcp', srcnetworkid=external, dstnetworkid=dmz, action='allow', srcip=src,
                                        virtualipid=dst, startport='22', comments='Sogom-Session'))













# ipaddressid = ''
#
# for temp in data:
#     # print(temp['vmguest'])
#     if temp['vmguestip'] == '172.16.11.93' and temp['privateport'] == '36000':
#         print(temp)
#         ipaddressid = temp['ipaddressid']
#
# print(ipaddressid)




# for temp in ds:
#     print(server.createFirewallRule(zone='EntSec의 경우 KR-M2 입력', protocol='tcp',
#                               srcnetworkid='external', dstnetworkid='private',
#                               action='allow', srcip=sr, virtualipid=targetvm, startport=ports, comments='설명 입력')







    # # 방화벽 정책 하나만 추가할 경우
# srcvm = '출발지 CIDR'
# targetvm = '도착지 CIDR'
# server.createFirewallRule(zone='EntSec의 경우 KR-M2 입력', protocol='프로토콜',
#                                 srcnetworkid='출발지. 위의 external, dmz, private 중 선택하여 입력', dstnetworkid='도착지. 위의 external, dmz, private 중 선택하여 입력',
#                                 action='allow', srcip=srcvm, virtualipid=targetvm, startport='포트번호', comments='설명 입력')





# # 포트는 동일한테 출발지 또는 도착지가 여러개인경우
# srcvm = ['172.16.21.11/32', '172.16.21.12/32']
# targetvm = '172.16.11.96/32'
#
# for ip in srcvm:
#     print(server.createFirewallRule(zone='KR-M2', protocol='tcp',
#                                     srcnetworkid=private, dstnetworkid=dmz,
#                                     action='allow', srcip=ip, virtualipid=targetvm, startport='5000', comments='WAS->Jennifer'))



# # 방화벽 정책을 여러개 동시에 추가할 경우
# # ex) SrcVM -> TargetVM으로 SSH(22), HTTP(80), HTTPS(443) 포트를 오픈하고자 할 경우
# srcvm = '출발지 CIDR'
# targetvm = '도착지 CIDR'
# port = {'22', '80', '443'}
# for ports in port:
#     server.createFirewallRule(zone='EntSec의 경우 KR-M2 입력', protocol='프로토콜',
#                           srcnetworkid='출발지. 위의 external, dmz, private 중 선택하여 입력', dstnetworkid='도착지. 위의 external, dmz, private 중 선택하여 입력',
#                           action='allow', srcip=srcvm, virtualipid=targetvm, startport=ports, comments='설명 입력')


# # 다수의 서버를 동시에 설정할 경우 활용
# srcdata = {'Developer2':'218.143.32.6/32',
#            'Developer-hanwha1':'222.110.254.21/32',
#            'Developer-hanwha2':'222.110.254.22/32',
#            'Developer-hanwha3':'222.110.254.23/32',
#            'Developer-hanwha4':'222.110.254.24/32',
#            'Developer-hanwha5':'222.110.254.25/32'
#            }
#
# for vm in srcdata.items():
#     print(server.createFirewallRule(zone='KR-M2', protocol='tcp', srcnetworkid=external, dstnetworkid=dmz,
#                           action='allow', srcip=vm[1], virtualipid=targetvm, startport='22', comments=vm[0]))


# # # 서버 n:n 포트 여러개
# stip = ['172.16.11.11/32', '172.16.11.12/32']
# dsip = ['172.16.21.11/32', '172.16.21.12/32']
# port = ['18099', '18899']
# for i in range(2):
#     for j in range(2):
#         for k in range(2):
#             print(server.createFirewallRule(zone='KR-M2', protocol='tcp', srcnetworkid=private, dstnetworkid=dmz,
#                                             action='allow', srcip=dsip[i], dstip=stip[j], startport=port[k], comments='WAS->WEB JMX'))
