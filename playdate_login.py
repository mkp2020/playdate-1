#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[31]:


df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vShT1iL5h5WAFoyhmJfjuzKvga3xRopxVfoxaPaEinH9tIgb00eJxzwvgEYQHRf6cHd5xd_mape1ksl/pub?output=csv')
df.columns = ['timestamp', 'name', 'grade', 'major', 'courses', 'interests', 'harry_potter']
df['timestamp'] = pd.to_datetime(df['timestamp'])
df


# In[ ]:





# In[ ]:





# In[ ]:




