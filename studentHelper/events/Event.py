from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, user):
        self.__user = user

    @abstractmethod
    def execute(self):  # returns data
        pass

    def get_user(self):
        return self.__user
