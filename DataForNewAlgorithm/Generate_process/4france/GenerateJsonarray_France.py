import json 
import io
import numpy as np

longitude = np.arange(-1.299819,-1.299819+16*0.5,0.5)
latitude = np.arange(49.322337-19*0.3,49.322337, 0.3)

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