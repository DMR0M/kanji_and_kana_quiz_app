from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import (
    KanjiQuiz, 
    HiraganaQuiz,
    KatakanaQuiz,
    Score, 
    Questionnaire, 
    QuestionnaireResults,
)
from .forms import AddKanjiDefinitionForm
from .utils import (
    util_generate_quiz_data, 
    util_get_correct_quiz_answers,
    util_get_quiz_score,
)

# Landing Page
def home(request):
    return render(request, "home.html", {})


# Kanji Master List Definition Page
def get_kanji_words(request):
    kanji_list = KanjiQuiz.objects.order_by('id').all()
    context = {"kanji_list": kanji_list}
    return render(request, "listKanji.html", context)


# Hiragana Master List Definition Page
def get_hiragana_words(request):
    hiragana_list = HiraganaQuiz.objects.order_by('id').all()
    context = {"hiragana_list": hiragana_list}
    return render(request, "listHiragana.html", context)


# Katakana Master List Definition Page
def get_katakana_words(request):
    katakana_list = KatakanaQuiz.objects.order_by('id').all()
    context = {"katakana_list": katakana_list}
    return render(request, "listKatakana.html", context)


# Get Kanji Characters for Quiz Page
def get_kanji_quiz_data(request):
    # Get 10 kanji characters from the list and shuffle the order of the characters
    kanji_list = util_generate_quiz_data("kanji")
    
    context = {"randomize_kanji_list": kanji_list}
    
    # Send the randomized list of kanji characters to the quiz results page
    render(request, "quizResults.html", context)
    
    return render(request, "quizPage.html", context)


# Get Hiragana Characters for Quiz Page
def get_hiragana_quiz_data(request):
    hiragana_list = util_generate_quiz_data("hiragana")
    
    context = {"randomize_hiragana_list": hiragana_list}
    
    return render(request, "hiraganaQuizPage.html", context)


# Get Katakana Characters for Quiz Page
def get_katakana_quiz_data(request):
    katakana_list = util_generate_quiz_data("katakana")
    
    context = {"randomize_katakana_list": katakana_list}
    
    return render(request, "katakanaQuizPage.html", context)


# Add data to Kanji Definitions Table
def add_quiz_view(request):
    context = {}
    context["form"] = AddKanjiDefinitionForm()
    return render(request, "addKanji.html", context)


# Handle Form Submission of Answers in Kanji Quiz Page
def answers_submit_view(request):
    reading_answers = []
    meaning_answers = []
    kanji_questions = []
    
    if request.method == "POST":
        quiz_taker_name = request.POST.get("name_value")
        
        for key, value in request.POST.items():
            if key.startswith("reading_answer_"):
                reading_answers.append(value)
            elif key.startswith("meaning_answer_"):
                meaning_answers.append(value)
            elif key.startswith("kanji_questions_"):
                kanji_questions.append(value)
                
        # Get the total score
        total_score = util_get_quiz_score("Kanji", reading_answers, meaning_answers, kanji_questions)
        # Get the total question count
        question_count = len(reading_answers) + len(meaning_answers)
        # Get the correct reading answers
        correct_reading_answers = util_get_correct_quiz_answers("Kanji", kanji_questions, "reading")
        # Get the correct meaning answers
        correct_meaning_answers = util_get_correct_quiz_answers("Kanji", kanji_questions, "meaning")
        
        questionnaire = Questionnaire.objects.create(
            quiz_taker_name=quiz_taker_name,
        )
        
        question_and_answer_lookup = list(zip(correct_reading_answers, reading_answers, correct_meaning_answers, meaning_answers, kanji_questions))
            
        for c_reading, reading, c_meaning, meaning, kanji_character in question_and_answer_lookup:
            QuestionnaireResults.objects.create(
                kanji_character=kanji_character.casefold(),
                correct_reading_answer=c_reading.casefold(),
                reading_answer=reading.casefold(),
                correct_meaning_answer=c_meaning.casefold(),
                meaning_answer=meaning.casefold(),
                questionnaire=questionnaire,
            )
        
        Score.objects.create(total_score=total_score, question_count=question_count)
        
        
        return HttpResponseRedirect('/your_score')
    
    else:
        return HttpResponse('Method not allowed')
    

# Handle Form Submission of Answers in Hiragana Quiz Page
def hiragana_answers_submit_view(request):
    reading_answers = []
    meaning_answers = []
    hiragana_questions = []
    
    if request.method == "POST":
        quiz_taker_name = request.POST.get("name_value")
        
        for key, value in request.POST.items():
            if key.startswith("reading_answer_"):
                reading_answers.append(value)
            elif key.startswith("meaning_answer_"):
                meaning_answers.append(value)
            elif key.startswith("hiragana_questions_"):
                hiragana_questions.append(value)
                
        # Get the total score
        total_score = util_get_quiz_score("Hiragana", reading_answers, meaning_answers, hiragana_questions)
        # Get the total question count
        question_count = len(reading_answers) + len(meaning_answers)
        # Get the correct reading answers
        correct_reading_answers = util_get_correct_quiz_answers("Hiragana", hiragana_questions, "reading")
        print(correct_reading_answers)
        # Get the correct meaning answers
        correct_meaning_answers = util_get_correct_quiz_answers("Hiragana", hiragana_questions, "meaning")
        print(correct_meaning_answers)
        
        questionnaire = Questionnaire.objects.create(
            quiz_name="Hiragana Quiz",
            quiz_taker_name=quiz_taker_name,
        )
        
        question_and_answer_lookup = list(zip(correct_reading_answers, reading_answers, correct_meaning_answers, meaning_answers, hiragana_questions))
        
        print(question_and_answer_lookup)
        
        for c_reading, reading, c_meaning, meaning, kanji_character in question_and_answer_lookup:
            QuestionnaireResults.objects.create(
                kanji_character=kanji_character.casefold(),
                correct_reading_answer=c_reading.casefold(),
                reading_answer=reading.casefold(),
                correct_meaning_answer=c_meaning.casefold(),
                meaning_answer=meaning.casefold(),
                questionnaire=questionnaire,
            )
        
        Score.objects.create(total_score=total_score, question_count=question_count)
        
        
        return HttpResponseRedirect('/your_score_hiragana_quiz')
    
    else:
        return HttpResponse('Method not allowed')


