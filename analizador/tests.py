from django.test import TestCase
from django.urls import reverse

from .models import NumberConversion


class NumberAnalysisTests(TestCase):
    def post_number(self, number, bits):
        return self.client.post(reverse('home'), {
            'form_type': 'number',
            'number': str(number),
            'bits': str(bits),
        })

    def test_negative_one_in_8_bit_twos_complement(self):
        response = self.post_number(-1, 8)
        self.assertContains(response, '1111 1111')
        self.assertContains(response, '0xFF')
        self.assertContains(response, '377')
        self.assertContains(response, 'Bit de signo (MSB):')
        self.assertContains(response, 'Interpretado sin signo:')
        self.assertContains(response, '>255</b>')

    def test_negative_128_in_8_bit_twos_complement(self):
        response = self.post_number(-128, 8)
        self.assertContains(response, '1000 0000')
        self.assertContains(response, '0x80')
        self.assertContains(response, '200')
        self.assertContains(response, '>128</b>')

    def test_positive_value_in_16_bits(self):
        response = self.post_number(258, 16)
        self.assertContains(response, '0000 0001 0000 0010')
        self.assertContains(response, '0x0102')
        self.assertContains(response, '000402')

    def test_32_bit_minimum_is_valid(self):
        response = self.post_number(-2147483648, 32)
        self.assertContains(response, '1000 0000 0000 0000 0000 0000 0000 0000')
        self.assertContains(response, '0x80000000')
        self.assertContains(response, '2147483648')

    def test_value_outside_selected_range_is_rejected(self):
        response = self.post_number(128, 8)
        self.assertContains(response, 'entre -128 y 127')
        self.assertEqual(NumberConversion.objects.count(), 0)

    def test_non_numeric_value_is_rejected(self):
        response = self.post_number('doce', 8)
        self.assertContains(response, 'Ingresa un número entero decimal válido.')

    def test_empty_number_is_rejected(self):
        response = self.post_number('', 8)
        self.assertContains(response, 'Escribe un número entero decimal.')

    def test_invalid_bit_size_is_rejected(self):
        response = self.client.post(reverse('home'), {
            'form_type': 'number', 'number': '1', 'bits': '7',
        })
        self.assertContains(response, 'Selecciona un tamaño válido: 8, 16 o 32 bits.')

    def test_history_keeps_only_the_latest_ten_conversions(self):
        for value in range(12):
            response = self.post_number(value, 8)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(NumberConversion.objects.count(), 10)
        self.assertEqual(
            list(NumberConversion.objects.values_list('value', flat=True)),
            list(range(11, 1, -1)),
        )


class TextAnalysisTests(TestCase):
    def post_text(self, text):
        return self.client.post(reverse('home'), {
            'form_type': 'text',
            'text': text,
        })

    def test_text_with_enye_shows_utf8_and_utf16_byte_counts(self):
        response = self.post_text('ñ')
        self.assertContains(response, 'U+00F1')
        self.assertContains(response, 'C3 B1')
        self.assertContains(response, 'Total UTF-8:')
        self.assertContains(response, 'Total UTF-16:')
        self.assertContains(response, '2 bytes')

    def test_text_with_emoji_shows_utf8_and_utf16_byte_counts(self):
        response = self.post_text('😀')
        self.assertContains(response, 'U+1F600')
        self.assertContains(response, 'F0 9F 98 80')
        self.assertContains(response, '4 bytes')

    def test_text_totals_are_summed_for_mixed_characters(self):
        response = self.post_text('ñ😀')
        self.assertContains(response, '6 bytes')
        self.assertContains(response, 'U+00F1')
        self.assertContains(response, 'U+1F600')

    def test_text_longer_than_fifteen_characters_is_rejected(self):
        response = self.post_text('a' * 16)
        self.assertContains(response, 'El texto no puede superar los 15 caracteres.')

    def test_empty_text_is_rejected(self):
        response = self.post_text('')
        self.assertContains(response, 'Escribe un texto para analizar.')
