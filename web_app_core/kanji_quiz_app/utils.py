from random import shuffle, sample

from .models import KanjiQuiz, HiraganaQuiz, KatakanaQuiz


# Generates 10 random japanese words from database 
# depending if it is Hiragana, Katakana, or Kanji
def util_generate_quiz_data(jap_lang, size=10) -> list[str]:
    quiz_characters_list = []
    
    if "kanji" == jap_lang.casefold():
        quiz_characters_list: list[tuple] = KanjiQuiz.objects.all().values_list("kanji_character", flat=True)
        quiz_characters_list = sample(list(quiz_characters_list), size)
    elif "hiragana" == jap_lang.casefold():
        quiz_characters_list: list[tuple] = HiraganaQuiz.objects.all().values_list("hiragana_character", flat=True)
        quiz_characters_list = sample(list(quiz_characters_list), size)
    elif "katakana" == jap_lang.casefold():
        quiz_characters_list: list[tuple] = KatakanaQuiz.objects.all().values_list("katakana_character", flat=True)
        quiz_characters_list = sample(list(quiz_characters_list), size)
    
    shuffle(quiz_characters_list)
    
    return quiz_characters_list


# Get the correct reading and meaning of a given kanji_characters_list
def util_get_correct_quiz_answers(jap_lang, questions, answer_type) -> list[str]:
    answers = []
    
    if "kanji" == jap_lang.casefold():
        # Return an empty list if inputs are not of the expected types
        if not isinstance(questions, list) or not isinstance(answer_type, str):
            return answers  
        
        if "reading" == answer_type.casefold():
            for kanji in questions:
                result_set = KanjiQuiz.objects.filter(kanji_character=kanji)

                answers.append(result_set.first().reading)
                
        elif "meaning" == answer_type.casefold():
            for kanji in questions:
                result_set = KanjiQuiz.objects.filter(kanji_character=kanji)
                
                answers.append(result_set.first().meaning)
                
    elif "hiragana" == jap_lang.casefold():
        # Return an empty list if inputs are not of the expected types
        if not isinstance(questions, list) or not isinstance(answer_type, str):
            return answers  
        
        if "reading" == answer_type.casefold():
            for hiragana in questions:
                result_set = HiraganaQuiz.objects.filter(hiragana_character=hiragana)

                answers.append(result_set.first().reading)
                
        elif "meaning" == answer_type.casefold():
            for hiragana in questions:
                result_set = HiraganaQuiz.objects.filter(hiragana_character=hiragana)
                
                answers.append(result_set.first().meaning)
                
    elif "katakana" == jap_lang.casefold():
        # Return an empty list if inputs are not of the expected types
        if not isinstance(questions, list) or not isinstance(answer_type, str):
            return answers  
        
        if "reading" == answer_type.casefold():
            for katakana in questions:
                result_set = KatakanaQuiz.objects.filter(katakana_character=katakana)

                answers.append(result_set.first().reading)
                
        elif "meaning" == answer_type.casefold():
            for katakana in questions:
                result_set = KatakanaQuiz.objects.filter(katakana_character=katakana)
                
                answers.append(result_set.first().meaning)
    
    return answers


# Generates total score based on quiz answers
def util_get_quiz_score(jap_lang, reading_answers, meaning_answers, questions) -> int:
    reading_answers = list(map(lambda x: x.casefold(), reading_answers))
    meaning_answers = list(map(lambda x: x.casefold(), meaning_answers))
    
    total_score = 0
    
    if "kanji" == jap_lang.casefold():
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
        
        for data in zip(questions, reading_answers, meaning_answers):
                kanji = data[0]         # kanji_questions_value
                read_ans = data[1]      # reading_answers_value
                mean_ans = data[2]      # meaning_answer_value
                
                if reading_lookup[kanji] == read_ans.replace(" ", ""):
                    total_score += 1
                    
                if mean_ans.replace(" ", "") in meaning_lookup[kanji]:
                    total_score += 1
                    
    elif "hiragana" == jap_lang.casefold():
        correct_answers_reading: list[tuple] = HiraganaQuiz.objects.all().values_list(
            "hiragana_character", "reading"
        )
        correct_answers_meaning: list[tuple] = HiraganaQuiz.objects.all().values_list(
            "hiragana_character", "meaning"
        )
    
        reading_lookup = dict(correct_answers_reading)
        meaning_lookup = dict(correct_answers_meaning)
        
        for meaning in meaning_lookup:
            meaning_lookup[meaning] = list(map(lambda x: x.replace(" ", ""), meaning_lookup[meaning].split(";")))
        
        for data in zip(questions, reading_answers, meaning_answers):
                hiragana = data[0]         # hiragana_questions_value
                read_ans = data[1]      # reading_answers_value
                mean_ans = data[2]      # meaning_answer_value
                
                if reading_lookup[hiragana] == read_ans.replace(" ", ""):
                    total_score += 1
                    
                if mean_ans.replace(" ", "") in meaning_lookup[hiragana]:
                    total_score += 1
    
    elif "katakana" == jap_lang.casefold():
        correct_answers_reading: list[tuple] = KatakanaQuiz.objects.all().values_list(
            "katakana_character", "reading"
        )
        correct_answers_meaning: list[tuple] = KatakanaQuiz.objects.all().values_list(
            "katakana_character", "meaning"
        )
    
        reading_lookup = dict(correct_answers_reading)
        meaning_lookup = dict(correct_answers_meaning)
        
        for meaning in meaning_lookup:
            meaning_lookup[meaning] = list(map(lambda x: x.replace(" ", ""), meaning_lookup[meaning].split(";")))
        
        for data in zip(questions, reading_answers, meaning_answers):
                katakana = data[0]         # katakana_questions_value
                read_ans = data[1]      # reading_answers_value
                mean_ans = data[2]      # meaning_answer_value
                
                if reading_lookup[katakana] == read_ans.replace(" ", ""):
                    total_score += 1
                    
                if mean_ans.replace(" ", "") in meaning_lookup[katakana]:
                    total_score += 1
    
    return total_score


# Convert all words to lowercase
def util_convert_to_lowercase(*args) -> list[str]:
    return list(map(lambda x: x.casefold(), args))


# Removes character ; and ,
def util_remove_characters(*args) -> list[str]:
    return list(map(lambda x: x.replace(";", "").replace(",",""), args))