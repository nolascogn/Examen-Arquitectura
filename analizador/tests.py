from django.test import TestCase
from django.urls import reverse


class NumberAnalysisTests(TestCase):
    def test_binary_conversion_is_padded_to_a_byte(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '101', 'base': '2',
        })
        self.assertContains(response, '00000101')
        self.assertContains(response, '5')

    def test_octal_conversion(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '17', 'base': '8',
        })
        self.assertContains(response, '15')
        self.assertContains(response, '1111')

    def test_hexadecimal_conversion_at_upper_limit(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': 'FFFF', 'base': '16',
        })
        self.assertContains(response, '65535')
        self.assertContains(response, '1111111111111111')

    def test_invalid_digit_for_base_is_rejected(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '102', 'base': '2',
        })
        self.assertContains(response, 'no es válido en base 2')

    def test_separator_is_not_accepted_as_a_digit(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '1_0', 'base': '10',
        })
        self.assertContains(response, 'no es válido en base 10')

    def test_empty_number_has_a_clear_error(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '', 'base': '10',
        })
        self.assertContains(response, 'Escribe un número para analizar.')

    def test_empty_text_has_a_clear_error(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'text', 'text': '',
        })
        self.assertContains(response, 'Escribe un texto para analizar.')

    def test_value_above_range_is_rejected(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '65536', 'base': '10',
        })
        self.assertContains(response, 'entre 0 y 65 535')

    def test_negative_value_is_rejected(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '-1', 'base': '10',
        })
        self.assertContains(response, 'No se permiten valores negativos')

    def test_utf8_analysis_for_enye(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'text', 'text': 'ñ',
        })
        self.assertContains(response, 'U+00F1')
        self.assertContains(response, 'C3 B1')