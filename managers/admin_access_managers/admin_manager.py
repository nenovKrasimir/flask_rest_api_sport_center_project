from abc import ABC, abstractmethod


class AdminManager(ABC):
    @staticmethod
    @abstractmethod
    def adding(data):
        ...

    @staticmethod
    @abstractmethod
    def delete(data):
        ...

    @staticmethod
    @abstractmethod
    def access_all():
        ...

    @staticmethod
    @abstractmethod
    def update_contact(data):
        ...
