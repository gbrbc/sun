
str = '{"coord":{"lon":-73.99,"lat":40.73},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"base":"stations","main":{"temp":299.78,"pressure":1017,"humidity":34,"temp_min":298.15,"temp_max":301.15},"visibility":16093,"wind":{"speed":5.1,"deg":330,"gust":7.7},"clouds":{"all":40},"dt":1529950500,"sys":{"type":1,"id":1969,"message":0.0041,"country":"US","sunrise":1529918775,"sunset":1529973077},"id":420027420,"name":"New York","cod":200}'

import json

myio = json.loads(str)

ctemp = (myio["main"]["temp"])  - 273
ftemp =  (ctemp*(9/5)) + 32
hum = myio["main"]["humidity"]
print('temp %.2f  humid %d' % (ftemp, hum))
