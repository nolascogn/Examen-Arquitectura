from django.db import models


class NumberConversion(models.Model):
    value = models.BigIntegerField()
    bits = models.PositiveSmallIntegerField()
    binary = models.CharField(max_length=47)
    hexadecimal = models.CharField(max_length=8)
    octal = models.CharField(max_length=11)
    unsigned_value = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', '-pk')
        verbose_name = 'conversión numérica'
        verbose_name_plural = 'conversiones numéricas'

    def __str__(self):
        return f'{self.value} ({self.bits} bits)'
