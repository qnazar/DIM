from django.urls import path
from .views import home, StylesList, StyleDetail, TeachersList, TeacherDetail, GroupList, \
    AbonementsList, Schedule, AbonementsDetail

urlpatterns = [
    path('', home, name='home'),
    path('styles', StylesList.as_view(), name='styles_list'),
    path('styles/<slug:slug>', StyleDetail.as_view(), name='style_detail'),
    path('teachers', TeachersList.as_view(), name='teachers_list'),
    path('teachers/<slug:slug>', TeacherDetail.as_view(), name='teacher_detail'),
    path('groups', GroupList.as_view(), name='groups_list'),
    path('abonements', AbonementsList.as_view(), name='abonements_list'),
    path('abonements/<int:pk>', AbonementsDetail.as_view(), name='abonement_detail'),
    path('schedule/<str:day>', Schedule.as_view(), name='schedule'),
    path('schedule', Schedule.as_view(), name='schedule'),
]
