from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),

    path('developer_home/', views.developer_home, name='developer_home'),
    path('startapper_home/', views.startapper_home, name='startapper_home'),
    path('practitioner_home/', views.practitioner_home, name='practitioner_home'),

    path('user-update/', views.user_update, name='user-update'),
    path('user-password/', views.user_password, name='user-password'),
    path('user-change/', views.Nimadir.as_view(), name='user-change'),

    path('success-projects/', views.success_projects, name='success-projects'),
    path('success-project/<int:pk>/', views.success_project_detail, name='success-project-detail'),
    path('success-project/comment/<int:pk>/', views.comment_of_post, name='comment-of-post'),

    path('about-us/', views.about_us, name='about-us'),
    path('contact-prowork', views.contact_prowork, name='contact-prowork'),
]
