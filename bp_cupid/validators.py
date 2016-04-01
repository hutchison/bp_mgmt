from django.core.validators import RegexValidator

telefon_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Telefonnummer muss von folgendem Format sein: '+999999999'. "
    "Es sind bis zu 15 Ziffern erlaubt."
)
