from ....app import db

import pandas as pd
from abc import abstractmethod, ABC, ABCMeta
class MatchmakingBase(metaclass = ABCMeta):
    @abstractmethod 
    def __init__(self, path):
        self.__dataset_path = path


    @property
    @abstractmethod
    def dataset_path(self):
        pass


    @dataset_path.setter
    @abstractmethod
    def dataset_path(self, value):
        pass


    @abstractmethod
    def perform_matchmaking(self) -> int:
        pass


