### 💾Installation

```bash
pip install telecoin
```

---

## Contacts
* 🖱️ __Developer contacts: [![Dev-Telegram](https://img.shields.io/badge/Telegram-blue.svg?style=flat-square&logo=telegram)](https://t.me/marple_tech)__

---

## 🐦Dependencies  

| Library | Description                                            |
|:-------:|:----------------------------------------------:        |
|aiohttp  | Asynchronous HTTP Client/Server for asyncio and Python.|
|pyrogram | Modern Telegram Framework                             |

---

## ↗️ Create Session
```python
import asyncio

from telecoin import BankerWrapper


async def main():
    banker = BankerWrapper(phone_number='Your Number', api_id='Your ID',
                           api_hash='Your Hash',
                           session_name='i_love_telecoin')
    await banker.create_session()


if __name__ == '__main__':
    asyncio.run(main())
```

## 💰 Activate Cheque
```python
import asyncio

import telecoin.exceptions
from telecoin import BankerWrapper


async def main():
    banker = BankerWrapper(phone_number='Your Number', api_id='Your ID',
                           api_hash='Your Hash',
                           session_name='i_love_telecoin')
    await banker.create_session()
    result = await banker.activate_cheque(cheque='https://telegram.me/BTC_CHANGE_BOT?start=c_59500d20eaac0ac2b479382409596b5d')
    try:
        print(f'Received {result.btc} / {result.rub} RUB.')
    except telecoin.exceptions.InvalidCheque:
        print('This is not a valid cheque.')


if __name__ == '__main__':
    asyncio.run(main())

```
