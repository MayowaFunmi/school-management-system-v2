from django.urls import path
from . import views, ajax_view, n_teaching, student_views

app_name = 'auths'

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_teacher_profile/', views.create_teacher_profile, name='create_teacher_profile'),
    path('update_teacher_profile/', views.update_teacher_profile, name='update_teacher_profile'),
    path('add_files/', views.add_files, name='add_files'),
    path('display_teacher_profile/', views.display_teacher_profile, name='display_teacher_profile'),
    path('teacher_docs/', views.teacher_docs, name='teacher_docs'),
    path('create_non_teacher_profile/', n_teaching.create_non_teacher_profile, name='create_non_teacher_profile'),
    path('display_non_teacher_profile/', n_teaching.display_non_teacher_profile, name='display_non_teacher_profile'),
    path('update_non_teacher_profile/', n_teaching.update_non_teacher_profile, name='update_non_teacher_profile'),
    path('non_teacher_docs/', n_teaching.non_teacher_docs, name='non_teacher_docs'),
    path('create_student_profile/', student_views.create_student_profile, name='create_student_profile'),
    path('display_student_profile/', student_views.display_student_profile, name='display_student_profile'),
    path('update_student_profile/', student_views.update_student_profile, name='update_student_profile'),
    path('get_school_by_zone/', ajax_view.get_school_by_zone, name='get_school_by_zone'),
    path('render_pdf_view/', views.render_pdf_view, name='render_pdf_view'),
    path('n_render_pdf_view/', n_teaching.render_pdf_view, name='n_render_pdf_view'),
]