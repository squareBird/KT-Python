import server # 서버 모듈

# api 및 sec key 설정 부분 임시로 excel21c@wins21.co.kr 로 하드코딩
# c.set_config_env()

def zoneList():

    json_data = server.listZones()
    arr = []

    for data in json_data['listzonesresponse']['zone']:
        arr.append(data['name'])

    return arr

def createVM():

    zoneList = {"1":{"name":"KOR-Seoul M","code":"KR-M"}, "2":{"name":"KOR-Seoul M2", "code":"KR-M2"}, "3":{"name":"KOR-Central A","code":"KR-CA"}, "4":{"name":"KOR-Central B","code":"KR-CB"}}

    print("Zone 선택")
    print("----------------------------------------------")
    for num, zones in zoneList.items():
        str = f'{num} : {zones["name"]}'
        print(str)
    print("----------------------------------------------")

    zoneCode = input()
    zone = zoneList[zoneCode]["code"]
    serviceofferingid = input("Serviceofferingid : ")
    templateid = input("Templateid : ")

    data = {"zone" : zone, "serviceofferingid": serviceofferingid, "templateid": templateid}

    print(server.deployVirtualMachine(data))

def deleteVM():

    zoneList = {"1":{"name":"KOR-Seoul M","code":"KR-M"}, "2":{"name":"KOR-Seoul M2", "code":"KR-M2"}, "3":{"name":"KOR-Central A","code":"KR-CA"}, "4":{"name":"KOR-Central B","code":"KR-CB"}}

    print("Zone 선택")
    print("----------------------------------------------")
    for num, zones in zoneList.items():
        str = f'{num} : {zones["name"]}'
        print(str)
    print("----------------------------------------------")

    zoneCode = input()
    zone = zoneList[zoneCode]["code"]

    json_data = server.listVirtualMachines(zone)
    arr = []

    num = int(1)

    for data in json_data['listvirtualmachinesresponse']['virtualmachine']:
        arr.append(data['id'])
        print(f'{num}. {data["name"]}')
        num+=1

    vmNum = int(input("삭제 VM 선택(9999 입력시 전부 삭제)"))-1

    if(vmNum==9998):
        for i in range(0, len(arr)):
            server.destroyVirtualMachine(zone, arr[i])
    else:
        server.destroyVirtualMachine(zone, arr[vmNum])

    print(zone)

def stopVM():

    zoneList = {"1":{"name":"KOR-Seoul M","code":"KR-M"}, "2":{"name":"KOR-Seoul M2", "code":"KR-M2"}, "3":{"name":"KOR-Central A","code":"KR-CA"}, "4":{"name":"KOR-Central B","code":"KR-CB"}}

    print("Zone 선택")
    print("----------------------------------------------")
    for num, zones in zoneList.items():
        str = f'{num} : {zones["name"]}'
        print(str)
    print("----------------------------------------------")

    zoneCode = input()
    zone = zoneList[zoneCode]["code"]

    json_data = server.listVirtualMachines(zone)
    arr = []

    num = int(1)

    for data in json_data['listvirtualmachinesresponse']['virtualmachine']:
        arr.append(data['id'])
        print(f'{num}. {data["name"]}')
        num+=1

    vmNum = int(input("정지할 VM 선택(9999 입력시 전부 종료)"))-1

    if(vmNum==9998):
        for i in range(0, len(arr)):
            server.stopVirtualMachine(zone, arr[i])
    else:
        server.stopVirtualMachine(zone, arr[vmNum])

    print(zone)