import requests

def get_usd_kes_rate():
    """
    Fetches the current USD/KES exchange rate from the Frankfurter API.
    Frankfurter wraps its response in a list ,
    Index into [0] before pulling the 'rate' key.
    """
    frank_url="https://api.frankfurter.dev/v2/rates?base=USD&quotes=KES"
    frank_res=requests.get(frank_url)
    frank_data=frank_res.json()  #
    rate=frank_data[0]
    usdksh_rate=rate['rate']
    return usdksh_rate

def get_crypto_prices(symbols):
    """
    Fetches live USD spot prices from Binance for each symbol passed in.
    Binance wraps its response in a dictionary
    Index into price key to convert it from string to float.
    """
    usd_prices = {}

    for btc in symbols:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={btc}"
        res = requests.get(url)
        data = res.json()
        price = float(data['price'])
        usd_prices[btc] = round(price,2)

    return usd_prices
