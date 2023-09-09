from django.urls import path
from . import views


urlpatterns = [
   path('register',views.register, name = "account"),
   path('verify/<email_token>/', views.verify_email, name = "verify_email"),
   path('login',views.logining, name = "logining"),
   path('logouting/', views.logouting, name = 'logouting')
    
]
