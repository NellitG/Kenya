from django.urls import path
from . import views

urlpatterns = [
    path('api/counties/', views.get_counties),
    path('api/subcounties/', views.get_subcounties),
    path('api/wards/', views.get_wards),
    path('api/wards/<int:ward_id>/', views.get_ward),
    path('api/wards/search/', views.search_wards),
]
