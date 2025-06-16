import os


str = '{"coord":{"lon":-73.99,"lat":40.73},"weather":[{"id":211,"main":"Thunderstorm","description":"thunderstorm","icon":"11d"},{"id":500,"main":"Rain","description":"light rain","icon":"10d"},{"id":701,"main":"Mist","description":"mist","icon":"50d"}],"base":"stations","main":{"temp":299.79,"pressure":1022,"humidity":70,"temp_min":297.15,"temp_max":302.15},"visibility":16093,"wind":{"speed":1.5,"deg":270},"clouds":{"all":75},"dt":1530652980,"sys":{"type":1,"id":2120,"message":0.0083,"country":"US","sunrise":1530610201,"sunset":1530664232},"id":420027420,"name":"New York","cod":200}'


import json
import pprint

myio = json.loads(str)

#print (json.dumps(str, sort_keys=True, indent=4))

pp=pprint.PrettyPrinter(indent=4, width=40, depth=6, stream=None)

#pp.pprint(str)
if (0) :
     ctemp = (myio["main"]["temp"])  - 273
     ftemp =  (ctemp*(9/5)) + 32
     hum = myio["main"]["humidity"]
     print('temp %.2f  humid %d' % (ftemp, hum))
     print('%s\n' % myio["main:Thunderstorm"])

#for i in myio.items():
#    print (i)

#for j in myio["weather"][0]:
#    print(j)

if myio["weather"][0]["main"] == "Thunderstorm":
    print("Bad weather")
    os.system('echo "Bad weather" | wall')


