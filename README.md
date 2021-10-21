[![Downloads](https://pepy.tech/badge/telecoin)](https://pepy.tech/project/telecoin)
[![Downloads](https://pepy.tech/badge/telecoin/month)](https://pepy.tech/project/telecoin)[![Downloads](https://pepy.tech/badge/telecoin/week)](https://pepy.tech/project/telecoin)
![Score](https://www.code-inspector.com/project/29472/score/svg)
![Score](https://www.code-inspector.com/project/29472/status/svg)

### 💾 Installation

```bash
pip install telecoin
```

---

## 📞 Contacts
* 🖱️ __Developer contacts: [![Dev-Telegram](https://img.shields.io/badge/Telegram-blue.svg?style=flat-square&logo=telegram)](https://t.me/marple_tech)__

---

## 🐦 Dependencies  

| Library | Description                                            |
|:-------:|:----------------------------------------------:        |
|aiohttp  | Asynchronous HTTP Client/Server for asyncio and Python.|
|pyrogram | Modern Telegram Framework                             |

---


## ❔ What is this? 
* This is simple library to activate @BTC_CHANGE_BOT, @Chatex_bot, @GetWallet_bot gift cheque. 


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

---

## 💰 Activate Cheque
```python
import asyncio

import telecoin.exceptions
from telecoin import BankerWrapper


async def main():
    banker = BankerWrapper(phone_number='Your Number', api_id='Your ID',
                           api_hash='Your Hash',
                           session_name='i_love_telecoin')
    try:
        result = await chatex.activate_cheque('https://telegram.me/BTC_CHANGE_BOT?start=c_ae0f629a49fd1b494b371c0ec64d1v21')
        print(f'Received {result.btc} BTC / {result.rub} RUB')
    except InvalidCheque:
        print('Cheque is not valid')


if __name__ == '__main__':
    asyncio.run(main())

```

---

