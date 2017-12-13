import json 
import io
import numpy as np

longitude = np.arange(-117.085136,-117.085136+20*2,2.0)
latitude = np.arange(48.577052-9*2.0, 50.577052, 2.0)

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