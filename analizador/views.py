from django.db import transaction
from django.shortcuts import render

from .forms import NumberForm, TextForm
from .models import NumberConversion


def analyze_number(value, bits):
    unsigned_value = value & ((1 << bits) - 1)
    binary_pattern = format(unsigned_value, f'0{bits}b')
    grouped_binary = ' '.join(
        binary_pattern[index:index + 4]
        for index in range(0, bits, 4)
    )
    return {
        'decimal': value,
        'bits': bits,
        'binary': grouped_binary,
        'hexadecimal': format(unsigned_value, f'0{(bits + 3) // 4}X'),
        'octal': format(unsigned_value, f'0{(bits + 2) // 3}o'),
        'sign_bit': binary_pattern[0],
        'sign_meaning': 'negativo' if binary_pattern[0] == '1' else 'no negativo',
        'unsigned_value': unsigned_value,
    }


def analyze_text(text):
    character_rows = []
    for character in text:
        utf8_bytes = character.encode('utf-8')
        utf16_bytes = character.encode('utf-16-le')
        character_rows.append({
            'character': character,
            'codepoint': f'U+{ord(character):04X}',
            'utf8': ' '.join(f'{byte:02X}' for byte in utf8_bytes),
            'utf8_count': len(utf8_bytes),
            'utf16_count': len(utf16_bytes),
        })

    return {
        'rows': character_rows,
        'utf8_total': sum(row['utf8_count'] for row in character_rows),
        'utf16_total': sum(row['utf16_count'] for row in character_rows),
    }


def home(request):
    number_form = NumberForm()
    text_form = TextForm()
    number_result = None
    text_result = None

    if request.method == 'POST' and request.POST.get('form_type') == 'number':
        number_form = NumberForm(request.POST)
        if number_form.is_valid():
            value = number_form.cleaned_data['number']
            bits = int(number_form.cleaned_data['bits'])
            number_result = analyze_number(value, bits)
            with transaction.atomic():
                NumberConversion.objects.create(
                    value=value,
                    bits=bits,
                    binary=number_result['binary'],
                    hexadecimal=number_result['hexadecimal'],
                    octal=number_result['octal'],
                    unsigned_value=number_result['unsigned_value'],
                )
                old_ids = NumberConversion.objects.order_by(
                    '-created_at', '-pk'
                ).values_list('pk', flat=True)[10:]
                NumberConversion.objects.filter(pk__in=old_ids).delete()

    elif request.method == 'POST' and request.POST.get('form_type') == 'text':
        text_form = TextForm(request.POST)
        if text_form.is_valid():
            text_result = analyze_text(text_form.cleaned_data['text'])

    return render(request, 'analizador/home.html', {
        'number_form': number_form,
        'text_form': text_form,
        'number_result': number_result,
        'text_result': text_result,
        'history': NumberConversion.objects.all()[:10],
    })
