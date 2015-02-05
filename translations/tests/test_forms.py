from django.test import TestCase

from translations.forms import TMForm, EMPTY_ITEM_ERROR

class TMFormTest(TestCase):

    def test_form_render_html(self):
        tmform = TMForm()
        self.assertIn('placeholder="Enter source text"', tmform.as_p())
        self.assertIn('placeholder="Enter target text"', tmform.as_p())
        self.assertIn('class="form-control"', tmform.as_p())

    def test_form_validation_for_blanks(self):
        new_form = TMForm(
            data={
            'source':'',
            'target':''})
        self.assertFalse(new_form.is_valid())
        self.assertEqual(
            new_form.errors['source'],
            [EMPTY_ITEM_ERROR])
        self.assertEqual(
            new_form.errors['target'],
            [EMPTY_ITEM_ERROR])
        
