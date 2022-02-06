import abc
import asyncio
import re
from contextlib import asynccontextmanager
from typing import Union, AsyncIterator

import aiohttp
from pyrogram import Client

from .exceptions import InvalidCheque
from .utils import _validate_params, get_cheque_code, Result


class BaseWrapper:
    def __init__(self, phone_number: str, api_hash: str, api_id: Union[str, int], session_name: str) -> None:
        """
        :param phone_number: Telegram Phone Number
        :param api_hash: The *api_hash* part of your Telegram API Key (visit https://my.telegram.org/auth?to=apps)
        :param api_id: The *api_id* part of your Telegram API Key (visit https://my.telegram.org/auth?to=apps)
        :param session_name: Session Name
        """
        _validate_params(
            phone_number=phone_number,
            api_hash=api_hash,
            api_id=api_id,
            session_name=session_name
        )

        self.session = aiohttp.ClientSession
        self.app = Client(
            phone_number=phone_number,
            api_hash=api_hash,
            api_id=api_id,
            session_name=session_name
        )

    @asynccontextmanager
    async def connect(self) -> AsyncIterator:
        """Create connection"""
        try:
            if not self.app.is_connected:
                await self.app.start()
            yield self.app
        except Exception as ex:
            print(ex)
        finally:
            if self.app.is_connected:
                await self.app.stop(block=False)

    async def create_session(self):
        """Create Account Session"""
        await self.app.start()
        await self.app.stop(block=False)

    async def to_rub(self, btc_amount: float) -> float:
        """
        Convert BTC to RUB
        :return: Amount in RUB
        """
        async with self.session() as session:
            async with session.get('https://blockchain.info/ticker') as r:
                response = await r.json()
        btc_price = float(response['RUB']['15m'])
        return btc_amount * btc_price


class BankerWrapper(BaseWrapper):
    async def activate_cheque(self, cheque: str):
        """Activate Cheque"""
        code = get_cheque_code(cheque)
        async with self.connect() as client:
            await asyncio.sleep(1.5)
            await client.send_message('BTC_CHANGE_BOT', f'/start {code}')
            await asyncio.sleep(1.5)
            messages = await client.get_history("@BTC_CHANGE_BOT")
            message_text = messages[0].text
        if 'Упс, кажется, данный чек успел обналичить кто-то другой 😟' in message_text:
            raise InvalidCheque('Cheque was already activated.')
        elif 'Вы получили' in message_text:
            btc = float(re.findall('\d[.]\d+|\d+', message_text)[0])
            rub = await self.to_rub(btc)
            return Result(rub=rub, btc=btc)
        else:
            raise InvalidCheque("Looks like BTC Banker didn't answer to me or cheque is invalid")


class GetWalletWrapper(BaseWrapper):
    async def activate_cheque(self, cheque: str):
        """Activate Cheque"""
        code = get_cheque_code(cheque)
        async with self.connect() as client:
            await asyncio.sleep(1.5)
            await client.send_message('Getwallet_bot', f'/start {code}')
            await asyncio.sleep(1.5)
            messages = await client.get_history("@Getwallet_bot")
            message_text = messages[0].text
        if '😮 Увы, но данный купон не существует' in message_text:
            raise InvalidCheque('Cheque was already activated.')
        elif 'Подарочный код активирован' in message_text:
            btc = float(re.findall('\d[.]\d+|\d+', message_text)[0])
            rub = await self.to_rub(btc)
            return Result(rub=rub, btc=btc)
        else:
            raise InvalidCheque("Looks like GetWallet didn't answer to me or cheque is invalid")