import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl
from scipy.optimize import minimize


aaple=pd.read_csv(r"C:\Users\leilypour\Python-for-Finance-Repo-master\09-Python-Finance-Fundamentals\AAPL_CLOSE",index_col='Date',parse_dates=True)
cisco=pd.read_csv(r"C:\Users\leilypour\Python-for-Finance-Repo-master\09-Python-Finance-Fundamentals\CISCO_CLOSE",index_col='Date',parse_dates=True)
ibm=pd.read_csv(r"C:\Users\leilypour\Python-for-Finance-Repo-master\09-Python-Finance-Fundamentals\IBM_CLOSE",index_col='Date',parse_dates=True)
amzn=pd.read_csv(r"C:\Users\leilypour\Python-for-Finance-Repo-master\09-Python-Finance-Fundamentals\AMZN_CLOSE",index_col='Date',parse_dates=True)

stocks=pd.concat([aaple,cisco,ibm,amzn],axis=1)
stocks.columns=['Apple','cisco','ibm','amzn']

### Moshabeh in code stocks.pct_change(1)....Darsad Taghyir har roz nesbat be roze ghabl
log_return=np.log(stocks/stocks.shift(1))


np.random.seed(101) #### Make sure that always we will have the same random number


retail=stocks


def generate_weights(N):
    weights=np.random.random(N)
    
    return weights/np.sum(weights)


def calculate_return(weight,logarithmic_return):
   return np.sum(logarithmic_return.mean()*weight)*252


def calculate_volatility(weight,log_return_covarience):
    anualized_volatility=np.dot(weight,log_return_covarience)
    volatility=np.dot(weight.transpose(),anualized_volatility)*252 #*252 to anualize it
    return np.sqrt(volatility)



mc_volatility=[]
mc_return=[]
mc_weights=[]


for sim in range(3000):
    weights=generate_weights(N=4)
    mc_weights.append(weights)
    mc_return.append(calculate_return(weights,log_return))
    mc_volatility.append(calculate_volatility(weights,log_return.cov()))
mc_sharpRatio=np.array(mc_return)/np.array(mc_volatility)
 

   
plt.figure(dpi=200,figsize=(10,5))

plt.scatter(np.array(mc_volatility),np.array(mc_return),c=mc_sharpRatio)
plt.colorbar(label="Sharp Ratio")
plt.xlabel("Volatility")
plt.ylabel("Return")
    

########################### Optimization part #############################

from scipy.optimize import minimize

def sharp_ratio_calculate(weight):
    Profit=calculate_return(weight,log_return)
    volatility=calculate_volatility(weight,log_return.cov())
    SP=np.array(Profit)/np.array(volatility)
    return -SP


w0=list(1/4 for n in range(4))

boundss=tuple((0,1) for n in range(4))
constrainsss={'type':'eq','fun': lambda weight:np.sum(weight)-1}
minimize(sharp_ratio_calculate,x0=w0,bounds=boundss,constraints=constrainsss)
















