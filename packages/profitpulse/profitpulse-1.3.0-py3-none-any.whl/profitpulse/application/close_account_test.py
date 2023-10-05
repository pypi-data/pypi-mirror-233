from typing import Optional

import pytest

from profitpulse.account import Account
from profitpulse.account_name import AccountName
from profitpulse.application.close_account import (
    AccountNotFoundError,
    CloseAccountService,
)


class CloseAccountRequest:
    def __init__(self, account_name: str):
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def test_raise_exception_when_account_is_not_found():
    account_name = "TheAccountName"
    request = CloseAccountRequest(account_name)
    accounts = CloseAccountAccountsRepo()
    service = CloseAccountService(accounts)

    with pytest.raises(
        AccountNotFoundError,
        match="Could not find an account with name 'TheAccountName'",
    ):
        service.execute(request)


class CloseAccountAccountsRepo:
    def __init__(self, account: Optional[Account] = None) -> None:
        self._account = account

    @property
    def account_was_closed(self) -> bool:
        if not self._account:
            raise Exception("Expected an account, got None")
        return self._account.closed

    def __getitem__(self, account_name: AccountName) -> Account:
        if not self._account:
            raise KeyError
        return self._account

    def append(self, account: Account):
        self._account = account


def test_close_account_when_the_account_exists():
    account_name = "TheAccountName"
    accounts = CloseAccountAccountsRepo(Account(AccountName(account_name)))
    request = CloseAccountRequest(account_name)
    service = CloseAccountService(accounts)

    service.execute(request)

    assert accounts.account_was_closed  # nosec
