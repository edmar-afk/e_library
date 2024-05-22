from django.urls import path
from . import views

urlpatterns = [
    path('mainLogin', views.mainLogin, name='mainLogin'),
    path('mainDashboard', views.dashboard, name='mainDashboard'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('disapprove-user/<int:user_id>/', views.disapprove_user, name='disapprove_user'),
    path('<int:user_id>/deleteuser/', views.deleteUser, name='deleteuser'),
    
    path('approve-instructor/<int:instructor_id>/', views.approve_instructor, name='approve_instructor'),
    path('disapprove-instructor/<int:instructor_id>/', views.disapprove_instructor, name='disapprove_instructor'),
    
    path('about', views.about, name='about'),
    path('homepage', views.homepage, name='homepage'),
    path('user_register', views.user_register, name='user_register'),
    path('user_login', views.user_login, name='user_login'),
    path('logout', views.logout, name='logout'),
    
    
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('<int:forum_id>/student_forumPost/', views.student_forumPost, name='student_forumPost'),
    path('student_classroom', views.student_classroom, name='student_classroom'),
    path('<int:class_id>/student_room/', views.student_room, name='student_room'),
    path('student_lesson', views.student_lesson, name='student_lesson'),
    
    
    path('teacher_dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher_lesson', views.teacher_lesson, name='teacher_lesson'),
    path('teacher_forum', views.teacher_forum, name='teacher_forum'),
    path('<int:class_id>/classroom/', views.classroom, name='classroom'),
    path('<int:forum_id>/teacher_forumPost/', views.teacher_forumPost, name='teacher_forumPost'),
    
    path('<int:class_id>/deleteClassroom/', views.deleteClassroom, name='deleteClassroom'),
    path('<int:forum_id>/deleteforum/', views.deleteForum, name='deleteforum'),
    path('<int:lesson_id>/deleteLesson/', views.deleteLesson, name='deleteLesson'),
]