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
result=minimize(sharp_ratio_calculate,x0=w0,bounds=boundss,constraints=constrainsss)




##### we have change a lot
