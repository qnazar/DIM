from django.urls import path
from .views import TeacherList, TeacherDetail

urlpatterns = [
    path('teachers/', TeacherList.as_view(), name='teachers_list'),
    path('teachers/<int:pk>/', TeacherDetail.as_view(), name='teacher_detail'),
]
