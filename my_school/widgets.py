# widgets.py
from django_countries.widgets import CountrySelectWidget as BaseCountrySelectWidget

class CountrySelectWidget(BaseCountrySelectWidget):
    def __len__(self):
        return len(self.choices)
