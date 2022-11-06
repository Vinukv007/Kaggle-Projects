# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZM36u3Q2zgti7oSwmJqVU_ro61xekATH

### 3. Mobile Price Prediction

---
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import re

df=pd.read_csv('mobile_price_data.csv')
df.head()

df.drop_duplicates(inplace=True)

df.info()

df.columns

# dropping columns that doesnt influence the price

df.drop(['mobile_color', 'dual_sim', 'bluetooth', 'mob_width',
       'mob_height', 'mob_depth', 'mob_weight'],1,inplace=True)
df.info()

df.columns

# All the columns are strings. extracting digits or names from them 

# Creating new column 'brand' to give brand value influence over price

df['brand']=df.mobile_name.str.extract(r"(\w+)")

df.brand[df.brand=='MI3']='Mi'
df.brand.unique()

df['price(Rs.)']=df.mobile_price.str.extract(r"(\d+)")+df.mobile_price.str.extract(r",(\d+)")

df['display(cm)']=df.disp_size.str.extract(r"([0-9\.]+)")

df['res']=df.resolution.str.extract(r"(720|1080|540)")

df['cores']=df.num_cores.map({'Octa Core':8, 'Quad Core':4, 'Single Core':1})

df['clock_speed(GHz)']=df.mp_speed.str.extract(r"([0-9\.])")

df['storage']=df.int_memory.str.extract(r"(\d+)")

df['ram']=df.ram.str.extract(r"(\d+)")

df['primary_cam(MP)']=df.p_cam.str.extract(r"(\d+)")

df['back_camera_count']=df.p_cam.str.count(r"(\d+)")

df['front_cam(MP)']=df.f_cam.str.extract(r"(\d+)")

df['bands']=df.network.str.extract(r"(4G)")
df.bands[df.network=='3G']='3G'
df.bands[df.network=='2G']='2G'

df['battery(Mah)']=df.battery_power.str.extract(r"(\d+)")

#dropping duplicate columns

df.drop([ 'mobile_price', 'disp_size', 'resolution', 'os',
       'num_cores', 'mp_speed', 'int_memory', 'ram', 'p_cam', 'f_cam',
       'network', 'battery_power'],1,inplace=True)
df.info()

df.head()

df.columns

# converting columns to appropriate datatypes

for i in [ 'price(Rs.)', 'res', 'cores'
       , 'storage', 'primary_cam(MP)', 'back_camera_count',
       'front_cam(MP)', 'battery(Mah)']:
       df[i]=df[i].astype(int)

df['display(cm)']=df['display(cm)'].astype(float)
df['clock_speed(GHz)']=df['clock_speed(GHz)'].astype(float)

df.info()

# encoding bands columns according to importance

df.bands=df.bands.map({'4G':3, '3G':2, '2G':1})

from sklearn.preprocessing import MinMaxScaler

mms=MinMaxScaler()

df['res_scaled']=mms.fit_transform(df[['res']])

x=df[['display(cm)', 'cores',
       'clock_speed(GHz)', 'storage', 'primary_cam(MP)', 'back_camera_count',
       'front_cam(MP)', 'bands', 'battery(Mah)', 'res_scaled']]
y=df['price(Rs.)']

new_x=pd.concat([x,pd.get_dummies(df.brand,prefix='brand')],1)
new_x.drop('brand_Mi',1,inplace=True)
xtrain,xtest,ytrain, ytest=train_test_split(new_x,y,test_size=0.2, random_state=2)

from sklearn.linear_model import LinearRegression
lreg=LinearRegression()

lreg.fit(xtrain,ytrain)
lreg.score(xtest,ytest)

from sklearn.tree import DecisionTreeRegressor
dtr=DecisionTreeRegressor()

dtr.fit(xtrain,ytrain)
dtr.score(xtest,ytest)
