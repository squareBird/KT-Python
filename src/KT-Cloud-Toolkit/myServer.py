import server # 서버 모듈

# api 및 sec key 설정 부분 임시로 excel21c@wins21.co.kr 로 하드코딩
# c.set_config_env() -> 환경변수 설정

# 사용가능한 Zone List를 보여줌
def viewZoneList():

    json_data = server.listZones()
    arr = []

    for data in json_data['listzonesresponse']['zone']:
        arr.append(data['name'])

    return arr

# 작업을 수행할 Zone을 선택
def choiceZone():

    viewZoneList()

    zoneList = {"1":{"name":"KOR-Seoul M","code":"KR-M"}, "2":{"name":"KOR-Seoul M2", "code":"KR-M2"}, "3":{"name":"KOR-Central A","code":"KR-CA"}, "4":{"name":"KOR-Central B","code":"KR-CB"}}

    print("Zone 선택")
    print("----------------------------------------------")
    for num, zones in zoneList.items():
        str = f'{num} : {zones["name"]}'
        print(str)
    print("----------------------------------------------")

    zoneCode = input()
    zone = zoneList[zoneCode]["code"]

    return zone

# 특정 Zone의 VM List를 보여줌
def viewVMList(zone):

    json_data = server.listVirtualMachines(zone=zone)
    arr = []

    num = int(1)

    for data in json_data['listvirtualmachinesresponse']['virtualmachine']:
        arr.append(data['id'])
        print(f'{num}. {data["name"]}')
        num+=1

    return arr

def viewPublicIPList(zone):

    # public IP 리스트를 받아옴
    json_data = server.listPublicIpAddresses(zone=zone)
    # public ip들이 담긴 배열
    publicIpList = []

    num = int(1)

    for data in json_data['listpublicipaddressesresponse']['publicipaddress']:
        publicIpList.append(data['id'])
        print(f'{num}. {data["ipaddress"]}')
        num+=1

    return publicIpList

# 특정 Zone의 공인 IP List를 보여줌
def choicePublicIp(zone):

    publicIpList = viewPublicIPList(zone)
    num = int(input("포트포워딩 설정할 IP 선택 : "))-1

    print(f'선택한 IP : {publicIpList[num]}')

    return publicIpList[num]

# VM 생성
def createVM():

    num = int(input("생성 방식 선택(1. 직접 입력\t2. 설정 파일"))

    # zone : 생성할 zone
    # serviceofferingid : CPU/MEM 사양
    # templateid : OS 정보
    # name : 이름
    zone = choiceZone()
    serviceofferingid = input("CPU/Memory ID : ")
    templateid = input("OS ID : ")
    name = input("VM 이름 : ")

    print(server.deployVirtualMachine(zone=zone, serviceofferingid=serviceofferingid, templateid=templateid, name=name))

# VM 삭제
def deleteVM():

    zone = choiceZone()
    arr = viewVMList(zone)
    vmNum = int(input("삭제 VM 선택(9999 입력시 전부 삭제)"))-1

    if(vmNum==9998):
        for i in range(0, len(arr)):
            server.destroyVirtualMachine(zone, arr[i])
    else:
        server.destroyVirtualMachine(zone=zone, vmid=arr[vmNum])

    print(zone)

# VM 정지
def stopVM():

    zone = choiceZone()
    arr = viewVMList(zone)
    vmNum = int(input("정지할 VM 선택(9999 입력시 전부 종료)"))-1

    if(vmNum==9998):
        for i in range(0, len(arr)):
            server.stopVirtualMachine(zone, arr[i])
    else:
        server.stopVirtualMachine(zone=zone, vmid=arr[vmNum])

    print(zone)

# 포트포워딩 룰 생성
def createPortFowardingRules():

    zone = choiceZone()
    publicIp = choicePublicIp(zone)
    vmList = viewVMList(zone)
    vmid = vmList[int(input("VM 선택"))-1]
    protocol = input("프로토콜 입력 (tcp/udp) : ").lower()
    publicPort = input("퍼블릭 IP 포트 : ")
    privatePort = input("VM 포트 : ")

    print(f'{zone} {publicIp} {publicPort} {protocol} {privatePort} {vmid}')

    print(server.createPortForwardingRule(zone=zone, ipaddressid=publicIp, protocol=protocol, publicport=publicPort, privateport=privatePort, vmid=vmid))
    




