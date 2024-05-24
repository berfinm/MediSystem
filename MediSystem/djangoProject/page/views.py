from django.views.generic import TemplateView
from .forms import YoneticiGirisFormu
import mysql.connector
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.db import connection
from .forms import DoktorEkleFormu, DoktorSilFormu, RandevuFormu, DoktorGirisFormu, HastaGirisFormu, HastaSilFormu, HastaEkleFormu, RandevuSilFormu, RandevuDuzenleFormu, KayıtFormu

class DoktorGirisView(TemplateView):
    template_name = 'doktor_giris.html'

    def get(self, request, *args, **kwargs):
        form_add = HastaEkleFormu()
        form_delete = HastaSilFormu()
        ad = request.session.get("ad")
        soyad = request.session.get("soyad")
        kimlik = request.session.get("kimlik")

        query = """
                SELECT patient_id, name, surname, tckn, date_of_birth, gender
                FROM patients
                WHERE patient_id IN (
                    SELECT patient_id
                    FROM appointments
                    WHERE hospital_id IN (
                        SELECT hospital_id
                        FROM doctors
                        WHERE tckn = %s
                    )
                )
                """

        with connection.cursor() as cursor:
            cursor.execute(query, [kimlik])
            hastalar = cursor.fetchall()

        context = {
            'ad': ad,
            'soyad': soyad,
            'hastalar': hastalar,
            'form_add': form_add,
            'form_delete': form_delete
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'form_type' in request.POST:
            if request.POST['form_type'] == 'add_patient':
                form_add = HastaEkleFormu(request.POST)
                if form_add.is_valid():
                    data = form_add.cleaned_data
                    query = """
                    INSERT INTO patients (name, surname, tckn, date_of_birth, gender, tel_no, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query, [
                            data['name'],
                            data['surname'],
                            data['tckn'],
                            data['date_of_birth'],
                            data['gender'],
                            data['tel_no'],
                            data['address']
                        ])
                    print('*****+')
                    query2 = """
                    INSERT INTO appointments (patient_id, doctor_id, hospital_id)
                    VALUES ((SELECT patient_id FROM patients WHERE tckn=%s), (SELECT doctor_id FROM doctors WHERE tckn = %s), (SELECT hospital_id FROM doctors WHERE tckn=%s))
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query2, [
                            data['tckn'],
                            request.session.get('kimlik'),
                            request.session.get('kimlik')
                        ])
            elif request.POST['form_type'] == 'delete_patient':
                form_delete = HastaSilFormu(request.POST)
                if form_delete.is_valid():
                    hasta_id = form_delete.cleaned_data['hasta_id']
                    query = "DELETE FROM appointments WHERE patient_id = %s"
                    with connection.cursor() as cursor:
                        cursor.execute(query, [hasta_id])
                    query2 = "DELETE FROM patients WHERE patient_id = %s"
                    with connection.cursor() as cursor:
                        cursor.execute(query2, [hasta_id])

        return redirect('doktor_giris')

class DoktorView(TemplateView):
    template_name = 'doktor.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = DoktorGirisFormu()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DoktorGirisFormu(request.POST)
        if form.is_valid():
            name = form.cleaned_data['ad']
            surname = form.cleaned_data['soyad']
            tckn = form.cleaned_data['kimlik']

            sql = "SELECT * FROM doctors WHERE tckn = %s AND surname =%s AND name=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql, [tckn,surname,name])
                result = cursor.fetchall()

            if result:
                print("Result:", result)
                request.session['ad'] = name
                request.session['soyad'] = surname
                request.session['kimlik'] = tckn
                return HttpResponseRedirect(reverse('doktor_giris'))
            else:
                error_message = "Giriş bilgileri geçersiz."
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = "Form doğrulanamadı."
            return render(request, self.template_name, {'form': form, 'error_message': error_message})


