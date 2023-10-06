import pytest

from profitpulse.views.transactions import ViewTransactions
from testrig.scenario import database, scenario_for


@pytest.mark.integration
def test_shown_no_transactions_on_empty_database(tmp_db_session):
    transactions, total = ViewTransactions(tmp_db_session).data

    assert not transactions  # nosec
    assert not total  # nosec


@pytest.mark.integration
def test_show_one_transaction_when_one_is_available(tmp_db_session):
    """
    Given a database with one transaction
    When the view is executed
    Then the transaction is shown
    """

    scenario = scenario_for(database, tmp_db_session)
    scenario = scenario.log_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session).data

    assert transactions == [{"description": "foo", "value": 1}]  # nosec
    assert total == 1  # nosec


@pytest.mark.integration
def test_show_multiple_transactions_when_more_than_one_is_available(tmp_db_session):
    """
    Given a database with multiple transactions
    When the view is executed
    Then the transactions are shown
    """

    scenario = scenario_for(database, tmp_db_session)
    scenario = scenario.log_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )
    scenario = scenario.log_transaction(
        description="bar", value=2, date_of_movement="2020-01-01", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session).data

    assert transactions == [  # nosec
        {"description": "foo", "value": 1},
        {"description": "bar", "value": 2},
    ]
    assert total == 3  # nosec


@pytest.mark.integration
def test_show_transactions_since_a_given_date(tmp_db_session):
    """
    Given a database with multiple transactions
    When the view is executed with a since date
    Then the transactions since the given date are shown
    """

    scenario = scenario_for(database, tmp_db_session)
    scenario = scenario.log_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )
    scenario = scenario.log_transaction(
        description="bar", value=2, date_of_movement="2020-01-02", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session, since="2020-01-02").data

    assert transactions == [{"description": "bar", "value": 2}]  # nosec
    assert total == 2  # nosec


@pytest.mark.integration
def test_show_transactions_on_a_given_date(tmp_db_session):
    """
    Given a database with multiple transactions
    When the view is executed with a on date
    Then the transactions on the given date are shown
    """

    scenario = scenario_for(database, tmp_db_session)
    scenario = scenario.log_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )
    scenario = scenario.log_transaction(
        description="bar", value=2, date_of_movement="2020-01-02", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session, on="2020-01-01").data

    assert transactions == [{"description": "foo", "value": 1.0}]  # nosec
    assert total == 1.0  # nosec


@pytest.mark.integration
def test_show_total_for_a_specific_seller(tmp_db_session):
    """
    Given a database with multiple transactions
    When the view is executed with a seller
    Then the total for the given seller is shown
    """
    scenario = scenario_for(database, tmp_db_session)
    scenario = scenario.log_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )
    scenario = scenario.log_transaction(
        description="bar", value=2, date_of_movement="2020-01-02", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session, seller="foo").data

    assert total == 1.0  # nosec
    # TODO: transactions should be ignore while the view is the same for all use cases
    # assert transactions == [{"description": "foo", "value": 1.0}]  # nosec
