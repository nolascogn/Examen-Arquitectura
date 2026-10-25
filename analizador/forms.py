import re

from django import forms


class NumberForm(forms.Form):
    number = forms.CharField(
        label='Entero decimal',
        max_length=11,
        required=False,
        strip=True,
        error_messages={
            'max_length': 'El entero está fuera del rango permitido para 8, 16 o 32 bits.',
        },
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'p. ej. -128',
            'inputmode': 'numeric',
            'spellcheck': 'false',
        }),
    )
    bits = forms.ChoiceField(
        label='Tamaño en bits',
        choices=((8, '8 bits'), (16, '16 bits'), (32, '32 bits')),
        initial=8,
        error_messages={
            'invalid_choice': 'Selecciona un tamaño válido: 8, 16 o 32 bits.',
        },
    )

    def clean_number(self):
        number = self.cleaned_data['number']
        if not number:
            raise forms.ValidationError('Escribe un número entero decimal.')
        if not re.fullmatch(r'[+-]?\d+', number):
            raise forms.ValidationError('Ingresa un número entero decimal válido.')
        return int(number)

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        bits = cleaned_data.get('bits')
        if number is None or bits is None:
            return cleaned_data

        bit_size = int(bits)
        minimum = -(1 << (bit_size - 1))
        maximum = (1 << (bit_size - 1)) - 1
        if not minimum <= number <= maximum:
            self.add_error(
                'number',
                f'Para {bit_size} bits, el valor debe estar entre {minimum:,} y {maximum:,}.'.replace(',', ' '),
            )
        return cleaned_data


class TextForm(forms.Form):
    text = forms.CharField(
        label='Texto',
        max_length=15,
        required=False,
        strip=False,
        error_messages={'max_length': 'El texto no puede superar los 15 caracteres.'},
        widget=forms.TextInput(attrs={
            'maxlength': 15,
            'placeholder': 'Escribe hasta 15 caracteres',
        }),
    )

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError('Escribe un texto para analizar.')
        return text
