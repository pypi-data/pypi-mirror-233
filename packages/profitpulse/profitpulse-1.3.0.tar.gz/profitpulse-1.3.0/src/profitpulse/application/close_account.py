import typing

from profitpulse.account import Account
from profitpulse.account_name import AccountName


class AccountNotFoundError(Exception):
    def __init__(self, account_name):
        self._account_name = account_name

    def __str__(self):
        return f"Could not find an account with name '{self._account_name}'"


class CloseAccountRequester(typing.Protocol):
    @property
    def account_name(self) -> AccountName:
        ...


class Accounts(typing.Protocol):
    def __getitem__(self, account_name: AccountName) -> Account:
        ...

    def append(self, account: Account):
        ...


class CloseAccountService:
    """
    Closes an account.
    """

    def __init__(self, accounts: Accounts):
        self.accounts = accounts

    def execute(self, request: CloseAccountRequester):
        try:
            account = self.accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(request.account_name)

        account.close()

        self.accounts.append(account)
