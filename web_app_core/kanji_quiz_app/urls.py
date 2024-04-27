from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('kanji_list', views.get_kanji_words, name='kanji_list'),
    path('basic_kanji_list', views.get_basic_kanji_words, name='basic_kanji_list'),
    path('hiragana_list', views.get_hiragana_words, name='hiragana_list'),
    path('katakana_list', views.get_katakana_words, name='katakana_list'),
    path('kanji_quiz', views.get_kanji_quiz_data, name='kanji_quiz'),
    path('basic_kanji_quiz', views.get_basic_kanji_quiz_data, name='basic_kanji_quiz'),
    path('hiragana_quiz', views.get_hiragana_quiz_data, name='hiragana_quiz'),
    path('katakana_quiz', views.get_katakana_quiz_data, name='katakana_quiz'),
    path('submit_answers', views.answers_submit_view, name='submit_answers'),
    path('basic_kanji_submit_answers', views.basic_kanji_answers_submit_view, name='basic_kanji_submit_answers'),
    path('hiragana_submit_answers', views.hiragana_answers_submit_view, name='hiragana_submit_answers'),
    path('katakana_submit_answers', views.katakana_answers_submit_view, name='katakana_submit_answers'),
    path('add_kanji_definition', views.add_quiz_view, name='add_kanji_definition'),
    path('post_quiz', views.process_add_quiz_data_entry, name='insert_kanji_definition'),
    path('your_score', views.score_view, name='your_score'),
    path('your_score_basic_kanji_quiz', views.basic_kanji_score_view, name='your_score_basic_kanji_quiz'),
    path('your_score_hiragana_quiz', views.hiragana_score_view, name='your_score_hiragana_quiz'),
    path('your_score_katakana_quiz', views.katakana_score_view, name='your_score_katakana_quiz'),
    path('quiz_results', views.quiz_results_view, name='quiz_results'),
    path('quiz_settings', views.quiz_settings_view, name='quiz_settings'),
    path('guessing_game_settings', views.guessing_game_settings_view, name='guessing_game_settings'),
    path('guessing_game', views.guess_kanji_word_view, name="guessing_game"),
]
