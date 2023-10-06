from typing import Optional

from profitpulse.account_name import AccountName
from profitpulse.comment import Comment
from profitpulse.money import Money


class Account:
    def __init__(
        self,
        account_name: AccountName,
        closed: bool = False,
        balance: Optional[Money] = None,
        comment: Optional[Comment] = None,
    ):
        self._account_name = account_name
        self._closed = closed
        self._balance: Money = Money(0)
        self._comment: Optional[Comment] = comment
        if balance:
            self._balance = balance

    def __repr__(self) -> str:
        return f"Account({self._account_name})"

    @property
    def name(self) -> AccountName:
        return self._account_name

    @property
    def balance(self) -> Money:
        return self._balance

    def close(self):
        self._closed = True

    @property
    def closed(self) -> bool:
        return True if self._closed else False

    def deposit(self, amount: Money, comment: Optional[Comment] = None):
        if self.closed:
            return
        self._balance += amount
        self._comment = comment

    @property
    def last_comment(self) -> Optional[Comment]:
        return self._comment
