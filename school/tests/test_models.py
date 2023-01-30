import datetime

from django.test import TestCase
from ..models import Category, Style, Teacher, Group


class TestCategoryModel(TestCase):
    def create_category(self, name, salary):
        return Category.objects.create(name=name, salary=salary)

    def test_category_creation(self):
        cat = self.create_category('TestCat', 100.0)
        self.assertTrue(isinstance(cat, Category))
        self.assertTrue(isinstance(cat.salary, float))
        self.assertEqual(str(cat), cat.name)


class TestStyleModel(TestCase):

    def create_style(self, name='Testing', description='Fake style for testing', photo=None, slug='testing'):
        return Style.objects.create(name=name, description=description, photo=photo, slug=slug)

    def test_style_creation(self):
        s = self.create_style()
        self.assertTrue(isinstance(s, Style))
        self.assertEqual(s.__str__(), s.name)
        self.assertEqual(s.get_absolute_url(), f'/styles/{s.slug}')


class TestTeacherModel(TestCase):

    def create_teacher(self, first_name, last_name, middle_name=None, nickname=None, photo=None,
                       slug=None, category=None, styles=None):
        t = Teacher.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   middle_name=middle_name,
                                   nickname=nickname,
                                   photo=photo,
                                   slug=slug,
                                   category=category)
        t.styles.set((Style.objects.create(name='Test1'),))
        return t

    def test_teacher_creation(self):
        t = self.create_teacher('Anna', 'Trincher', category=Category.objects.create(name='Test', salary=20.0))
        self.assertTrue(isinstance(t, Teacher))
        self.assertEqual(str(t), t.nickname)
        self.assertEqual(t.get_absolute_url(), f'/teachers/{t.slug}')
        self.assertEqual(t.nickname, 'Anna Trincher')
        self.assertEqual(t.slug, 'anna-trincher')
        self.assertIn(Style.objects.get(name='Test1'), t.styles.all())


class TestGroupModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='TestCat', salary=100.0)
        teacher = Teacher.objects.create(first_name='Anna',
                                         last_name='Trincher',
                                         category=category)
        style = Style.objects.create(name='TestStyle', slug='teststyle')
        teacher.styles.set((style,))
        group = Group.objects.create(teacher=teacher,
                                     style=style,
                                     level=0,
                                     day_1=1, day_2=4,
                                     scheduled_time=datetime.time(18, 00),
                                     duration=60,
                                     is_active=True)

    def test_group(self):
        group = Group.objects.get(pk=1)
        self.assertTrue(isinstance(group, Group))
        self.assertEqual(group.get_days, 'Mon-Thu')
        self.assertEqual(str(group), 'TestStyle with Anna Trincher every Mon-Thu at 18:00:00')
