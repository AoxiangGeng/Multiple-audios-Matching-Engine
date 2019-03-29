#import json
import numpy as np
#temp = []       
#with open("temp_match_4.csv","r") as f:
#    for row in f.readlines():
#        temp.append(float(json.loads(row)[0]))
#        temp.append(float(json.loads(row)[1]))
#temp=np.array(temp)
#temp = np.unique(temp)
#with open("temp_match_6.csv","w") as g:
#    for i in temp:
#        g.write(str(i)+'\n')


id1=[[1,2],
     [3,3],
     [5,1],
     [1.1,4],
     [7,0],
     [6,1]    
     ]
id1=np.array(id1)
print(id1)
maxd=np.argmax(id1,axis=0)
print(maxd)

