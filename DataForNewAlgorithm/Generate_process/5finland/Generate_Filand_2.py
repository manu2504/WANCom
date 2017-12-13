import json 
import io
import numpy as np

longitude = np.arange(21.612457,21.612457+15*0.5,0.5)
latitude = np.arange(63.203807-9*0.3,63.203807, 0.3)

#print longitude
#print latitude
data = []

for La in latitude:
	for Lo in longitude:
		info={}
		info["Latitude"]=La
		info["Longitude"]=Lo
		data.append(info)
#print data
dictionary = {"nodes":data}
#print dictionary 
j = json.dumps(dictionary, indent=4, separators=(',', ': '))
f = open('data.json', 'w')
f.write(j)
#print >> f, j
f.close()