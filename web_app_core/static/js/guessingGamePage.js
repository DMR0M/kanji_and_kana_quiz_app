let questionCounter = 0;
let guessValues = [];
let guessValuesCount = document.getElementById("guess-values-count").value;
let correctReadingAnswerValues = [];
let correctMeaningAnswerValues = [];
let answersList1 = [];
let answersList2 = [];
const characterValue = document.getElementById("character-field");

let currAnswerValue1 = document.getElementById("answer-field1").value;
const answerField1 = document.getElementById("answer-field1");

let currAnswerValue2 = document.getElementById("answer-field2").value;
const answerField2 = document.getElementById("answer-field2");

const progressBar = document.getElementById("progress-bar");
const submitAnswersButton = document.getElementById("submit-answers-btn");
const playAgainButton = document.getElementById("play-again-btn");

let isCorrectBadge = document.getElementById("isCorrectBadge");
let isWrongBadge = document.getElementById("isWrongBadge");

let progressValue = 0;
let score = 0;

document.addEventListener('DOMContentLoaded', function() {
    var submitButton = document.getElementById('submit-answers-btn');
    var textInput1 = document.getElementById('answer-field1');
    var textInput2 = document.getElementById('answer-field2');

    function handleKeyPress(event) {
        if (event.keyCode === 13) {
            submitButton.click();
        }
    }

    textInput1.addEventListener('keydown', handleKeyPress);
    textInput2.addEventListener('keydown', handleKeyPress);
});

window.onload = () => {
    let guessCharacters = document.getElementsByClassName("guess-values");
    let correctReadingAnswers = document.getElementsByClassName("correct-reading-answer-values");
    let correctMeaningAnswers = document.getElementsByClassName("correct-meaning-answer-values");

    isCorrectBadge.style.display = "none";
    isWrongBadge.style.display = "none";
    playAgainButton.style.display = "none";

    for (let guessVal of guessCharacters) {
        guessValues.push(guessVal.value);
    }

    for (let correctAnswerVal of correctReadingAnswers) {
        correctReadingAnswerValues.push(correctAnswerVal.value)
    }

    for (let correctAnswerVal of correctMeaningAnswers) {
        correctMeaningAnswerValues.push(correctAnswerVal.value)
    }

    console.log(guessValues);
    console.log(correctReadingAnswerValues);
    console.log(correctMeaningAnswerValues);
    progressBar.innerText = progressValue + '%';
    characterValue.innerText = guessValues[questionCounter]
};

const handleSubmitAnswer = () => {
    if (submitAnswersButton.innerText == "Review Kanji Definition") {
        window.location.href = "/kanji_list";
    }

    if (questionCounter == Number(guessValuesCount) - 1) {
        submitAnswersButton.innerText = "Review Kanji Definition";
        answerField1.style.display = "none";
        answerField2.style.display = "none";
        playAgainButton.style.display = "";
    }

    if (questionCounter < Number(guessValuesCount)) {
        questionCounter++;

        currAnswerValue1 = document.getElementById("answer-field1").value;
        currAnswerValue2 = document.getElementById("answer-field2").value;
        answersList1.push(currAnswerValue1);
        answersList2.push(currAnswerValue2);

        evaluateAnswer(currAnswerValue1, currAnswerValue2);

        progressValue += (1 / Number(guessValuesCount)) * 100;
        progressBar.style.width = progressValue + '%';
        progressBar.setAttribute('aria-valuenow', progressValue);
        progressBar.innerText = progressValue + '%';

        console.log(score);
        document.getElementById("answer-field1").value = "";
        document.getElementById("answer-field2").value = "";
        characterValue.innerText = questionCounter < Number(guessValuesCount) ? guessValues[questionCounter] : `${score}/${guessValues.length}`;
    }
    console.log(answersList1)
    console.log(answersList2)

}

const evaluateAnswer = (readingAnswer, meaningAnswer) => {
    console.log(readingAnswer);
    console.log(meaningAnswer);
    console.log(correctReadingAnswerValues[questionCounter])
    if (readingAnswer.toLowerCase() === correctReadingAnswerValues[questionCounter - 1] &&
        meaningAnswer.toLowerCase() === correctMeaningAnswerValues[questionCounter - 1]) {
        score++;
        isCorrectBadge.style.display = '';
        isWrongBadge.style.display = 'none';
    } else {
        isCorrectBadge.style.display = 'none';
        isWrongBadge.style.display = '';
    }
}

const playAgain = () => {
    window.location.reload();
}