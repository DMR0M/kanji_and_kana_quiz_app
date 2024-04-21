from django.db import models
from django.utils import timezone


# Kanji Definition Model
class KanjiQuiz(models.Model):
    kanji_character = models.CharField(max_length=50)
    hiragana_character = models.CharField(max_length=100)
    reading = models.CharField(max_length=100)
    meaning = models.CharField(max_length=200)

    def __str__(self):
        return f"Kanji Character: {self.kanji_character}"
    
    
# Hiragana Definition Model
class HiraganaQuiz(models.Model):
    hiragana_character = models.CharField(max_length=100)
    reading = models.CharField(max_length=200)
    meaning = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Hiragana Character: {self.hiragana_character}"
    

# Hiragana Definition Model
class KatakanaQuiz(models.Model):
    katakana_character = models.CharField(max_length=100)
    reading = models.CharField(max_length=200)
    meaning = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Hiragana Character: {self.katakana_character}"


# Scores Model
class Score(models.Model):
    total_score = models.IntegerField()
    question_count = models.IntegerField()
    data_answered = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"Total Score: {self.total_score}/{self.question_count}"


class Questionnaire(models.Model):
    quiz_taker_name = models.CharField(max_length=200)
    quiz_name = models.CharField(max_length=100, default="Business Kanji Quiz")
    date_answered = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"Quiz Data {str(self.date_answered)}"


class QuestionnaireResults(models.Model):
    kanji_character = models.CharField(max_length=50)
    correct_reading_answer = models.CharField(max_length=100)
    reading_answer = models.CharField(max_length=100)
    correct_meaning_answer = models.CharField(max_length=200)
    meaning_answer = models.CharField(max_length=200)
    date_answered = models.DateField(default=timezone.now)
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Questions and Answers {str(self.date_answered)}"


class QuizSettings(models.Model):
    quiz_hiragana_question_count = models.IntegerField()
    quiz_katakana_question_count = models.IntegerField()
    quiz_kanji_question_count = models.IntegerField()
    date_modified = models.DateField(default=timezone.now)
