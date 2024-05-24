from Person import Person


class KManager(Person):
    TYPE = "M"

    def __init__(self, name, surname, tckn, date_of_birth,working_hospital):
        super().__init__(name, surname, tckn, date_of_birth)
        self._working_hospital = working_hospital
        self._manager_id = self.calculate_id()

    def calculate_id(self):
        return self.TYPE + self.tckn

    @property
    def working_hospital(self):
        return self._working_hospital

    @working_hospital.setter
    def working_hospital(self, value):
        self._working_hospital = value

    @property
    def manager_id(self):
        return self._manager_id

    @manager_id.setter
    def manager_id(self, value):
        self._manager_id = value
