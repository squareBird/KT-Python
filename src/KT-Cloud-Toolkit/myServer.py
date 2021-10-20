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

    print("VM을 생성할 Zone을 입력해주세요.")
    print("----------------------------------------------")
    for num, zones in zoneList.items():
        str = f'{num} : {zones["name"]}'
        print(str)
    print("----------------------------------------------")

    zoneCode = input()
    zone = zoneList[zoneCode]["code"]

    data = {"zone" : zone, "serviceofferingid":"672cf914-069b-4abc-85cc-0db3155fe001", "templateid":"2835a73c-f276-469c-b874-d75a7abca85b"}

    print(server.deployVirtualMachine(data))