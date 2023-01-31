import datetime
import decimal

from django.test import TestCase
from django.utils.text import slugify

from ..models import Category, Style, Teacher, Group, Abonement


class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='TestCat', salary=100.009)

    def test_category_creation(self):
        with self.assertRaises(decimal.InvalidOperation):
            Category.objects.create(name='TestCatFoo', salary=100000)

    def test_category(self):
        cat = Category.objects.get(name='TestCat')
        self.assertTrue(isinstance(cat, Category))
        self.assertEqual(str(cat), cat.name)

    def test_category_salary(self):
        cat = Category.objects.get(name='TestCat')
        self.assertTrue(isinstance(cat.salary, decimal.Decimal))
        self.assertEqual(cat.salary, decimal.Decimal('100.01'))

    @classmethod
    def tearDownClass(cls):
        Category.objects.all().delete()


class TestStyleModel(TestCase):
    def setUp(self, name='Testing', description='Fake style for testing', photo=None, slug=None) -> None:
        Style.objects.create(name=name, description=description, photo=photo, slug=slug)

    def test_style_creation(self):
        s = Style.objects.get(name='Testing')
        self.assertTrue(isinstance(s, Style))
        self.assertEqual(str(s), s.name)
        self.assertEqual(s.slug, 'testing')
        self.assertEqual(s.get_absolute_url(), f'/styles/{s.slug}')

    @classmethod
    def tearDownClass(cls):
        Style.objects.all().delete()


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
        self.assertIn(Style.objects.get(name='style_1'), t.styles.all())

    def test_category_deletion(self):
        t = Teacher.objects.get(last_name='Howitz')
        c = Category.objects.get(name='Cat')
        c.delete()
        t = Teacher.objects.get(last_name='Howitz')
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
        group = Group.objects.get(level=0)
        self.assertTrue(isinstance(group, Group))
        self.assertEqual(str(group), 'TestStyle with Anna Trincher every Mon-Thu at 18:00:00')

    def test_get_days_property(self):
        group = Group.objects.get(level=0)
        self.assertEqual(group.get_days, 'Mon-Thu')

    @classmethod
    def tearDownClass(cls):
        Group.objects.all().delete()
        Teacher.objects.all().delete()
        Style.objects.all().delete()
        Category.objects.all().delete()


class TestAbonementModel(TestCase):
    @classmethod
    def setUpClass(cls):
        category = Category.objects.create(name='Cat', salary=100.0)
        abonement = Abonement.objects.create(category=category, number_of_lessons=16, price=1200, duration=30,
                                             photo=None)

    def test_abonement(self):
        abonement = Abonement.objects.get(price=1200)
        self.assertTrue(isinstance(abonement, Abonement))
        self.assertEqual(str(abonement), 'Cat-16')
        self.assertTrue(isinstance(abonement.price, decimal.Decimal))

    @classmethod
    def tearDownClass(cls):
        Category.objects.all().delete()
        Abonement.objects.all().delete()

