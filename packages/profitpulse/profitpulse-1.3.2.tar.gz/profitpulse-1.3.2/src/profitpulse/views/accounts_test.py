import pytest

from profitpulse.money import Money
from profitpulse.views.accounts import AccountsView
from testrig.scenario import DatabaseScenario


@pytest.mark.integration
def test_return_no_data_when_no_accounts(tmp_db_session):
    assert AccountsView(tmp_db_session).data == []  # nosec


@pytest.mark.integration
def test_return_one_account_when_one_account_exists(tmp_db_session):
    DatabaseScenario(tmp_db_session).open_account(name="TheAccountName")

    assert AccountsView(tmp_db_session).data == [  # nosec
        {
            "name": "TheAccountName",
            "balance": Money(0),
            "status": True,
            "comment": "",
        },
    ]


@pytest.mark.integration
def test_show_the_balance_of_an_account(tmp_db_session):
    DatabaseScenario(tmp_db_session).open_account(name="TheAccountName")
    DatabaseScenario(tmp_db_session).deposit(100, "TheAccountName")

    assert AccountsView(tmp_db_session).data == [  # nosec
        {
            "name": "TheAccountName",
            "balance": Money(100),
            "status": True,
            "comment": "",
        },
    ]


@pytest.mark.integration
def test_show_the_balance_of_an_account_with_a_comment(tmp_db_session):
    DatabaseScenario(tmp_db_session).open_account(name="TheAccountName")
    DatabaseScenario(tmp_db_session).deposit(
        100, "TheAccountName", comment="TheComment"
    )

    assert AccountsView(tmp_db_session).data == [  # nosec
        {
            "name": "TheAccountName",
            "balance": Money(100),
            "status": True,
            "comment": "TheComment",
        },
    ]
