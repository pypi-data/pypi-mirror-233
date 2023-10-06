class Comment:
    def __init__(self, comment: str) -> None:
        self._comment = comment

    def __str__(self) -> str:
        return self._comment

    def __repr__(self) -> str:
        return f"Comment({self._comment})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Comment):
            return NotImplemented
        return self._comment == __value._comment
