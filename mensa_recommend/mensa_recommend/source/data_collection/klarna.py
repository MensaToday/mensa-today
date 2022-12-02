from .utils import Collector
import requests
from mensa.models import CardBalance
from users.models import User
from typing import Union
import global_data


class KlarnaCollector(Collector):

    def __init__(self):
        self.url_pattern = 'https://api.topup.klarna.com/api/v1/STW_MUNSTER/cards/{card_id}/balance'

    def run(self) -> None:
        users = User.objects.exclude(card_id__isnull=True)

        card_balances = []
        for user in users:
            balance = self.__get_current_balance(user.card_id)

            if balance:
                card_balances.append(CardBalance(balance=balance, user=user))

        self.save_balance(card_balances=card_balances)

    def get_current_balance(self, card_id: str) -> Union[float, None]:

        klarna_url = self.url_pattern.format(card_id=card_id)

        balance: float

        try:
            response = requests.get(klarna_url, proxies=global_data.proxies)
            response_json = response.json()

            if response.status_code == 404:
                return None

            if 'balance' in response_json:
                balance = response_json['balance']
        except requests.exceptions.RequestException as error:
            raise SystemError(error) from error

        return balance/100

    def save_balance(self, user: User = None, card_balances=None) -> None:

        if card_balances:
            CardBalance.objects.bulk_create(card_balances)
        elif user:
            if user.card_id:
                balance = self.__get_current_balance(user.card_id)
                if balance:
                    card_balance = CardBalance(balance=balance, user=user)
                    card_balance.save()
                else:
                    return card_balance
