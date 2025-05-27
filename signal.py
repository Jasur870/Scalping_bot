from utils import send_telegram_message
import pandas as pd
import requests

BOT_TOKEN = '7706510531:AAEkT4uQ5O8nYLdHxGC-irIkSC9P6PHG0_4'
CHAT_ID = '636914093'
TWELVE_API_KEY = '1c10752e92ea481ca2992336e5700c74'
symbols = ["XAU/USD", "EUR/USD", "GBP/USD", "USD/JPY"]


  # sizning indikator faylingiz
from indikator import calculate_indicators, get_support_resistance


def fetch_data(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=15min&apikey={TWELVE_API_KEY}&outputsize=50"
    response = requests.get(url)
    data = response.json()
    if 'values' not in data:
        raise ValueError(data.get('message', 'API xatosi yuz berdi'))
    df = pd.DataFrame(data['values'])
    df = df.rename(columns={'datetime': 'time'})
    df['time'] = pd.to_datetime(df['time'])
    df = df.astype({'open': float, 'high': float, 'low': float, 'close': float})
    return df.sort_values('time')

async def analyze_and_send_signal():
    
    send_telegram_message(BOT_TOKEN, CHAT_ID, "Tahlil boshlandi...")
    
    for symbol in symbols:
        try:
            df = fetch_data(symbol)
            df = calculate_indicators(df)
            last = df.iloc[-1]
            levels = get_support_resistance(df)

            buy_signal = (
                last['RSI'] < 30 and
                last['close'] > last['EMA20'] and
                last['MACD'] > last['MACD_signal'] and
                last['close'] > levels['support']
            )
            sell_signal = (
                last['RSI'] > 70 and
                last['close'] < last['EMA20'] and
                last['MACD'] < last['MACD_signal'] and
                last['close'] < levels['resistance']
            )

            if buy_signal:
                msg = (f"{symbol} uchun BUY signal!\n"
                       f"NARX: {last['close']}\n"
                       f"Support: {levels['support']}\n"
                       f"Resistance: {levels['resistance']}")
            elif sell_signal:
                msg = (f"{symbol} uchun SELL signal!\n"
                       f"NARX: {last['close']}\n"
                       f"Support: {levels['support']}\n"
                       f"Resistance: {levels['resistance']}")
            else:
                msg = f"{symbol} uchun signal yo‘q."

            send_telegram_message(BOT_TOKEN, CHAT_ID, msg)

        except Exception as e:
            print(f"{symbol} uchun xato: {e}")