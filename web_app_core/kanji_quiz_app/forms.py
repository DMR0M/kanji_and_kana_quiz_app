from django import forms
from .models import KanjiQuiz


class AddKanjiDefinitionForm(forms.ModelForm):
    class Meta:
        model = KanjiQuiz
        fields = "__all__"

