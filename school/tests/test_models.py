import datetime
import decimal

import django.db.utils
from django.test import TestCase
from django.utils.text import slugify

from ..models import Category, Style, Teacher, Group


class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='TestCat', salary=100.009)

    def test_category_creation(self):
        with self.assertRaises(decimal.InvalidOperation):
            Category.objects.create(name='TestCatFoo', salary=100000)

    def test_category(self):
        cat = Category.objects.get(pk=1)
        self.assertTrue(isinstance(cat, Category))
        self.assertEqual(str(cat), cat.name)

    def test_category_salary(self):
        cat = Category.objects.get(pk=1)
        self.assertTrue(isinstance(cat.salary, decimal.Decimal))
        self.assertEqual(cat.salary, decimal.Decimal('100.01'))


class TestStyleModel(TestCase):
    def setUp(self, name='Testing', description='Fake style for testing', photo=None, slug=None) -> None:
        Style.objects.create(name=name, description=description, photo=photo, slug=slug)

    def test_style_creation(self):
        s = Style.objects.get(pk=1)
        self.assertTrue(isinstance(s, Style))
        self.assertEqual(str(s), s.name)
        self.assertEqual(s.slug, 'testing')
        self.assertEqual(s.get_absolute_url(), f'/styles/{s.slug}')


class TestTeacherModel(TestCase):
    @classmethod
    def setUpClass(cls):
        category = Category.objects.create(name='Cat', salary=100.0)
        t = Teacher.objects.create(first_name='Ben',
                                   last_name='Howitz',
                                   middle_name=None,
                                   nickname=None,
                                   photo=None,
                                   slug=None,
                                   category=category)
        style_1 = Style.objects.create(name='style_1')
        style_2 = Style.objects.create(name='style_2')
        t.styles.set((style_1, style_2))

    def test_teacher_creation(self):
        t = Teacher.objects.get(first_name='Ben')
        self.assertTrue(isinstance(t, Teacher))
        self.assertEqual(t.nickname, f'{t.first_name} {t.last_name}')
        self.assertEqual(str(t), t.nickname)
        self.assertEqual(t.slug, slugify(t.nickname))
        self.assertEqual(t.get_absolute_url(), f'/teachers/{t.slug}')
        self.assertIn(Style.objects.get(pk=1), t.styles.all())

    def test_category_deletion(self):
        t = Teacher.objects.get(pk=1)
        c = Category.objects.get(name='Cat')
        c.delete()
        t = Teacher.objects.get(pk=1)
        self.assertIs(t.category, None)

    @classmethod
    def tearDownClass(cls):
        Style.objects.all().delete()
        Teacher.objects.all().delete()
        Category.objects.all().delete()


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
        self.assertEqual(str(group), 'TestStyle with Anna Trincher every Mon-Thu at 18:00:00')

    def test_get_days_property(self):
        group = Group.objects.get(pk=1)
        self.assertEqual(group.get_days, 'Mon-Thu')
