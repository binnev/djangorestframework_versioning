class VersionDoesNotExist(Exception):
    pass


class TransformsNotDeclaredError(Exception):
    pass


class VersionsNotDeclaredError(ValueError):
    def __init__(self, obj_name: str) -> None:
        msg = f"You need to declare either introduced_in or removed_in for {obj_name}"
        super().__init__(msg)
