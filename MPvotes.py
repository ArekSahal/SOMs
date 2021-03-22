import numpy as np
from SOMap import SOMap
from graphics import Presenter
import matplotlib.pyplot as plt

data = []
labels = [] 

parties = []
sex = [] # Not like that
districts = []
with open('votes.dat', 'r') as f:
	d = f.readlines()
	for i in d:
		dummy = []
		k = i.split(",")
		for j in k:
			dummy.append(float(j)) 
		data.append(dummy)

with open('mpparty.dat', 'r') as f:
	d = f.readlines()
	for i in d:
	    k = i.strip().split(",")
	    parties.append(k[0])

with open('mpsex.dat', 'r') as f:
	d = f.readlines()
	for i in d:
	    k = i.strip().split(",")
	    sex.append(k[0])

with open('mpdistrict.dat', 'r') as f:
	d = f.readlines()
	for i in d:
	    k = i.strip().split(",")
	    districts.append(k[0])
	  
data = np.array(data)
data = np.reshape(data,(349,31))

parties = parties[3:]
sex = sex[2:]
labels = [sex, parties, districts]

model = SOMap(31, 100)
model.set_data(data)
#model.train(30)
#model.save()
model.load()
presenter = Presenter()
presenter.model = model

#presenter.set_data(data, labels, ["Sex", "Party", "District"], [["Male", "Female"],[],[]])
presenter.set_data(data, labels, ["Sex"], [["Male", "Female"]])
presenter.show()
plt.show()