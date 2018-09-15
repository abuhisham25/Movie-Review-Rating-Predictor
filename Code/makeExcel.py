import json
data=""
size = [0,0,0,0,0,0,0,0,0,0]
file = open('data.json','r')
counter = 0
currLine = ""
files = [open('data'+str(i+1)+'.txt','w') for i in range(0,10)]
print(len(files))
data = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[]}
import pandas as pd
import numpy as np

for line in file:
	if(line.startswith('{')):
		currLine = line
		text = currLine.index('"text"')
		ratInd = currLine.index('"rating":')
		rat = ratInd+ 10
		rating = line[rat:rat+6]
		rating = rating [1:3]
		if rating[1] == '/':
			rating = rating[0]
		rating = int(rating)
		size[rating -1] += 1 
		toSave =""
		if rat > text :
			toSave = line[text + 8:ratInd]
		else:
			toSave = line[text + 8:line.index('}')]
		if(size[rating - 1] < 2901):
			data[rating].append(toSave)


d1 = np.ones(len(data[1]))
d2 = 2*np.ones(len(data[2]))
d3 = 3*np.ones(len(data[3]))
d4 = 4*np.ones(len(data[4]))
d5 = 5*np.ones(len(data[5]))
d6 = 6*np.ones(len(data[6]))
d7 = 7*np.ones(len(data[7]))
d8 = 8*np.ones(len(data[8]))
d9 = 9*np.ones(len(data[9]))
d10 = 10*np.ones(len(data[10]))
lab = np.concatenate((d1,d2));
lab = np.concatenate((lab,d3));
lab = np.concatenate((lab,d4));
lab = np.concatenate((lab,d5));
lab = np.concatenate((lab,d6));
lab = np.concatenate((lab,d7));
lab = np.concatenate((lab,d8));
lab = np.concatenate((lab,d9));
lab = np.concatenate((lab,d10));
print(str(np.shape(lab)))
temp = []
for i in data.keys():
	temp+=data[i]

print(str(np.shape(temp)))
df = pd.DataFrame({"reviews":temp,"rating":lab})
# df2 = pd.DataFrame({"org_person":list(org_person.keys()),"records":list(org_person.values())})

writer = pd.ExcelWriter('reviews.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()