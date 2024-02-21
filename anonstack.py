import os
import requests
import locale
from datetime import datetime
import time

# title
title_art = """
 █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗   ███████╗████████╗ █████╗  ██████╗██╗  ██╗
██╔══██╗████╗  ██║██╔═══██╗████╗  ██║   ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
███████║██╔██╗ ██║██║   ██║██╔██╗ ██║   ███████╗   ██║   ███████║██║     █████╔╝ 
██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║   ╚════██║   ██║   ██╔══██║██║     ██╔═██╗ 
██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║██╗███████║   ██║   ██║  ██║╚██████╗██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""

# subtitle
subtitle = "::A P2P TRADE ASSISTANT::"

# closing header
transaction_art = """
 _   _                   __                        _              
| |_| |__  _ __ __  __  / _| ___  _ __   _   _ ___(_)_ __   __ _  
| __| '_ \| '_ \\ \/ / | |_ / _ \| '__| | | | / __| | '_ \ / _` | 
| |_| | | | | | |>  <  |  _| (_) | |    | |_| \__ \ | | | | (_| | 
 \__|_| |_|_| |_/_/\_\ |_|  \___/|_|     \__,_|___/_|_| |_|\__, | 
  __ _ _ __   ___  _ __    ___| |_ __ _  ___| | __         |___/  
 / _` | '_ \ / _ \| '_ \  / __| __/ _` |/ __| |/ /                
| (_| | | | | (_) | | | |_\__ \ || (_| | (__|   <                 
 \__,_|_| |_|\___/|_| |_(_)___/\__\__,_|\___|_|\_\                              
"""

# title and subtitle
print(title_art)
print(subtitle)

# cost + markup
def calculate_total_cost(price, markup_percentage):
    total_cost = price * (1 + markup_percentage / 100)
    return total_cost

# load bar
def loading_bar(message):
    for _ in range(10):
        print(".", end="", flush=True)
        time.sleep(0.2)  # Adjust the delay as needed
    print(message)

# coinmarketcap API
def get_bitcoin_price(api_key):
    loading_bar("loading prices... ")
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'X-CMC_PRO_API_KEY': 'your_api_key'
    }
    parameters = {
        'symbol': 'BTC'
    }
    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        price = data['data']['BTC']['quote']['USD']['price']
        return price
    except requests.exceptions.RequestException as e:
        print("Error getting BTC price:", e)
        return None
    except KeyError as e:
        print("Error parsing response data:", e)
        return None

# format fiat
def format_price(price):
    locale.setlocale(locale.LC_ALL, '')  # Set locale to user's default
    return locale.format_string("%.2f", price, grouping=True)

# format bitcoin
def format_bitcoin(amount):
    return "{:.8f}".format(amount)

# fee estimator
def estimate_fee(confirmation_block_time):
    try:
        url = "https://mempool.space/api/v1/fees/recommended"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        fee_data = response.json()
        fee_rate = fee_data['fastestFee']  # Assuming 'fastestFee' represents the required fee rate
        total_fee = fee_rate * confirmation_block_time / 100000000  # Convert satoshis to BTC
        return fee_rate, total_fee
    except requests.exceptions.RequestException as e:
        print("Error fetching fee rate:", e)
        return None, None
    except KeyError as e:
        print("Error parsing response data:", e)
        return None, None

# buyer receipt
def print_receipt(fiat_amount, total_cost, bitcoin_amount, fee_rate, total_fee):
    print("\nBUYER RECEIPT:")
    print("Buy amount: $", format_price(fiat_amount))
    print("Rate: 1 BTC = $", format_price(total_cost))
    print("Bitcoin receiving:", format_bitcoin(bitcoin_amount), "BTC")
    print("Fee rate:", format_price(fee_rate), "sat/vb")
    print("Total fee:", format_bitcoin(total_fee), "BTC")
    print("Date:", datetime.utcnow().strftime("%m-%d-%Y, %H:%M:%S UTC"))

# main function
def main():
    coinmarketcap_api_key = os.getenv("COINMARKETCAP_API_KEY")
    if coinmarketcap_api_key is None:
        print("CoinMarketCap API key not found.")
        return
    
    while True:
        # current bitcoin price
        print("\nLaunching app.....")
        bitcoin_price = get_bitcoin_price(coinmarketcap_api_key)
        if bitcoin_price is None:
            return

        print()
        
        print("CURRENT BTC PRICE")
        print("1 BTC = $", format_price(bitcoin_price))

        # buyer's asking amount
        print("\nENTER BUY/SELL AMOUNT (dollars):")
        fiat_amount_str = input().replace(',', '')
        try:
            fiat_amount = round(float(fiat_amount_str), 2)
        except ValueError:
            print("Invalid input. Please enter a valid numerical value.")
            continue

        # markup
        print("\nMARKUP PERCENTAGE:")
        markup_percentage_str = input().replace(',', '')
        try:
            markup_percentage = round(float(markup_percentage_str), 2)
        except ValueError:
            print("Invalid input. Please enter a valid numerical value.")
            continue

        # subtotal
        total_cost = calculate_total_cost(bitcoin_price, markup_percentage)

        # bitcoin to sell
        bitcoin_amount = round(fiat_amount / total_cost, 8)
        print("\nBITCOIN TO SELL:")
        print(format_bitcoin(bitcoin_amount), "BTC")

        # fee estimator
        print("\nFEE ESTIMATOR")
        print("# of Conf Blocks (1, 6, 12, 24):")
        confirmation_block_time = int(input())
        print()
        fee_rate, total_fee = estimate_fee(confirmation_block_time)
        if fee_rate is not None:
            print("Fee rate: ", format_price(fee_rate), " sat/vb")
            print("Total fee: ", format_bitcoin(total_fee), "BTC")
        else:
            print("Failed to estimate fee rate")

        # grand total
        grand_total = round(bitcoin_amount + total_fee, 8)
        print("\nGRAND TOTAL")
        print(format_bitcoin(grand_total), "BTC")
        
        # buyer receipt
        print_receipt(fiat_amount, total_cost, bitcoin_amount, fee_rate, total_fee)
        print()

        while True:
            choice = input("Do you want to do another transaction? (y/n): ").lower()
            if choice == 'no' or choice == 'n':
                print(transaction_art)
                print()
                print("Have a great one.")
                print()
                print("made by @rarepassenger")
                print()
                return
            elif choice == 'yes' or choice == 'y':
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()

