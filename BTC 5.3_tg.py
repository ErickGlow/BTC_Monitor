import requests
import time
import winsound
import telebot
import json

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Telegram Bot Token and Chat ID
token = config['token']
CHANNEL_NAME = config['channel_name']
bot = telebot.TeleBot(token)

def get_price():
     url = "https://api.bybit.com/v2/public/tickers"
     params = {
         "symbol": config['symbol']
     }

     try:
         response = requests.get(url, params=params)
         response.raise_for_status()
         data = response.json()
         if data['ret_code'] == 0:
             price = data['result'][0]['last_price']
             return float(price)
         else:
             print("Error retrieving price:", data['ret_msg'])
     except requests.exceptions.RequestException as e:
         print("Error retrieving price:", str(e))

     return None

def print_price(price):
     print(f"BTC/USDT Price: {price}")

def send_telegram_message(message):
     bot.send_message(CHANNEL_NAME, text=message)

previous_price = get_price()

while True:
     current_price = get_price()
     if current_price is not None:
         price_diff = previous_price - current_price
         if price_diff >= 50:
             print("Price fell by 50 USDT or more per minute!")
             winsound.Beep(1000, 2000) # Beep sound for 2 seconds
             send_telegram_message("Price of BTC/USDT fell by 50 USDT or more per minute!")
         previous_price = current_price
         print_price(current_price)
     time.sleep(3)
