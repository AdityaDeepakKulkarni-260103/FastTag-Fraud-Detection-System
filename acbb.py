import json
import random
with open("carDBExt.json",encoding='utf-8') as jsonFile:
    data = json.load(jsonFile)
    for i in data['cardetails']:
        i['AccountBalance']=random.randint(6000,9000)
with open("carDBExt.json", "w") as jsonFile:
    json.dump(data, jsonFile)