import asyncio
import re
from abc import ABC
from contextlib import asynccontextmanager
from typing import Union, AsyncIterator

import aiohttp
from pyrogram import Client

from .exceptions import InvalidData, InvalidCheque
from .utils import Success


async def _to_rub(btc_amount: float) -> float:
    """
    Convert BTC to RUB
    :return: Amount in RUB
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://blockchain.info/ticker') as r:
            response = await r.json()
    btc_price = float(response['RUB']['15m'])
    return btc_amount * btc_price


def _get_cheque_code(cheque: str):
    if re.search(r'BTC_CHANGE_BOT\?start=', cheque):
        return re.findall(r'c_\S+', cheque)[0]
    return cheque


def _validate_params(
        phone_number: str,
        api_hash: str,
        api_id: Union[int, str],
        session_name: str
) -> None:
    """Validate authorization params"""
    if not isinstance(phone_number, str):
        raise InvalidData(
            f"Invalid type of phone_number parameter, required string, "
            f"got {type(phone_number)} instead."
        )

    if not isinstance(api_hash, str):
        raise InvalidData(
            f"Invalid type of api_hash parameter, required string, "
            f"got {type(api_hash)} instead."
        )

    if not isinstance(api_id, int) and not isinstance(api_id, str):
        raise InvalidData(
            f"Invalid type of api_id parameter, required integer/string, "
            f"got {type(api_id)} instead."
        )

    if not isinstance(session_name, str):
        raise InvalidData(
            f"Invalid type of session_name parameter, required string, "
            f"got {type(session_name)} instead."
        )


class BaseWrapper(ABC):
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

        self.phone_number = phone_number
        self.api_hash = api_hash
        self.api_id = api_id
        self.session_name = session_name
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


class BankerWrapper(BaseWrapper):
    async def create_session(self):
        """Create Account Session"""
        await self.app.start()
        await self.app.stop(block=False)

    async def activate_cheque(self, cheque: str):
        """Activate Cheque"""
        code = _get_cheque_code(cheque)
        async with self.connect() as client:
            await asyncio.sleep(1.5)
            await client.send_message('BTC_CHANGE_BOT', f'/start {code}')
            await asyncio.sleep(.7)
            async with asyncio.Lock():
                async for message in client.search_messages(chat_id='BTC_CHANGE_BOT', limit=1):
                    msg = message['text']
            if 'Упс, кажется, данный чек успел обналичить кто-то другой 😟' in msg:
                raise InvalidCheque('Cheque was already activated.')
            elif 'Вы получили' in msg:
                btc = float(re.findall('\d[.]\d+|\d+', msg)[0])
                rub = await _to_rub(btc)
                return Success(rub=rub, btc=btc)
            else:
                raise InvalidCheque("Looks like BTC Banker didn't answer to me or cheque is invalid")
