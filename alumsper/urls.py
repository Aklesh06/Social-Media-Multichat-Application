from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.login,name='login'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('home', views.home, name='home'),
    path('password_reset',views.pass_reset_req, name="password_reset"),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('post/<int:acc_id>', views.post, name = 'post'),
    path('comment/<int:post_id>/<int:acc_id>', views.comment, name='comment'),
    path('edit',views.edit, name = 'edit'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
     path('event_page',views.event_page,name='event_page'),
     path('event/<int:acc_id>',views.event,name='event'),
     path('eventcomment/<int:event_id>/<int:acc_id>', views.eventcomment, name='eventcomment'),
     path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
     path('delete_eventpost/<int:event_id>', views.delete_eventpost, name='delete_eventpost'),
     path('delete_comment/<int:comm_id>',views.delete_comment, name="delete_comment"),
     path('delete_eventcomment/<int:eventcomm_id>', views.delete_eventcomment, name='delete_eventcomment'),
]
