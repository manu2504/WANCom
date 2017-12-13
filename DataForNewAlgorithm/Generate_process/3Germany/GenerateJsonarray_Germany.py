import json 
import io
import numpy as np

longitude = np.arange(7.794115,7.794115+12*0.5,0.5)
latitude = np.arange(53.666343-18*0.3,53.666343, 0.3)

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