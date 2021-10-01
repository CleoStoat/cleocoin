from dataclasses import dataclass


@dataclass()
class UserCoins:
    user_id: int
    coins: int
