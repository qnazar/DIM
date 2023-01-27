from django.urls import path
from .views import home, TeacherDetail

urlpatterns = [
    path('', home, name='home'),
    path('teacher/<slug:slug>', TeacherDetail.as_view(), name='teacher_detail')
]
