import re
from dataclasses import dataclass
from typing import Union

from .exceptions import InvalidateCredentials


def get_cheque_code(cheque: str):
    """Get code"""
    if (
            re.search(r'BTC_CHANGE_BOT\?start=', cheque)
            or not re.search(r'BTC_CHANGE_BOT\?start=', cheque)
            and re.search(r'Chatex_bot\?start=', cheque)
    ):
        return re.findall(r'c_\S+', cheque)[0]
    elif re.search(r'Getwallet_bot\?start=', cheque):
        return re.findall(r'g_\S+', cheque)[0]
    return cheque


def _validate_params(
        phone_number: str,
        api_hash: str,
        api_id: Union[int, str],
        session_name: str
) -> None:
    """Validate authorization params"""
    if not isinstance(phone_number, str):
        raise InvalidateCredentials(
            f"Invalid type of phone_number parameter, required string, "
            f"got {type(phone_number)} instead."
        )

    if not isinstance(api_hash, str):
        raise InvalidateCredentials(
            f"Invalid type of api_hash parameter, required string, "
            f"got {type(api_hash)} instead."
        )

    if not isinstance(api_id, int) and not isinstance(api_id, str):
        raise InvalidateCredentials(
            f"Invalid type of api_id parameter, required integer/string, "
            f"got {type(api_id)} instead."
        )

    if not isinstance(session_name, str):
        raise InvalidateCredentials(
            f"Invalid type of session_name parameter, required string, "
            f"got {type(session_name)} instead."
        )


@dataclass
class Result:
    rub: float
    btc: float
