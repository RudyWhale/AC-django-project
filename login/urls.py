from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [	
	path(
		'', 
		auth_views.LoginView.as_view(template_name='login/login.html'), 
		name='login'
	),
	path(
        'change_password/',
        auth_views.PasswordChangeView.as_view(template_name='login/change-password.html'),
        name='password_reset'
    ),
    path(
    	'logout',
    	views.logout,
    	name='logout'
    ),
    path(
		'register',
		views.register,
		name='register'
	),
	path(
		'register_as_artist',
		views.register_as_artist,
		name='register_as_artist'
	)
]