from load import *

def get_history(interval,to_date,from_date,token,oi=True):
    return kite.historical_data(token,from_date,to_date,interval,oi)
    
def get_live_data():
    def on_ticks(ws, ticks):
        # logging.debug("Ticks: {}".format(ticks))
        print(ticks)
        kws.close()
        
    def on_connect(ws, response):
        ws.subscribe([738561])
        ws.set_mode(ws.MODE_FULL, [738561])
        
    def on_close(ws, code, reason):
        ws.stop()
        
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    
    kws.connect()

