from django.urls import path, include
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('mypage/<int:user_id>/', my_page, name="my_page"),
    # path('sign_up/', sign_up, name='sign_up'),
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
    path('', include('allauth.urls')) ,
    path(
        "email-confirmation-required/",
        TemplateView.as_view(template_name="accounts/email_confirmation_required.html"),
        name="account_email_confirmation_required",
    ),
    path(
        "email-confirmation-done/",
        TemplateView.as_view(template_name="accounts/email_confirmation_done.html"),
        name="account_email_confirmation_done",
    ),
    path(
        "password/change/",
        CustomPasswordChangeView.as_view(),
        name="account_change_password",
    ),
    path("nickname/change/", change_nickname, name="account_change_nickname"),     
]
