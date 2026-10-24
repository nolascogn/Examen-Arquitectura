from django import forms


class NumberForm(forms.Form):
    BASES = (
        ('2', 'Binaria (base 2)'),
        ('8', 'Octal (base 8)'),
        ('10', 'Decimal (base 10)'),
        ('16', 'Hexadecimal (base 16)'),
    )

    number = forms.CharField(
        label='Número',
        max_length=65,
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'p. ej. 11010110',
            'spellcheck': 'false',
        }),
    )
    base = forms.ChoiceField(label='Base de origen', choices=BASES)

    def clean_number(self):
        number = self.cleaned_data['number']
        if not number:
            raise forms.ValidationError('Escribe un número para analizar.')
        if number.startswith('-'):
            raise forms.ValidationError('No se permiten valores negativos.')

        base_digits = {
            2: '01',
            8: '0-7',
            10: '0-9',
            16: '0-9A-Fa-f',
        }
        try:
            base = int(self.data.get('base', 10))
        except (TypeError, ValueError):
            raise forms.ValidationError('Seleccione una base válida.')
        if base not in base_digits:
            raise forms.ValidationError('Seleccione una base válida.')
        import re
        if not re.fullmatch(f'[{base_digits[base]}]+', number):
            allowed = {2: '0 y 1', 8: '0 a 7', 10: '0 a 9', 16: '0 a 9 y A a F'}
            raise forms.ValidationError(
                f'El número no es válido en base {base}; use dígitos {allowed[base]}.'
            )
        try:
            value = int(number, base)
        except ValueError:
            raise forms.ValidationError('El número no es válido para la base seleccionada.')

        if value > 65_535:
            raise forms.ValidationError('El valor debe estar entre 0 y 65 535.')
        return value


class TextForm(forms.Form):
    text = forms.CharField(
        label='Texto',
        max_length=20,
        required=False,
        strip=False,
        widget=forms.TextInput(attrs={
            'maxlength': 20,
            'placeholder': 'Escribe hasta 20 caracteres',
        }),
    )

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError('Escribe un texto para analizar.')
        return text