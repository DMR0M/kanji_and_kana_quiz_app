from django.contrib import admin

from .models import KanjiQuiz, HiraganaQuiz, KatakanaQuiz


admin.site.register(KanjiQuiz)
admin.site.register(HiraganaQuiz)
admin.site.register(KatakanaQuiz)