# Handle Form Submission of Answers in Katakana Quiz Page
def katakana_answers_submit_view(request):
    reading_answers = []
    meaning_answers = []
    katakana_questions = []
    
    if request.method == "POST":
        quiz_taker_name = request.POST.get("name_value")
        
        for key, value in request.POST.items():
            if key.startswith("reading_answer_"):
                reading_answers.append(value)
            elif key.startswith("meaning_answer_"):
                meaning_answers.append(value)
            elif key.startswith("katakana_questions_"):
                katakana_questions.append(value)
                
        # Get the total score
        total_score = util_get_quiz_score("Katakana", reading_answers, meaning_answers, katakana_questions)
        # Get the total question count
        question_count = len(reading_answers) + len(meaning_answers)
        # Get the correct reading answers
        correct_reading_answers = util_get_correct_quiz_answers("Katakana", katakana_questions, "reading")
        # Get the correct meaning answers
        correct_meaning_answers = util_get_correct_quiz_answers("Katakana", katakana_questions, "meaning")
        
        questionnaire = Questionnaire.objects.create(
            quiz_name="Katakana Quiz",
            quiz_taker_name=quiz_taker_name,
        )
        
        question_and_answer_lookup = list(zip(correct_reading_answers, reading_answers, correct_meaning_answers, meaning_answers, katakana_questions))
        
        print(question_and_answer_lookup)
        
        for c_reading, reading, c_meaning, meaning, katakana_character in question_and_answer_lookup:
            QuestionnaireResults.objects.create(
                kanji_character=katakana_character.casefold(),
                correct_reading_answer=c_reading.casefold(),
                reading_answer=reading.casefold(),
                correct_meaning_answer=c_meaning.casefold(),
                meaning_answer=meaning.casefold(),
                questionnaire=questionnaire,
            )
        
        Score.objects.create(total_score=total_score, question_count=question_count)
        
        
        return HttpResponseRedirect('/your_score_katakana_quiz')
    
    else:
        return HttpResponse('Method not allowed')
    

# Display score page with the user's score based on the quiz taken
def score_view(request):
    score_list = Score.objects.last()
    context = {"score_list": score_list}
    return render(request, "scorePage.html", context)


# Display score page with the user's score based on the quiz taken
def hiragana_score_view(request):
    score_list = Score.objects.last()
    context = {"score_list": score_list}
    return render(request, "hiraganaScorePage.html", context)


# Display score page with the user's score based on the quiz taken
def katakana_score_view(request):
    score_list = Score.objects.last()
    context = {"score_list": score_list}
    return render(request, "katakanaScorePage.html", context)


# Process Inserting Data to Kanji Definitions Table
def process_add_quiz_data_entry(request):
    if request.method == "POST":
        kanji_character_input = request.POST.get("kanji_character")
        hiragana_character_input = request.POST.get("hiragana_character")
        reading_input = request.POST.get("reading")
        meaning_input = request.POST.get("meaning")
        
        # Get the latest record's id and increment by 1 for insertion
        # else set it to 1 
        latest_record = KanjiQuiz.objects.order_by('-id').first()
        
        if latest_record:
            kanji_id = latest_record.id + 1
        else:
            kanji_id = 1

        # Instantiate Entity From KanjiQuiz Model
        kanji_quiz_entity = KanjiQuiz(
            id=kanji_id,
            kanji_character=kanji_character_input, 
            hiragana_character=hiragana_character_input,
            reading=reading_input,    
            meaning=meaning_input,
        )
        kanji_quiz_entity.save()
        messages.success(request, "Kanji Definitions Updated Successfully!")
        
        return HttpResponseRedirect('/add_kanji_definition')
    
    else:
        return HttpResponse("Invalid Data")


def quiz_results_view(request):
    context = {}
    
    # Get the latest questionnaire
    latest_questionnaire = Questionnaire.objects.order_by("-id").first()
    # Get the latest total score
    latest_score_record = Score.objects.latest("id")
    latest_total_score = getattr(latest_score_record, "total_score", None)
    
    # print(latest_total_score)
    context["total_score"] = str(latest_total_score)
    
    if latest_questionnaire:
        # Get the latest questionnaire results
        latest_questionnaire_results = latest_questionnaire.questionnaireresults_set.all().order_by("id")

        context = {
            "questionnaire_results": latest_questionnaire_results,
        }
        
        return render(request, "quizResults.html", context)
    else:
        return HttpResponse('Method not allowed')
    