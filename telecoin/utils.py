from dataclasses import dataclass


@dataclass
class Cheque:
    rub: float
    btc: float


def configure(rub: float, btc: float):
    return Cheque(rub=rub,
                  btc=btc)
