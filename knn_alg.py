#!/usr/bin/env python
# coding: utf-8

# In[275]:


from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import io
import seaborn as sns
import copy


# In[276]:


url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vShT1iL5h5WAFoyhmJfjuzKvga3xRopxVfoxaPaEinH9tIgb00eJxzwvgEYQHRf6cHd5xd_mape1ksl/pub?gid=1885783064&single=true&output=csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')))


# In[277]:


#cleaned_data = c... #make into a matrix with only numerical values
df.columns = ['timestamp', 'name', 'grade', 'major', 'courses', 'interests', 'harry_potter']
df = df.drop('courses', axis=1)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df


# In[278]:


index_to_name = df.iloc[:,1]
index_to_name


# In[279]:


cleaned_data = df.copy()
cleaned_data = cleaned_data.drop(["timestamp", "name"], axis=1)
cleaned_data['grade'] = cleaned_data['grade'].map({'Freshman':0,'Sophomore':1,'Junior':2,'Senior':3})
cleaned_data['harry_potter'] = cleaned_data['harry_potter'].map({'Gryffindor':0,'Hufflepuff':1,'Ravenclaw':2,'Slytherin':3})
cleaned_data = cleaned_data[['grade', 'harry_potter']]
cleaned_data


# In[280]:


cdmatrix = cleaned_data.to_numpy()
tree = KDTree(cdmatrix)

ind_nearest = {} #each individual mapped to their pair (both repr by index)
nearest_ind = {}
my_set = set([]) #set of all individuals in a pair

def alreadyUsed(n):
    return n in my_set

def getNearest(n, k):
    #already matched
    if alreadyUsed(n): 
        return
    
    #get the nearest element
    dist, nearest = tree.query(cdmatrix[n:n+1], k=k, return_distance=True)
    nearest = nearest[0].tolist()
    dist = dist[0].tolist()
    if n in nearest:
        dist.remove(dist[nearest.index(n)])
        nearest.remove(n)
    ncopy = copy.deepcopy(nearest)
    length = len(ncopy)
    for ind in ncopy:
        if alreadyUsed(ind):
            dist.remove(dist[nearest.index(ind)])
            nearest.remove(ind)
    
    if nearest == [] and k < cdmatrix.shape[0]: #expand search to more distant pts
        getNearest(n, k+1)
    elif nearest == []:
        print("whoops this was not supposed to happen. Happy debugging! :(. Or maybe there's just an odd number of users in which case this ok")
    else: #create pairing/matching
        nearest = nearest[dist.index(min(dist))]
        my_set.add(n)
        my_set.add(nearest)
        ind_nearest[n] = nearest
        nearest_ind[nearest] = n

if cleaned_data.shape[0] <= 1:
    print("there's nothing to sort and you're gonna get an error")
for ind in cleaned_data.index.to_list():
    getNearest(ind, 2)


# In[281]:


# deal with odd numbers of users 
if cleaned_data.shape[0] % 2 == 1:
    for ind in cleaned_data.index.to_list():
        if not alreadyUsed(ind):
            odd_one_out = ind #this will be used later
            break
    dist, odd_one_out_nearest = tree.query(cdmatrix[odd_one_out:odd_one_out+1], k=2)
    dist = dist[0].tolist()
    odd_one_out_nearest = odd_one_out_nearest[0].tolist()
    if odd_one_out in odd_one_out_nearest.copy():
        dist.remove(dist[odd_one_out_nearest.index(odd_one_out)])
        odd_one_out_nearest.remove(odd_one_out)
    odd_one_out_nearest = odd_one_out_nearest[dist.index(min(dist))] #this will be used later


# In[282]:


ind_nearest, nearest_ind
pairs = {}

pair = 1
for key in ind_nearest.keys():
    pairs[pair] = (key, ind_nearest[key])
    pair += 1
pairs
print(pairs)


# In[283]:



# In[284]:


pair_col = [i//2 for i in range(2, cleaned_data.shape[0]+2)]

ind_col = []
alternating = 0
for i in pair_col:
    if i in pairs.keys():
        ind_col.append(pairs[i][alternating % 2])
        alternating += 1

if cleaned_data.shape[0] % 2 == 0:
    ind_w_group = pd.Series(pair_col, index=ind_col)
else:
    pair_col = pair_col[:len(pair_col)-1]
    insert_here = ind_col.index(odd_one_out_nearest)
    odd_one_out_group = pair_col[insert_here]
    pair_col.insert(insert_here, odd_one_out_group)
    ind_col.insert(insert_here, odd_one_out)
    ind_w_group = pd.Series(pair_col, index=ind_col)
ind_w_group


# In[285]:


cleaned_data["groups"] = ind_w_group
cleaned_data


# In[ ]:





# In[288]:


#plot individuals labeled by pair so we can evaluate if the pairs seem correctish
series_shape = cleaned_data["grade"].shape
max_random = 0#names/labels/pts overlap so add randomness to separate them. But remember that this makes them innaccurate
cleaned_data_plot = cleaned_data.copy()

cleaned_data_plot["grade"] = cleaned_data_plot["grade"] + np.random.uniform(0,max_random,series_shape)
cleaned_data_plot["harry_potter"] = cleaned_data_plot["harry_potter"] + np.random.uniform(0,max_random,series_shape)

plt.figure(figsize=(20,10))
my_plot = sns.scatterplot(data=cleaned_data_plot, x="grade", y="harry_potter", hue="groups",palette="tab10", legend=False)
for x, y, label, name in zip(cleaned_data_plot["grade"], cleaned_data_plot["harry_potter"], cleaned_data["groups"], index_to_name.to_list()):
    my_plot.text(x=x, y=y+.05, s="group: "+str(label)+" ind: "+name)


# In[ ]:




