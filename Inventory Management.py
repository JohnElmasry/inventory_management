#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries
# 
# Note : Sympy Library Converts the string to mathematical variable , So instead of 2*'x' = xx , it is 2x

# In[1]:


import pandas as pd
import numpy as np
import string
import sympy as sym


# # Importing the sheet of predicted price and quanitity needed

# In[2]:


df=pd.read_csv("Predicted Prices and Quantity.csv")
df


# # Importing the sheet of assumptions, which explains different costs variables

# In[3]:


df2=pd.read_csv("assumptions.csv",index_col=0)
df2


# Function to Add the Variables of Quantites to be ordered

# In[4]:


def add_quantities(df):
    df['Quantity to be ordered']=None
    for i in range(len(df)):
        df['Quantity to be ordered'][i]=sym.Symbol('x'+str(i))
        
    return df


# In[5]:


add_quantities(df)


# Start Adding Columns of Different costs as functions of "Quantity to be Ordered" Column

# In[6]:


df['Quantity Left']=None

df


# The First row of quantity left is different from the other rows

# In[7]:


df['Quantity Left'][0]=df['Quantity to be ordered'][0]-df['Quantity_Needed'][0]
df


# In[8]:


for i in range(1,len(df)):
    df['Quantity Left'][i]=df['Quantity Left'][i-1]+df['Quantity to be ordered'][i]-df['Quantity_Needed'][i]
df


# In[9]:


df['Material Cost']=df['Quantity to be ordered']*df['Predicted_Price']
df


# In[10]:


df['Storage Cost']=df['Quantity Left']*float(df2.iloc[1,0])
df


# In[11]:


df['Handling Cost']=df['Quantity to be ordered']*float(df2.iloc[2,0])
df


# In[12]:


df['Taxes and Insurance']=df['Quantity to be ordered']*float(df2.iloc[3,0])
df


# In[13]:


df['Damage Cost']=df['Predicted_Price']*df['Quantity Left']*(float(df2.iloc[4,0].replace('%',''))/100)
df


# In[14]:


df['Purchase Cost']=df['Predicted_Price']*df['Quantity to be ordered']*float(df2.iloc[7,0])
df


# In[15]:


df['Ordering Cost']=df['Quantity to be ordered']*float(df2.iloc[5,0])
df


# In[16]:


df['Total Cost']=df['Material Cost']+df['Storage Cost']+df['Handling Cost']+df['Taxes and Insurance']+df['Damage Cost']+df['Purchase Cost']+df['Ordering Cost']
df


# In[17]:


df['Present Value']=None
df


# In[18]:


1+float(df2.iloc[6,0].replace('%',''))


# Covert all the costs to the present value to compare different Hypothesis as an apple to an apple

# In[19]:



for i in range(len(df)):
    df['Present Value'][i]=df['Total Cost'][i]/(1+float(df2.iloc[6,0].replace('%','')))**i
df


# This is the function of the total price that we will need to minimize it using Sklearn.Optimize Algorithm

# In[20]:


total_price = df['Present Value'].sum()
total_price


# Covert the function from sympy data type to string, to manipulate the string and change each X with a subscription of initial guess list 
# So x0 will be x[0] ... etc

# In[21]:


eqn = str(total_price)
eqn


# In[22]:


def replacement(string):
    for i in range(len(df)):
        string=string.replace('x{}'.format(i),'x[{}]'.format(i))
    return string


# In[23]:


eqn=replacement(eqn)
eqn


# In[24]:


parameters=list(df['Quantity to be ordered'].values)
parameters


# In[25]:


storage_capacity=int(df2.Value[-1])
storage_capacity


# In[26]:


total_qty=int(df2.Value[0])
total_qty


# Here we need to define some constraints for the Quantity to be ordered variables :
# 1. Quantity left should be Positive ( more_const ) list
# 2. Quantity left should be less than the storage size ( less_const ) list
# 
# Note : We need the function always positive, for example x0+x1 >0

# In[27]:


# Constraints that we order more than or equal we need , Quantity left >=0

more_const=list(df['Quantity Left'])
more_const


# In[28]:


# Constraints that we order less than or equal inventory size
less_const=[]

for i in list(df['Quantity Left']):
    less_const.append(-i+storage_capacity)
    
less_const


# apply the replacement function again on each element of both lists to change the variables to subscription

# In[29]:


more_const2=[]
for i in more_const:
    i=replacement(str(i))
    more_const2.append(i)
more_const2


# In[30]:


less_const2=[]
for i in less_const:
    i=replacement(str(i))
    less_const2.append(i)
less_const2


# append the two constraints lists as one list

# In[31]:


all_const=more_const2+less_const2
all_const


# we need to put each constraint as a form of dictionary and all the constrants as a tuple 
# 
# the dictionary of the constraint should be { 'type' : 'eq or ineq' , 'fun' : lambda x : the equation 

# In[39]:


con=[]
x=[]
for i in all_const:
    single_con={'type': 'ineq','fun': eval('lambda x:{}'.format(i))}
    con.append(single_con)
con.append({'type': 'eq','fun': lambda x: sum(x)-total_qty})

con_tuple=tuple(con)
con_tuple


# In[44]:


import scipy.optimize as optimize

def f(x):
    #df['Quantity to be ordered'].values = params # <-- for readability you may wish to assign names to the component variables
    return eval(eqn)

initial_guess = [storage_capacity/6, storage_capacity/6,storage_capacity/6,storage_capacity/6,storage_capacity/6,storage_capacity/6]

bound= ((df['Quantity_Needed'][0],storage_capacity+df['Quantity_Needed'][0]),(0,2*storage_capacity),(0,2*storage_capacity),(0,2*storage_capacity),(0,2*storage_capacity),(0,2*storage_capacity))
result = optimize.minimize(f, initial_guess,bounds=bound,constraints =con_tuple)
if result.success:
    fitted_params = result.x
    print(fitted_params)
else:
    raise ValueError(result.message)


# In[45]:


list(fitted_params)


# In[46]:


Qty=[]
for i in list(fitted_params):
    Qty.append(int(round(i,0)))
Qty


# In[47]:


x=Qty
lowest=eval(eqn)
lowest


# Another Solution is Genetic Algorithm

# In[37]:



# #X is an array of the inputs 
# def f(X):
#     pen=0
#     if X[0]+X[1]+X[2]+X[3]+X[4]+X[5]!=740:
#         pen=500+1000*(2-X[0]-X[1])
#     return 12010.3028754279*X[0]+12180.4952784826*X[1]+12841.8025208041*X[2]+17260.6392193953*X[3]+12774.2000084253*X[4]+14172.0168286208*X[5]#−674077.793716568

# varbound=np.array([[0,400]]*6) #Boundary for each x

# model=ga(function=f,dimension=6,variable_type='int',variable_boundaries=varbound)

# model.run()

