"""
Cli adapters bridge the CLI frameworks with the application use cases.
"""

import site
from pathlib import Path
from typing import Optional

from toolcat.database import Database, Session

from profitpulse.account_name import AccountName
from profitpulse.application.close_account import CloseAccountService
from profitpulse.application.deposit_into_account import ServiceDepositIntoAccount
from profitpulse.application.import_transactions import ServiceImportTransactions
from profitpulse.application.open_account import (
    AccountAlreadyExistsError,
    OpenAccountService,
)
from profitpulse.comment import Comment
from profitpulse.gateways.cgdfile import GatewayCGDFile
from profitpulse.money import Money
from profitpulse.repositories.accounts import Accounts
from profitpulse.repositories.transactions import Transactions
from profitpulse.views.accounts import AccountsView
from profitpulse.views.transactions import ViewTransactions

# FIXME: There are objects in this module that do not match the protocols
#        defined in the application services. Fix them.

database_path = Path.home() / Path("Library/Application Support/Profitpulse")


def report(seller, since, on):
    db = Database(database_path)
    with Session(db.engine) as session:
        view = ViewTransactions(session, seller, since, on)

    transactions, total = view.data
    if not seller:
        if not transactions:
            print("Could not find any transactions!")
            return

        for t in transactions:
            print(f"Description: '{t['description']:>22}', Value: {t['value']:>10}")
        return

    print(f"Description: '{seller}', Value: {round(total, 2)}")


def migrate_database():
    """
    Runs the SQL migrations to update the database schema.
    """
    # TODO: This should belong to the toolcat.database.migrations module.
    db = Database(database_path)
    try:
        site_packages_path = site.getsitepackages()[
            0
        ]  # .pyenv/versions/3.11.2/lib/python3.11/site-packages

        for f in Path(f"{site_packages_path}/profitpulse/migrations").glob("*.sql"):
            db.run_sql_file(f)
    except FileNotFoundError:
        pass


migrate_database()


def reset():
    db = Database(database_path)
    db.remove()


def import_file(file_path: Path):
    db = Database(database_path)
    with Session(db.engine) as session:
        gateway_cgd = GatewayCGDFile(file_path)
        transactions = Transactions(session)
        ServiceImportTransactions(gateway_cgd, transactions).execute()
        session.commit()


class DepositRequest:
    def __init__(self, cent_amount, account_name, comment: Optional[str] = None):
        self._cent_amount = cent_amount
        self._account_name = account_name
        self._comment = comment

    @property
    def amount(self) -> Money:
        return Money(self._cent_amount)

    @property
    def comment(self) -> Optional[Comment]:
        return Comment(self._comment) if self._comment else None

    @property
    def account_name(self) -> AccountName:
        return self._account_name


def deposit(cent_amount: int, account_name: str, comment: Optional[str] = None) -> None:
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DepositRequest(cent_amount, account_name, comment)
        service = ServiceDepositIntoAccount(accounts)
        service.execute(request)

        session.commit()


def show_accounts(printer):
    with Session(Database(database_path).engine) as session:
        data = AccountsView(session).data
        if not data:
            print("No accounts found")
            return
        for i in data:
            printer(
                f"{i['name']}: {i['balance']} € {'Closed' if i['status'] else ''} {i['comment']}"
            )


class OpenAccountRequest:
    def __init__(self, name):
        self._name = AccountName(name)

    @property
    def account_name(self):
        return self._name


def print_error(e: Exception) -> None:
    print(f"\n\t> {str(e)},\n\t  why don't you try again using a different name ?")


def open_account(name):
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = OpenAccountRequest(name)
        try:
            OpenAccountService(accounts).execute(request)
        except AccountAlreadyExistsError as e:
            print_error(e)
        session.commit()


class CloseAccountRequest:
    def __init__(self, account_name):
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def close_account(name):
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = CloseAccountRequest(name)
        CloseAccountService(accounts).execute(request)
        session.commit()
