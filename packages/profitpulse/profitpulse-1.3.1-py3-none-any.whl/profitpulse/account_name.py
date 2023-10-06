class AccountName:
    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Account name cannot be empty")
        self._name: str = name

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"AccountName({self._name})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, AccountName):
            return NotImplemented
        return self._name == __value._name

    def __hash__(self):
        return hash((self._name,))
