from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
import datetime


def year_validator(value):
    current_year = datetime.date.today().year
    MinValueValidator(1700)
    MaxValueValidator(current_year)
    RegexValidator(
                regex=r"\d\d\d\d",
                message='Year must be 4 digits',
                code='invalid_year'
            )
