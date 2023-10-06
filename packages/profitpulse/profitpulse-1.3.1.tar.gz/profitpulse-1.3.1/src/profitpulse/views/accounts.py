from toolcat.database import text

from profitpulse.money import Money
from profitpulse.repositories import accounts
from profitpulse.views.views import View


class AccountsView(View):
    def __init__(self, session) -> None:
        self._session = session

    @property
    def data(self):
        sql_stmt = """
          SELECT account.name as name,
                 COALESCE(balance.value , 0) as balance,
                 account.status,
                 balance.comment
            FROM account
       LEFT JOIN balance
              ON account.id = balance.account_id
        """
        rows = self._session.execute(text(sql_stmt))

        return [
            {
                "name": row[0],
                "balance": Money(row[1]),
                "status": False if row[2] == accounts.OPEN else True,
                "comment": row[3],
            }
            for row in rows
        ]
