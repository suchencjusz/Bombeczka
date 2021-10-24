import asyncio
import os.path
from vulcan import Keystore
from vulcan import Account

async def main():
    if(not os.path.isfile("keystore.json")):
        keystore = Keystore.create(device_model="Bombeczka")
        with open("keystore.json", "w") as f: f.write(keystore.as_json)
    else:
        with open("keystore.json") as f: keystore = Keystore.load(f.read())
        
    token = input("Enter token: ")
    symbol = input("Enter symbol: ")
    pin = str(input("Enter pin: "))

    account = await Account.register(keystore, token, symbol, pin)

    with open("account.json", "w") as f: f.write(account.as_json)

    print("Account registered successful! (Name of device is \"Bombeczka\")")  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())