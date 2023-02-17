from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.db.models import Q

from .models import Teacher, Style, Group, Abonement


def home(request):
    return render(request, 'school/home.html', context={'test': 'DIM'})


class StylesList(ListView):
    queryset = Style.objects.filter(teacher__isnull=False).prefetch_related('teachers').distinct()
    context_object_name = 'styles'
    template_name = 'school/styles_list.html'


class StyleDetail(DetailView):
    queryset = Style.objects.prefetch_related('teachers').all()
    context_object_name = 'style'
    template_name = 'school/style_detail.html'


class TeachersList(ListView):
    queryset = Teacher.objects.prefetch_related('styles').select_related('category').all()
    context_object_name = 'teachers'
    template_name = 'school/teacher_list.html'


class TeacherDetail(DetailView):
    queryset = Teacher.objects.prefetch_related('styles').select_related('category').all()


class GroupList(ListView):
    queryset = Group.objects.select_related('style', 'teacher', 'teacher__category').all()
    context_object_name = 'groups'
    template_name = 'school/groups_list.html'


class AbonementsList(ListView):
    queryset = Abonement.objects.select_related('category').all()
    context_object_name = 'abonements'
    template_name = 'school/abonements_list.html'


class AbonementsDetail(DetailView):
    queryset = Abonement.objects.select_related('category').all()
    context_object_name = 'abonement'
    template_name = 'school/abonement_detail.html'


class Schedule(ListView):
    context_object_name = 'groups'
    template_name = 'school/schedule.html'

    def get_queryset(self):
        if 'day' not in self.kwargs.keys():
            return Group.objects.select_related('teacher', 'hall', 'style', 'teacher__category') \
                .filter(is_active=True).order_by('day_1', 'scheduled_time')

        days = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}
        day = days[self.kwargs['day']]
        return Group.objects.select_related('teacher', 'hall', 'style', 'teacher__category') \
            .filter(is_active=True).filter(Q(day_1=day) | Q(day_2=day)).order_by('day_1', 'scheduled_time') \
            .order_by('day_1', 'day_2', 'scheduled_time')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'] = {'monday': 'Понеділок', 'tuesday': 'Вівторок', 'wednesday': 'Середа', 'thursday': 'Четвер',
                           'friday': 'П’ятниця', 'saturday': 'Субота', 'sunday': 'Неділя'}
        return context
