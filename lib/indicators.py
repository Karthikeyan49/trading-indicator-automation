def vwap_ind(data):
    # VWAP = Σ(Pi * Vi) / ΣVi
    vwap = (((data['High'] + data['Low'] + data['Close']) / 3) * data['Volume']).cumsum() / data['Volume'].cumsum()
    return vwap

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
    
def get_di(data, lookback):
    ma = data.rolling(lookback).mean()
    di = ((data - ma) / ma) * 100
    return di