class HastaGirisView(TemplateView):
    template_name = 'hasta_giris.html'
    def get(self, request, *args, **kwargs):
        form_edit = RandevuDuzenleFormu()
        form_delete = RandevuSilFormu()
        ad = request.session.get("ad")
        soyad = request.session.get("soyad")
        kimlik = request.session.get("kimlik")

        query = """
                SELECT a.appointment_id, a.appointment_date, a.appointment_time, 
                       p.tckn AS patient_tckn,
                       d.name AS doctor_name, d.surname AS doctor_surname, d.profession,
                       h.hospital_name AS hospital_name
                FROM appointments a
                INNER JOIN patients p ON a.patient_id = p.patient_id
                INNER JOIN doctors d ON a.doctor_id = d.doctor_id
                INNER JOIN hospitals h ON a.hospital_id = h.hospital_id
                WHERE p.tckn = %s;

                """
        with connection.cursor() as cursor:
            cursor.execute(query, [kimlik])
            randevu_detay = cursor.fetchall()

        context = {
            'ad': ad,
            'soyad': soyad,
            'randevu_detay': randevu_detay,
            'form_delete': form_delete,
            'form_edit': form_edit,
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        if 'form_type' in request.POST:
            if request.POST['form_type'] == 'delete_randevu':
                form_delete = RandevuSilFormu(request.POST)
                if form_delete.is_valid():
                    randevu_id = form_delete.cleaned_data['randevu_id']
                    query = "DELETE FROM appointments WHERE appointment_id = %s"
                    with connection.cursor() as cursor:
                        cursor.execute(query, [randevu_id])
                        messages.success(request, 'Randevu başarıyla silindi.')
                        return HttpResponseRedirect(reverse('hasta_giris'))
            elif request.POST['form_type'] == 'edit_randevu':
                form_edit = RandevuDuzenleFormu(request.POST)
                if form_edit.is_valid():
                    randevu_id = form_edit.cleaned_data['randevu_id']
                    yeni_tarih = str(form_edit.cleaned_data['yeni_tarih'])
                    yeni_saat = str(form_edit.cleaned_data['yeni_saat'])
                    query = """
                                    UPDATE appointments
                                    SET appointment_date = %s, appointment_time = %s
                                    WHERE appointment_id = %s;
                                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query, [yeni_tarih, yeni_saat, randevu_id])

                return self.get(request, *args, **kwargs)


class HastaView(TemplateView):
    template_name = 'hasta.html'
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = HastaGirisFormu()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = HastaGirisFormu(request.POST)
        if form.is_valid():
            name = form.cleaned_data['ad']
            surname = form.cleaned_data['soyad']
            tckn = form.cleaned_data['kimlik']

            sql = "SELECT * FROM patients WHERE tckn = %s AND surname =%s AND name=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql, [tckn,surname,name])
                result = cursor.fetchall()

            if result:
                print("Result:", result)
                request.session['ad'] = name
                request.session['soyad'] = surname
                request.session['kimlik'] = tckn
                return HttpResponseRedirect(reverse('hasta_giris'))
            else:
                error_message = "Giriş bilgileri geçersiz."
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = "Form doğrulanamadı."
            return render(request, self.template_name, {'form': form, 'error_message': error_message})
class YoneticiGirisView(View):
    template_name = 'yonetici_giris.html'
    def get(self, request, *args, **kwargs):
        form_add = DoktorEkleFormu()
        form_delete = DoktorSilFormu()
        ad = request.session.get("ad")
        soyad = request.session.get("soyad")
        kimlik = request.session.get("kimlik")
        # SQL query to fetch doctors
        query = """
        SELECT doctor_id, name, surname, profession
        FROM doctors
        WHERE hospital_id = (SELECT hospital_id FROM managers WHERE name = %s AND tckn = %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [ad, kimlik])
            doktorlar = cursor.fetchall()
        context = {
            'ad': ad,
            'soyad': soyad,
            'doktorlar': doktorlar,
            'form_add': form_add,
            'form_delete': form_delete
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'form_type' in request.POST and request.POST['form_type'] == 'add_doctor':
            form_add = DoktorEkleFormu(request.POST)
            if form_add.is_valid():
                data = form_add.cleaned_data
                query = """
                INSERT INTO doctors (name, surname, tckn, date_of_birth, profession, hospital_id)
                VALUES (%s, %s, %s, %s, %s, (SELECT hospital_id FROM managers WHERE name = %s AND tckn = %s))
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['name'],
                        data['surname'],
                        data['tckn'],
                        data['date_of_birth'],
                        data['profession'],
                        request.session.get("ad"),  # Pull from session
                        request.session.get("kimlik")  # Pull from session
                    ])
        elif 'form_type' in request.POST and request.POST['form_type'] == 'delete_doctor':
            form_delete = DoktorSilFormu(request.POST)
            if form_delete.is_valid():
                doktor_id = form_delete.cleaned_data['doktor_id']
                query2 = "DELETE FROM appointments WHERE doctor_id = %s"
                with connection.cursor() as cursor:
                    cursor.execute(query2, [doktor_id])
                query = "DELETE FROM doctors WHERE doctor_id = %s"
                with connection.cursor() as cursor:
                    cursor.execute(query, [doktor_id])


        return redirect('yonetici_giris')


class AnasayfaView(TemplateView):
    template_name = 'home.html'


class HakkindaView(TemplateView):
    template_name = 'hakkimda.html'


def login(request):
    return render(request, 'login.html')


class RandevuView(TemplateView):
    template_name = 'randevu.html'

    def get(self, request, *args, **kwargs):
        form = RandevuFormu()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RandevuFormu(request.POST)
        if form.is_valid():
            ad = form.cleaned_data['ad']
            soyad = form.cleaned_data['soyad']
            kimlik = form.cleaned_data['kimlik']
            randevu_tarih = str(form.cleaned_data['randevu_tarih'])
            randevu_saat = str(form.cleaned_data['randevu_saat'])
            randevu_alanlari = form.cleaned_data['randevu_alanlari']

            action = request.POST.get('action')
            if action == 'search_randevu':
                # Doktor arama sorgusu ve sonuçlar
                query = """SELECT doctor_id, name, surname, profession FROM doctors WHERE profession = %s"""
                with connection.cursor() as cursor:
                    cursor.execute(query, [randevu_alanlari])
                    randevular = cursor.fetchall()
                # Doktorları ve form verilerini gönder
                return render(request, 'randevu.html', {'randevular': randevular, 'form': form})

            elif action == 'select_randevu':
                # Seçilen doktor ile randevu kaydı
                selected_randevu = request.POST.get('selected_randevu')
                doctor_id = selected_randevu.split(' ')[0]
                print(randevu_tarih + randevu_saat + kimlik + doctor_id + doctor_id)
                query = """
                    INSERT INTO appointments (appointment_id, appointment_date, appointment_time, patient_id, doctor_id, hospital_id)
                    SELECT COALESCE(MAX(appointment_id), 0) + 1, %s, %s, 
                           (SELECT patient_id FROM patients WHERE tckn=%s), 
                           (SELECT doctor_id FROM doctors WHERE doctor_id=%s), 
                           (SELECT hospital_id FROM doctors WHERE doctor_id = %s)
                    FROM appointments
                """

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query, [randevu_tarih, randevu_saat, kimlik, doctor_id, doctor_id])
                    messages.success(request, "Randevu başarıyla kaydedildi!")
                except Exception as e:
                    messages.error(request, f"Randevu kaydedilirken bir hata oluştu: {str(e)}")

                    messages.success(request, "Randevu başarıyla kaydedildi!")
                except Exception as e:
                    messages.error(request, f"Randevu kaydedilirken bir hata oluştu: {str(e)}")
                # İşlem başarılıysa başka bir sayfaya yönlendirme veya başka bir mesaj gösterebilirsiniz
                messages.success(request, "Randevu başarıyla tamamlandı!")
                return redirect('succsess')
        else:
            messages.error(request, "Formda hatalı bilgiler var. Lütfen bilgileri kontrol edin.")

        return render(request, 'randevu.html', {'form': form})


class YoneticiView(TemplateView):
    template_name = 'yonetici.html'
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = YoneticiGirisFormu()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = YoneticiGirisFormu(request.POST)
        if form.is_valid():
            ad = form.cleaned_data['ad']
            soyad = form.cleaned_data['soyad']
            kimlik = form.cleaned_data['kimlik']

            try:
                # MySQL veritabanına bağlan
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="24012004Bb*",
                    database="proje4"
                )
                print("***********")
                # SQL sorgusu
                cursor = conn.cursor()
                sql = "SELECT * FROM managers WHERE name = %s AND tckn = %s"
                cursor.execute(sql, (ad, kimlik))
                result = cursor.fetchall()
                print("Result:", result)
                cursor.close()
                conn.close()

                # Eğer doğrulama başarılıysa, yönlendir
                if result:
                    print("Result:", result)
                    request.session['ad'] = ad
                    request.session['soyad'] = soyad
                    request.session['kimlik'] = kimlik
                    return HttpResponseRedirect(reverse('yonetici_giris'))  # Yönetici anasayfasına yönlendir
                else:
                    error_message = "Giriş bilgileri geçersiz."
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            except Exception as e:
                error_message = "Veritabanı hatası: {}".format(e)
                return render(request, self.template_name, {'form': form, 'error_message': error_message})

        # Form doğrulanmadıysa, tekrar yonetici.html sayfasını göster
        return render(request, self.template_name, {'form': form})


class KayıtView(TemplateView):
    template_name = 'kayıt.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = KayıtFormu(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            query = """
            INSERT INTO patients (name, surname, tckn, date_of_birth, gender, tel_no, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['name'],
                        data['surname'],
                        data['tckn'],
                        data['date_of_birth'],
                        data['gender'],
                        data['tel_no'],
                        data['address'],
                    ])
                messages.success(request, "Kayıt başarıyla tamamlandı.")
                return redirect('succsess')
            except Exception as e:
                messages.error(request, f'Kayıt sırasında bir hata oluştu: {e}')
                return redirect('kayıt')  # Hata durumunda aynı sayfaya yönlendirme

        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = KayıtFormu()  # Formu context'e ekleyin
        return context

class SuccsessView(TemplateView):
    template_name = 'success.html'