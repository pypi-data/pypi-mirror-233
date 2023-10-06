import pytest

from profitpulse.account import Account
from profitpulse.account_name import AccountName
from profitpulse.comment import Comment
from profitpulse.money import Money
from profitpulse.repositories.accounts import Accounts
from testrig.scenario import DatabaseScenario


@pytest.mark.integration
def test_return_none_when_account_not_found(tmp_db_session):
    accounts = Accounts(tmp_db_session)
    assert accounts.get(AccountName("TheAccountName")) is None  # nosec


@pytest.mark.integration
def test_return_account_when_one_exists(tmp_db_session):
    DatabaseScenario(tmp_db_session).open_account(name="TheAccountName")
    accounts = Accounts(tmp_db_session)

    account = accounts.get(AccountName("TheAccountName"))

    assert isinstance(account, Account)  # nosec
    assert account.name == AccountName("TheAccountName")  # nosec


@pytest.mark.integration
def test_set_account(tmp_db_session):
    account = Account(AccountName("TheAccountName"))
    accounts = Accounts(tmp_db_session)

    accounts[account.name] = account


@pytest.mark.integration
def test_save_account_balance(tmp_db_session):
    balance = Money(10)
    account_name = AccountName("TheAccountName")
    account = Account(account_name=account_name, balance=balance)
    accounts = Accounts(tmp_db_session)

    accounts[account.name] = account

    account = accounts.get(account_name)
    assert account is not None  # nosec
    assert account.balance == balance  # nosec


@pytest.mark.integration
def test_save_account_closed_status(tmp_db_session):
    account_name = AccountName("TheAccountName")
    account = Account(account_name=account_name)
    accounts = Accounts(tmp_db_session)

    account.close()

    accounts[account.name] = account

    account = accounts[account.name]
    assert account.closed is True  # nosec


@pytest.mark.integration
def test_save_comment(tmp_db_session):
    account_name = AccountName("TheAccountName")
    account = Account(account_name=account_name)
    accounts = Accounts(tmp_db_session)

    comment = Comment("TheComment")
    account.deposit(Money(10), comment=comment)

    accounts[account.name] = account

    account = accounts[account.name]
    assert account.last_comment == comment  # nosec
