import server


data = server.listFirewallRules(zone='KR-M2')
data = data['listfirewallrulesresponse']['firewallrules'][0]['acls']

data = sorted(data, key = lambda x:x['id'])

print(data)

# # 특정한 comment가 달린 방화벽 정책 일괄 삭제
# for temp in data:
#     if(temp['comments']=='WAS->WEB JMX'):
#         print(server.deleteFirewallRule(zone='KR-M2', id=str(temp['id'])))

