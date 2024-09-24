from load import *

var=pd.read_excel("/home/karthikeyan/vscode/TA/tradingautomationindicators/data/nifty.xlsx")
a=pd.DataFrame({"dis":var["disperative"] , "sma_7":var["sma_7"] , "sma_9":var["sma_9"]})
plt.plot(var['Datetime'],a)
plt.plot(var['Datetime'],var["Unnamed: 11"],marker="x")
plt.title('nifty')
plt.show() 