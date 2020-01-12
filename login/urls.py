from django.urls import path, re_path, include
from . import views, ajax
from django.contrib.auth import views as auth_views

urlpatterns = [
	path(
		'',
		views.login,
		name = 'login'
	),
	path(
        'password_reset',
        views.password_reset,
        name = 'password reset'
    ),
	path(
		'password_change/<pk>/<hash>',
		views.password_change,
		name = 'password change'
	),
    # path(
    # 	'logout',
    # 	views.logout,
    # 	name = 'logout'
    # ),
    path(
		'register',
		views.register,
		name = 'register'
	),
	path(
		'check_nickname',
		ajax.check_nickname,
		name = 'check nickname'
	),
	path(
		'check_email',
		ajax.check_email,
		name = 'check email'
	),
	path(
		'activate/<pk>/<hash>',
		views.activate,
		name = 'activate'
	)
]
