from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

import config
from domain.model import UserCoins
from sqlalchemy.orm import Session, session


class AbstractRepository(ABC):

    @abstractmethod
    def get_coins(self, user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def create_coins(self, user_id: int, ammount: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_coins(self, user_id: int, ammount: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rem_coins(self, user_id: int, ammount: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def give_coins(self, from_user_id: int, to_user_id: int, ammount: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def take_coins(self, from_user_id: int, to_user_id: int, ammount: int) -> bool:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_coins(self, user_id: int) -> int:
        self.create_coins(user_id, config.get_initial_coin_ammount())
        user_coins = self.session.query(UserCoins).get(user_id)
        return user_coins.coins

    def create_coins(self, user_id: int, ammount: int) -> bool:
        user_coins = self.session.query(UserCoins).get(user_id)
        if user_coins is not None:
            return False
        user_coins = UserCoins(user_id=user_id, coins=ammount)
        self.session.add(user_coins)
        return True

    def add_coins(self, user_id: int, ammount: int) -> bool:
        self.create_coins(user_id, config.get_initial_coin_ammount())
        user_coins = self.session.query(UserCoins).get(user_id)
        user_coins.coins += ammount
        self.session.add(user_coins)
        return True

    def rem_coins(self, user_id: int, ammount: int) -> bool:
        self.create_coins(user_id, config.get_initial_coin_ammount())
        user_coins = self.session.query(UserCoins).get(user_id)
        if user_coins.coins - ammount < 0:
            return False
        user_coins.coins -= ammount
        self.session.add(user_coins)
        return True

    def give_coins(self, from_user_id: int, to_user_id: int, ammount: int) -> bool:
        if self.get_coins(from_user_id) < ammount:
            return False
        self.rem_coins(user_id=from_user_id, ammount=ammount)
        self.add_coins(user_id=to_user_id, ammount=ammount)
        return True

    def take_coins(self, from_user_id: int, to_user_id: int, ammount: int) -> bool:
        if self.get_coins(to_user_id) < ammount:
            return False
        self.rem_coins(user_id=to_user_id, ammount=ammount)
        self.add_coins(user_id=from_user_id, ammount=ammount)
        return True
