from django.db import models


class LowerCaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        if isinstance(value, str):
            return value.strip().lower()
        return str(value)
