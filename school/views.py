from django.shortcuts import render
from django.views.generic import DetailView

from .models import Teacher


# Create your views here.
def home(request):
    return render(request, 'school/home.html', context={'test': 'Static'})


class TeacherDetail(DetailView):
    model = Teacher
