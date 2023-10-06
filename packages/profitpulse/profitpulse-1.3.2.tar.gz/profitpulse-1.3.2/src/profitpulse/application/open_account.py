import typing
from typing import Optional

from profitpulse.account import Account
from profitpulse.account_name import AccountName


class AccountAlreadyExistsError(Exception):
    def __str__(self):
        return "An account with the same name already exists"


class Accounts(typing.Protocol):
    def get(self, account_name: AccountName) -> Optional[Account]:
        ...

    def __setitem__(self, account_name, account: Account):
        ...


class OpenAccountRequester(typing.Protocol):
    @property
    def account_name(self) -> AccountName:
        ...


class OpenAccountService:
    def __init__(self, accounts: Accounts):
        self.accounts = accounts

    def execute(self, request: OpenAccountRequester):
        if self.accounts.get(request.account_name):
            raise AccountAlreadyExistsError()

        account = Account(request.account_name)
        self.accounts[request.account_name] = account
