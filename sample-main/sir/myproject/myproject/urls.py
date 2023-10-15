
from django.contrib import admin
from django.urls import path
from django.urls import include
from sirapp import views
from sirapp.views import GeneratePDF,GenerateFacPDF,GenerateStdPDF
from django.conf.urls.static import static
from django.conf import settings
# from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('admin_registration/', views.admin_registration, name='admin_registration'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('registration/', views.registration, name='registration'),
    path('liveevents/', views.liveevents, name='liveevents'),
    path('requestform/', views.requestform, name='requestform'),
    path('studentevents/', views.studentevents, name='studentevents'),
    path('lectures_seminar/', views.lectures_seminar, name='lectures_seminar'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_home/',views.user_home,name = 'user_home'),
    path('faculty/',views.facultyevents,name= "facultyevents"),
    path('admin_lectures/',views.admin_lectures, name = "admin_lectures"),
    path('admin_fac_events/',views.admin_fac_events,name="admin_fac_events"),
    path('admin_std_events/',views.admin_std_events,name="admin_std_events"),
    path('admin_calender/',views.admin_calender, name="admin_calender"),
    path('admin_settings/', views.admin_settings, name="admin_settings"),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('submit_lecture_feedback/', views.submit_lecture_feedback, name='submit_lecture_feedback'),
    path('submit_faculty_event_feedback/',views.submit_faculty_event_feedback,name='submit_faculty_event_feedback'),


    path('feedback/<str:event_title>/', views.feedback_page, name='feedback_page'),
    path('std_feedback/<str:event_title>/', views.std_feedbacks, name='std_feedbacks'),
    path('fac_feedback/<str:event_title>/', views.fac_feedbacks, name='fac_feedbacks'),
    path('std_login/',views.std_login, name ="std_login"),
    path('fac_login/',views.fac_login, name ="fac_login"),
    path('lec_login/',views.lec_login, name ="lec_login"),
    # path('generate_pdf/<str:event_title>/',views.GeneratePDF, name='generate_pdf'),
    path('generate_pdf/<str:event_title>/', GeneratePDF.as_view(), name='generate_pdf'),
    path('generate_std_pdf/<str:event_title>/', GenerateStdPDF.as_view(), name='generate_std_pdf'),

    path('generate_fac_pdf/<str:event_title>/', GenerateFacPDF.as_view(), name='generate_fac_pdf'),

    path('pdf_template/',views.pdf_template, name="pdf_template"),
    path('submit_request/',views.submit_request, name="submit_request"),
    path('get_events/', views.get_events, name='get_events'),


    path('std_pdf/',views.std_pdf,name="std_pdf"),

    path('fac_pdf/',views.fac_pdf,name="fac_pdf"),
    path('cal',views.cal,name = 'cal'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('usercal/',views.usercal,name = "usercal"),


    path('send_email/<str:email>/<str:event_name>/<str:event_type>/', views.send_email, name='send_email'),

    path('send_reject_email/<str:email>/<str:event_name>/', views.send_reject_email, name='send_reject_email'),
    path('newsreport/',views.newsreport, name='newsreport'),
    path('filter_events/', views.filter_events, name='filter_events'),
    path('deleteStdevents/<str:event_title>/<str:event_date>/', views.deleteStdevents, name='deleteStdevents'),

    path('deleteFacevents/<str:event_title>/<str:event_date>/', views.deleteFacevents, name='deleteFacevents'),

    path('deleteLectures/<str:event_title>/<str:event_date>/', views.deleteLectures, name='deleteLectures'),



]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
