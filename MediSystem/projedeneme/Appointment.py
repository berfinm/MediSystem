class KAppointment:
    def __init__(self, appointment_date, appointment_time, appointment_id):
        self._appointment_date = appointment_date
        self._appointment_time = appointment_time
        self._appointment_id = appointment_id

    @property
    def appointment_date(self):
        return self._appointment_date

    @appointment_date.setter
    def appointment_date(self, value):
        self._appointment_date = value

    @property
    def appointment_time(self):
        return self._appointment_time

    @appointment_time.setter
    def appointment_time(self, value):
        self._appointment_time = value

    @property
    def appointment_id(self):
        return self._appointment_id

    @appointment_id.setter
    def appointment_id(self, value):
        self._appointment_id = value
