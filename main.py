import asyncio
from signal import analyze_and_send_signal

async def runner():
    while True:
        await analyze_and_send_signal()
        await asyncio.sleep(600)

loop = asyncio.get_event_loop()
loop.run_until_complete(runner())

if __name__ == '__main__':
    print("Scalping signal bot ishga tushdi...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(signal_loop())