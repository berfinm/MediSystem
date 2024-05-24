import random
import datetime
import mysql.connector
import mysql.connector


host = 'localhost'
user = 'root'
password = '24012004Bb*'
database = 'proje4'


conn = mysql.connector.connect(host=host, user=user, password=password, database=database)

cursor = conn.cursor()

new_appointments = []


cursor.execute("SELECT hospital_id FROM hospitals")
hospital_ids = cursor.fetchall()


cursor.execute("SELECT patient_id FROM patients")
patient_ids = cursor.fetchall()


cursor.execute("SELECT doctor_id FROM doctors")
doctor_ids = cursor.fetchall()


for _ in range(30):

    random_hospital_id = random.choice(hospital_ids)[0]
    random_patient_id = random.choice(patient_ids)[0]
    random_doctor_id = random.choice(doctor_ids)[0]


    appointment_date = datetime.datetime.now().date() + datetime.timedelta(days=random.randint(1, 30))
    appointment_time = datetime.time(hour=random.randint(0, 23), minute=random.randint(0, 59))


    new_appointments.append((None, appointment_date, appointment_time, random_patient_id, random_doctor_id, random_hospital_id))


sql = "INSERT INTO appointments (appointment_id, appointment_date, appointment_time, patient_id, doctor_id, hospital_id) VALUES (%s, %s, %s, %s, %s, %s)"


for appointment in new_appointments:
    cursor.execute(sql, appointment)


conn.commit()


cursor.close()
conn.close()
