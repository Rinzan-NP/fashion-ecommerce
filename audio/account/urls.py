from django.urls import path
from . import views


urlpatterns = [
   path('register',views.register, name = "account"),
   path('verify/<email_token>/', views.verify_email, name = "verify_email"),
   path('login/',views.logining, name = "logining"),
   path('logouting/', views.logouting, name = 'logouting'),
   path('verify_account/',views.verify_account, name = "verify_account"),
   path('change_password/<forgot_password_token>',views.change_password, name = "check_account"),

   



    
]
