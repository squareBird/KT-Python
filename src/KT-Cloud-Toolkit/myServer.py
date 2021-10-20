import server # 서버 모듈

# api 및 sec key 설정 부분 임시로 excel21c@wins21.co.kr 로 하드코딩
# c.set_config_env() -> 환경변수 설정
# myserver.py는 KT에서 기본적으로 제공하는 sever.py 모듈을 SDK로 활용하여 커스터마이징하기 위한 모듈
# 기존의 server들은 커맨드라인에서 **kargs를 통해 받은 파라미터를 변수로 사용하였음
# 커맨드라인을 통해 기능들이 수행 가능하도록 하기 위해 **kargs로 받던 값들을 메소드 전달시 변수의 형태로 전달해주도록 SDK 수정

# 사용가능한 Zone List를 보여줌
def viewZoneList():

    json_data = server.listZones()
    arr = []

    for data in json_data['listzonesresponse']['zone']:
        arr.append(data['name'])

    return arr

# 작업을 수행할 Zone을 선택
# 내부에서 viewZoneList 메소드 수행하여 출력된 Zone List의 번호를 입력하여 선택
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
# 파라미터 : zone 이름(choiceZone 메소드 return 값)
def viewVMList(zone):

    json_data = server.listVirtualMachines(zone)
    arr = []

    num = int(1)

    for data in json_data['listvirtualmachinesresponse']['virtualmachine']:
        arr.append(data['id'])
        print(f'{num}. {data["name"]}')
        num+=1

    return arr

def viewPublicIPList(zone):

    # public IP 리스트를 받아옴
    json_data = server.listPublicIpAddresses(zone)
    # public ip들이 담긴 배열
    publicIpList = []

    num = int(1)

    for data in json_data['listpublicipaddressesresponse']['publicipaddress']:
        publicIpList.append(data['ipaddress'])
        print(f'{num}. {data["ipaddress"]}')
        num+=1

    return publicIpList

# 특정 Zone의 공인 IP List를 보여줌
# 파라미터 : zone 이름(choiceZone 메소드 return 값)
def choicePublicIp(zone):

    publicIpList = viewPublicIPList(zone)
    num = int(input("포트포워딩 설정할 IP 선택 : "))-1

    print(f'선택한 IP : {publicIpList[num]}')

    return publicIpList[num]

# VM 생성
# 직접 입력 방식과 txt 파일에 서버 정보 입력하는 방식으로 제작 예정
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

    print(server.deployVirtualMachine(zone, serviceofferingid, templateid, name))

# VM 삭제
def deleteVM():

    zone = choiceZone()
    arr = viewVMList(zone)
    vmNum = int(input("삭제 VM 선택(9999 입력시 전부 삭제)"))-1

    if(vmNum==9998):
        for i in range(0, len(arr)):
            server.destroyVirtualMachine(zone, arr[i])
    else:
        server.destroyVirtualMachine(zone, arr[vmNum])

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
        server.stopVirtualMachine(zone, arr[vmNum])

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

    print(f"{zone} {publicIp} {publicPort} {vmid} {privatePort} {protocol}")
    # * Examples : print(server.createPortForwardingRule(zone='KR-M', ipaddressid='3a304bed-d7c0-4836-a31f-c4e10d2ab0be', privateport='5555', protocol='tcp', publicport='5555', vmid='47d2ea4c-d434-418b-a854-c99054abeff7'))

    server.createPortForwardingRule(zone=zone, ipaddressid=publicIp, protocol=protocol, publicport=publicPort, privateport=privatePort, vmid)
    




