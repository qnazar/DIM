from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Teacher, Style, Group, Abonement


# Create your views here.
def home(request):
    return render(request, 'school/home.html', context={'test': 'Static'})


class StylesList(ListView):
    queryset = Style.objects.filter(teacher__isnull=False).prefetch_related('teachers').distinct()
    context_object_name = 'styles'
    template_name = 'school/styles_list.html'


class StyleDetail(DetailView):
    queryset = Style.objects.prefetch_related('teachers').all()
    context_object_name = 'style'
    template_name = 'school/style_detail.html'


class TeachersList(ListView):
    queryset = Teacher.objects.prefetch_related('styles', 'category').all()
    context_object_name = 'teachers'
    template_name = 'school/teacher_list.html'
    # paginate_by =


class TeacherDetail(DetailView):
    queryset = Teacher.objects.prefetch_related('styles').select_related('category').all()


class GroupList(ListView):
    queryset = Group.objects.select_related('style', 'teacher').all()
    context_object_name = 'groups'
    template_name = 'school/groups_list.html'


class AbonementsList(ListView):
    queryset = Abonement.objects.select_related('category').all()
    context_object_name = 'abonements'
    template_name = 'school/abonements_list.html'
