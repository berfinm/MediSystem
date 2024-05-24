from django import forms

class YoneticiGirisFormu(forms.Form):
    ad = forms.CharField(label='Adınız', max_length=100)
    soyad = forms.CharField(label='Soyadınız', max_length=100)
    kimlik = forms.CharField(label='Kimlik Numaranız', max_length=12)

class DoktorGirisFormu(forms.Form):
    ad = forms.CharField(label='Adınız', max_length=100)
    soyad = forms.CharField(label='Soyadınız', max_length=100)
    kimlik = forms.CharField(label='Kimlik Numaranız', max_length=12)

class HastaGirisFormu(forms.Form):
    ad = forms.CharField(label='Adınız', max_length=100)
    soyad = forms.CharField(label='Soyadınız', max_length=100)
    kimlik = forms.CharField(label='Kimlik Numaranız', max_length=12)

class DoktorEkleFormu(forms.Form):
    name = forms.CharField(label='Ad', max_length=50)
    surname = forms.CharField(label='Soyad', max_length=50)
    tckn = forms.CharField(label='TCKN', max_length=12)
    date_of_birth = forms.CharField(label='Doğum Tarihi', max_length=50)
    profession = forms.CharField(label='Meslek', max_length=50)

class DoktorSilFormu(forms.Form):
    doktor_id = forms.IntegerField(label='Doktor ID')

class HastaSilFormu(forms.Form):
    hasta_id = forms.IntegerField(label='Hasta ID')

class RandevuSilFormu(forms.Form):
    randevu_id = forms.IntegerField(label='Randevu numarası')

class RandevuDuzenleFormu(forms.Form):
    randevu_id = forms.IntegerField(label='Randevu ID')
    yeni_tarih = forms.DateField(label='Yeni Tarih', widget=forms.DateInput(attrs={'type': 'date'}))
    yeni_saat = forms.TimeField(label='Yeni Saat', widget=forms.TimeInput(attrs={'type': 'time'}))


class HastaEkleFormu(forms.Form):
    name = forms.CharField(label='Ad', max_length=50)
    surname = forms.CharField(label='Soyad', max_length=50)
    tckn = forms.CharField(label='TCKN', max_length=12)
    date_of_birth = forms.CharField(label='Doğum Tarihi', max_length=50)
    gender = forms.CharField(label='Cinsiyet', max_length=50)
    tel_no = forms.CharField(label='Telefon', max_length=50)
    address = forms.CharField(label='Adres', max_length= 200)

class KayıtFormu(forms.Form):
    name = forms.CharField(label='Ad', max_length=50)
    surname = forms.CharField(label='Soyad', max_length=50)
    tckn = forms.CharField(label='TCKN', max_length=12)
    date_of_birth = forms.CharField(label='Doğum Tarihi', max_length=50)
    gender = forms.CharField(label='Cinsiyet', max_length=50)
    tel_no = forms.CharField(label='Telefon', max_length=50)
    address = forms.CharField(label='Adres', max_length= 200)
class RandevuFormu(forms.Form):
    ad = forms.CharField(label='Ad', max_length=100)
    soyad = forms.CharField(label='Soyad', max_length=100)
    kimlik = forms.CharField(label='Kimlik Numarası', max_length=11)
    randevu_alanlari = forms.CharField(label='Randevu Almak İstediğiniz Alan', max_length=100)
    randevu_tarih = forms.DateField(label='Randevu Tarihi', widget=forms.DateInput(attrs={'type': 'date'}))
    randevu_saat = forms.TimeField(label='Randevu Saati', widget=forms.TimeInput(attrs={'type': 'time'}))