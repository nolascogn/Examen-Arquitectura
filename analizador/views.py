from django.shortcuts import render

from .forms import NumberForm, TextForm


def home(request):
    number_form = NumberForm()
    text_form = TextForm()
    number_result = None
    character_rows = None

    if request.method == 'POST' and request.POST.get('form_type') == 'number':
        number_form = NumberForm(request.POST)
        if number_form.is_valid():
            value = number_form.cleaned_data['number']
            significant_bits = value.bit_length()
            byte_count = max(1, (significant_bits + 7) // 8)
            padded_bits = ((significant_bits + 7) // 8) * 8 or 8
            number_result = {
                'decimal': value,
                'binary': format(value, f'0{padded_bits}b'),
                'octal': format(value, 'o'),
                'hexadecimal': format(value, 'X'),
                'significant_bits': significant_bits,
                'bytes': byte_count,
            }
    elif request.method == 'POST' and request.POST.get('form_type') == 'text':
        text_form = TextForm(request.POST)
        if text_form.is_valid():
            character_rows = [
                {
                    'character': character,
                    'decimal': ord(character),
                    'codepoint': f'U+{ord(character):04X}',
                    'hexadecimal': f'{ord(character):X}',
                    'utf8': ' '.join(f'{byte:02X}' for byte in character.encode('utf-8')),
                }
                for character in text_form.cleaned_data['text']
            ]

    return render(request, 'analizador/home.html', {
        'number_form': number_form,
        'text_form': text_form,
        'number_result': number_result,
        'character_rows': character_rows,
    })