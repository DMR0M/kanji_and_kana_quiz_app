from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('kanji_list', views.get_kanji_words, name='kanji_list'),
    path('kanji_quiz', views.get_quiz_data, name='kanji_quiz'),
    path('submit_answers', views.answers_submit_view, name='submit_answers'),
    path('add_kanji_definition', views.add_quiz_view, name='add_kanji_definition'),
    path('post_quiz', views.process_add_quiz_data_entry, name='insert_kanji_definition'),
    path('your_score', views.score_view, name='your_score'),
    path('quiz_results', views.quiz_results_view, name='quiz_results'),
]
