from load import *

def authenticate():
    it=webbrowser.open_new_tab(kite.login_url())
    print(it)
    request_token=input("enter the token : ")
    data = kite.generate_session(request_token, api_secret=get_api_config("api_secret"))
    access_token=data['access_token']
    file=open('/home/karthikeyan/vscode/TA/trading automation data/data.json','r')    
    api_info=json.load(file)
    file.close()
    api_info["access_token"]=access_token
    file=open('/home/karthikeyan/vscode/TA/trading automation data/data.json','w')    
    json.dump(api_info,file)
    file.close()
    return access_token
  
authenticate()
