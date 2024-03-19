import requests
import json
from config import curr


class APIException(Exception):
    pass


class Conversion:
    @staticmethod
    def get_price(base: str, quote: str, amount:str):
        if base == quote:
            raise APIException(f'Вы пытаетесь конвертировать одинаковые валюты: {base}')

        try:
            available_base = curr[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}. \n'
                               'Доcтупные валюты можно увидеть по команде /values')

        try:
            available_quote = curr[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}. \n'
                               'Доcтупные валюты можно увидеть по команде /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}. \n'
                               'Инструкцию по вводу можно увидеть по команде /help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={available_base}&tsyms={available_quote}')
        total_quote = json.loads(r.content)[curr[quote]] * float(amount)

        return total_quote
