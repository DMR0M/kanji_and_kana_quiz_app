from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from random import shuffle, sample

from .models import KanjiQuiz, Score, Questionnaire, QuestionnaireResults
from .forms import AddKanjiDefinitionForm


# Landing Page
def home(request):
    return render(request, "home.html", {})


# Kanji Master List Definition Page
def get_kanji_words(request):
    kanji_list = KanjiQuiz.objects.order_by('id').all()
    context = {"kanji_list": kanji_list}
    return render(request, "listKanji.html", context)


# Convert all words to lowecase
def util_convert_to_lowercase(*args) -> list[str]:
    return list(map(lambda x: x.casefold(), args))


# Removes character ; and ,
def util_remove_characters(*args) -> list[str]:
    return list(map(lambda x: x.replace(";", "").replace(",",""), args))


# Generates 10 random kanji words from database
def util_generate_quiz_data(size=10) -> list[str]:
    kanji_list: list[tuple] = KanjiQuiz.objects.all().values_list("kanji_character", flat=True)
    kanji_list = sample(list(kanji_list), size)
    
    shuffle(kanji_list)
    
    return kanji_list


# Get the correct reading and meaning of a given kanji_characters_list
def util_get_correct_quiz_answers(kanji_questions, answer_type) -> list[str]:
    answers = []
    
    # Return an empty list if inputs are not of the expected types
    if not isinstance(kanji_questions, list) or not isinstance(answer_type, str):
        return answers  
    
    if "reading" == answer_type.casefold():
        for kanji in kanji_questions:
            result_set = KanjiQuiz.objects.filter(kanji_character=kanji)

            answers.append(result_set.first().reading)
            
    elif "meaning" == answer_type.casefold():
        for kanji in kanji_questions:
            result_set = KanjiQuiz.objects.filter(kanji_character=kanji)
            
            answers.append(result_set.first().meaning)
    
    return answers


# Generates total score based on quiz answers
def util_get_quiz_score(reading_answers, meaning_answers, kanji_questions) -> int:
    reading_answers = list(map(lambda x: x.casefold(), reading_answers))
    meaning_answers = list(map(lambda x: x.casefold(), meaning_answers))
    
    total_score = 0
    
    correct_answers_reading: list[tuple] = KanjiQuiz.objects.all().values_list(
        "kanji_character", "reading"
    )
    correct_answers_meaning: list[tuple] = KanjiQuiz.objects.all().values_list(
        "kanji_character", "meaning"
    )
    
    reading_lookup = dict(correct_answers_reading)
    meaning_lookup = dict(correct_answers_meaning)
    
    for meaning in meaning_lookup:
        meaning_lookup[meaning] = list(map(lambda x: x.replace(" ", ""), meaning_lookup[meaning].split(";")))
        
    # print(meaning_lookup)
    
    for data in zip(kanji_questions, reading_answers, meaning_answers):
            kanji = data[0]         # kanji_questions_value
            read_ans = data[1]      # reading_answers_value
            mean_ans = data[2]      # meaning_answer_value
            
            if reading_lookup[kanji] == read_ans.replace(" ", ""):
                total_score += 1
                
            if mean_ans.replace(" ", "") in meaning_lookup[kanji]:
                total_score += 1
    
    return total_score


# Get Kanji Characters for Quiz Page
def get_quiz_data(request):
    # Get 10 kanji characters from the list and shuffle the order of the characters
    kanji_list = util_generate_quiz_data()
    
    context = {"randomize_kanji_list": kanji_list}
    
    # Send the randomized list of kanji characters to the quiz results page
    render(request, "quizResults.html", context)
    
    return render(request, "quizPage.html", context)


def add_quiz_view(request):
    context = {}
    context["form"] = AddKanjiDefinitionForm()
    return render(request, "addKanji.html", context)


# Handle Form Submission of Answers in Quiz Page
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
        total_score = util_get_quiz_score(reading_answers, meaning_answers, kanji_questions)
        # Get the total question count
        question_count = len(reading_answers) + len(meaning_answers)
        # Get the correct reading answers
        correct_reading_answers = util_get_correct_quiz_answers(kanji_questions, "reading")
        # Get the correct meaning answers
        correct_meaning_answers = util_get_correct_quiz_answers(kanji_questions, "meaning")
        
        questionnaire = Questionnaire.objects.create(
            quiz_taker_name=quiz_taker_name.title(),
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
    

# Display score page with the user's score based on the quiz taken
def score_view(request):
    score_list = Score.objects.last()
    context = {"score_list": score_list}
    return render(request, "scorePage.html", context)


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
    
    