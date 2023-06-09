from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .form import LoginForm , MyPasswordChangeForm ,MyPasswordResetForm ,MySetPasswordForm

urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart , name='show_cart'),
    path('adjust-cart/',views.adjust_cart , name='adjust_cart'),
    path('edit/<int:id>',views.edit_add , name='edit_add'),
    path('delete/<int:id>',views.delete_add , name='delete_add'),
    path('buy/', views.buy_now, name='buy-now'),
    path('paymentdone/', views.payment_done, name='payment_done'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/<slug:data>/', views.mobile, name='mobile_data'),
    path('mobile/', views.mobile, name='mobile'),
    path('topwear/<slug:data>/', views.topwear, name='topwear_data'),
    path('topwear/', views.topwear, name='topwear'),
    path('bottomwear/<slug:data>/', views.bottomwear, name='bottomwear_data'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'app/login.html',authentication_form = LoginForm,next_page='address') , name='login'),
    path('accounts/logout /', auth_views.LogoutView.as_view(next_page='login') , name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class = MyPasswordChangeForm,success_url ='/passwordchangedone/') , name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html') , name='passwordchangedone'),
    path('checkout/', views.checkout, name='checkout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html' , form_class = MyPasswordResetForm ) , name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html') , name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class = MySetPasswordForm) , name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html') , name="password_reset_complete"),
]    + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
