from django.forms import Form, ModelForm, Textarea, TextInput, HiddenInput, ModelChoiceField
from WIMPsite.models import TestStrip, ChemicalTest, Color, ScheduledTest


def __all__():
    return [TestStripForm, ChemicalTestForm, ColorForm]


class TestStripForm(ModelForm):
    class Meta:
        model = TestStrip
        fields = ["name"]
        widgets = {
            "name": TextInput
        }


class ChemicalTestForm(ModelForm):
    class Meta:
        model = ChemicalTest
        fields = ["name", "unit", "test"]
        widgets = {
            'name': TextInput,
            "unit": TextInput,
            "test": HiddenInput
        }


class ColorForm(ModelForm):
    class Meta:
        model = Color
        fields = ["r", "g", "b", "text", "unit_value", "test"]

        widgets = {
            "test": HiddenInput
        }
