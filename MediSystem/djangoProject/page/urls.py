from django.urls import path
from .views import AnasayfaView, HakkindaView, login, YoneticiView, RandevuView, YoneticiGirisView, DoktorView, \
    HastaView, DoktorGirisView, HastaGirisView, KayıtView, SuccsessView

urlpatterns = [
    path('', AnasayfaView.as_view(), name='anasayfa'),
    path('hakkinda/', HakkindaView.as_view(), name='hakkinda'),
    path('yonetici/', YoneticiView.as_view(), name='yonetici'),
    path('randevu/', RandevuView.as_view(), name='randevu'),
    path('login/', login, name='login'),
    path('yonetici_giris', YoneticiGirisView.as_view(), name='yonetici_giris'),
    path('doktor/', DoktorView.as_view(), name='doktor'),
    path('hasta/', HastaView.as_view(), name='hasta'),
    path('doktor_giris/', DoktorGirisView.as_view(), name='doktor_giris'),
    path('hasta_giris/', HastaGirisView.as_view(), name='hasta_giris'),
    path('kayıt/', KayıtView.as_view(), name = 'kayıt'),
    path('succsess/', SuccsessView.as_view(), name = 'succsess')
]
