from abc import ABC, abstractmethod


class KPerson(ABC):
    def __init__(self, name, surname, tckn, date_of_birth):
        self._name = name
        self._surname = surname
        self._tckn = tckn
        self._date_of_birth = date_of_birth
        self._id = None

    @abstractmethod
    def calculate_id(self):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def tckn(self):
        return self._tckn

    @tckn.setter
    def tckn(self, value):
        self._tckn = value

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        self._date_of_birth = value

    @property
    def id(self):
        return self._id
