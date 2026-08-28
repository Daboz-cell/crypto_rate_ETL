def transform_prices(usd_prices, usd_kes_rate):
    """
    Converts USD crypto prices into KES using the given exchange rate.
    
    """
    records = []
    for symbol in usd_prices:
        usd_price = usd_prices[symbol]
        ksh_price = round(usd_price * usd_kes_rate,2)
        records.append({
            "symbol": symbol,
            "usd_price": usd_price,
            "ksh_price": ksh_price
        })

    return records


    

   
