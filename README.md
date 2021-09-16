### 💾Installation

```bash
pip install telecoin
```

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
'''
