from django.test import TestCase
from translations.models import TransUnit, TM
        

class TransUnitandTMModelTest(TestCase):


    def test_saving_and_retrieving(self):
        tm = TM()
        tm.save()


        first_translation_unit = TransUnit()
        first_translation_unit.source = "Source"
        first_translation_unit.target = "Target"
        first_translation_unit.tm = tm

        first_translation_unit.save()

        second_translation_unit = TransUnit()
        second_translation_unit.source = 'The 2nd Source'
        second_translation_unit.target = 'snd target'
        second_translation_unit.tm = tm
        second_translation_unit.save()

        saved_tm = TM.objects.first()
        self.assertEqual(saved_tm, tm)


        saved_translation_units = TransUnit.objects.all()

        self.assertEqual(saved_translation_units.count(), 2)
       
        first_saved_translation_unit = saved_translation_units[0]
        second_saved_translation_unit = saved_translation_units[1]

        self.assertEqual(first_translation_unit, first_saved_translation_unit)
        self.assertEqual(first_saved_translation_unit.tm, tm)
        self.assertEqual(second_saved_translation_unit, second_translation_unit)

        self.assertEqual(second_saved_translation_unit.tm, tm)

        