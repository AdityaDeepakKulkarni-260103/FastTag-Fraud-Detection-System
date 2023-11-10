import json
def calldb():
    print("function called ")
    f=open('carDBExt.json',encoding='utf-8')
    data=json.load(f)
    print(next(item for item in data['cardetails'] if item["CarRegistration"] == "GJ05JH2501"))
        
calldb()  