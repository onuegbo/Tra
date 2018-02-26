from django.test import TestCase
from ..models import Company



class AuthorModelTest(TestCase):

        @classmethod
        def setUpTestData(cls):
            #Set up non-modified objects used by all test methods
            Company.objects.create(company_name='Sogatra',  location = 'pk8', numero_telephone = '07635581', description='Best Transport.')



        def test_first_name_label(self):
            company=Company.objects.get(id=1)
            field_label = company._meta.get_field('company_name').verbose_name
            self.assertEquals(field_label,'company name')

        def test_location_label(self):
                company=Company.objects.get(id=1)
                field_label = company._meta.get_field('location').verbose_name
                self.assertEquals(field_label,'location')

        def test_company_name_max_length(self):
                company=Company.objects.get(id=1)
                max_length = company._meta.get_field('company_name').max_length
                self.assertEquals(max_length,50)

        def test_teephone_label(self):
            company=Company.objects.get(id=1)
            field_label = company._meta.get_field('numero_telephone').verbose_name
            self.assertEquals(field_label,'numero telephone')


        def test_object_name_is_last_name_comma_first_name(self):
                company=Company.objects.get(id=1)
                expected_object_name = '%s' % (company.company_name)
                self.assertEquals(expected_object_name,str(company))

        def test_get_absolute_url(self):
                company=Company.objects.get(id=1)
                #This will also fail if the urlconf is not defined.
                self.assertEquals(company.get_absolute_url(),'/etrans/companys/1/')

        































class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(True)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)