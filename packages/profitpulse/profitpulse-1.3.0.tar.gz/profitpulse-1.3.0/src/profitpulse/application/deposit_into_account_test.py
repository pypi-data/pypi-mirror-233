import pytest

from profitpulse.account import Account
from profitpulse.account_name import AccountName
from profitpulse.application.deposit_into_account import (
    AccountDoesNotExistError,
    ServiceDepositIntoAccount,
)
from profitpulse.comment import Comment
from profitpulse.money import Money


class AccountsNoAccount:
    def __getitem__(self, account_name):
        raise KeyError

    def __setitem__(self, account_name, account):
        pass


class DepositInAccountRequest:
    @property
    def account_name(self) -> AccountName:
        return AccountName("TheAccountName")

    @property
    def comment(self) -> Comment:
        return None

    @property
    def amount(self) -> Money:
        return Money(100)


def test_raise_error_if_account_does_not_exist():
    request = DepositInAccountRequest()
    accounts = AccountsNoAccount()

    service = ServiceDepositIntoAccount(accounts)
    with pytest.raises(AccountDoesNotExistError, match="Account does not exist"):
        service.execute(request)


class Accounts:
    def __init__(self, account: Account) -> None:
        self._account = account
        self.account_added = False

    def __getitem__(self, account_name) -> Account:
        return self._account

    def __setitem__(self, account_name, account: Account):
        self.account_added = True
        self._account = account


def test_save_deposit_into_account():
    request = DepositInAccountRequest()
    account = Account(AccountName("TheAccountName"))
    accounts = Accounts(account)

    service = ServiceDepositIntoAccount(accounts)

    service.execute(request)

    assert accounts.account_added  # nosec
    assert account.last_comment is None  # nosec


class DepositInAccountWithCommentRequest:
    @property
    def account_name(self) -> AccountName:
        return AccountName("TheAccountName")

    @property
    def comment(self) -> Comment:
        return Comment("A comment")

    @property
    def amount(self) -> Money:
        return Money(100)


def test_inject_the_comment_into_the_account_deposit_when_one_is_defined():
    request = DepositInAccountWithCommentRequest()
    account = Account(AccountName("TheAccountName"))
    accounts = Accounts(account)

    service = ServiceDepositIntoAccount(accounts)

    service.execute(request)

    assert accounts.account_added  # nosec
    assert_string_equals("A comment", account.last_comment)


# TODO: move to toolcat
def assert_string_equals(expected: str, got):
    """
    Compares an object objects in it's string value and raises an AssertionError
    if it's not equal to the expected value.
    """
    __tracebackhide__ = True
    assert str(got) == expected, f"Expected {expected}, got {got}"  # nosec
