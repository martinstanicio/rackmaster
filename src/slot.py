class Slot:
    def __init__(
        self,
        xx: int,
        yyy: int,
        zz: int,
        article_code: str,
        quantity: int = 0,
        status: str = "divided_pallet",
    ) -> None:
        if quantity < 0:
            raise Exception("`quantity` must be a positive number")

        match status:
            case "blocked" | "full_pallet" | "divided_pallet":
                pass
            case _:
                raise Exception(
                    "`status` must be 'blocked', 'full_pallet', or 'divided_pallet'"
                )

        self.xx = xx
        self.yyy = yyy
        self.zz = zz
        self.article_code = article_code
        self.quantity = quantity
        self.status = status

    def is_blocked(self) -> bool:
        return self.status == "blocked"

    def is_empty(self) -> bool:
        return not self.is_blocked() and self.quantity == 0
