from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob

from src.ml_model import predict_score
from src.semantic_analyzer import calculate_topic_relevance
from src.plagiarism import calculate_plagiarism


def analyze_essay(text,topic,previous_essays=None):

    if previous_essays is None:
        previous_essays=[]

    sentences=sent_tokenize(text)
    words=word_tokenize(text)

    clean_words=[
        word.lower()
        for word in words
        if word.isalpha()
    ]

    word_count=len(clean_words)
    sentence_count=len(sentences)
    unique_words=len(set(clean_words))

    reading_time=round(word_count/200,2)

    paragraph_count=len(
        [p for p in text.split("\n") if p.strip()]
    )

    avg_sentence_length=(
        word_count/sentence_count
        if sentence_count>0
        else 0
    )

    vocabulary_score=(
        (unique_words/word_count)*100
        if word_count>0
        else 0
    )

    blob=TextBlob(text)

    corrected=str(blob.correct())

    grammar_errors=abs(
        len(corrected.split())-
        len(text.split())
    )

    grammar_score=max(
        0,
        100-(grammar_errors*2)
    )

    readability_score=max(
        0,
        100-abs(avg_sentence_length-15)*2
    )

    ml_score=predict_score(
        word_count,
        sentence_count,
        vocabulary_score,
        readability_score
    )

    topic_score=calculate_topic_relevance(
        topic,
        text
    )

    plagiarism_score=calculate_plagiarism(
        text,
        previous_essays
    )

    essay_type="General"

    argumentative_words=[
        "should","must","because",
        "therefore","however","argue",
        "opinion","reason","conclusion"
    ]

    narrative_words=[
        "once","story","journey",
        "experience","memory",
        "happened","felt"
    ]

    descriptive_words=[
        "beautiful","colourful",
        "bright","dark","peaceful",
        "wonderful"
    ]

    if any(
        word in clean_words
        for word in argumentative_words
    ):
        essay_type="Argumentative"

    elif any(
        word in clean_words
        for word in narrative_words
    ):
        essay_type="Narrative"

    elif any(
        word in clean_words
        for word in descriptive_words
    ):
        essay_type="Descriptive"

    final_score=(
        grammar_score*0.20+
        vocabulary_score*0.20+
        readability_score*0.15+
        ml_score*0.25+
        topic_score*0.15+
        (100-plagiarism_score)*0.05
    )

    strengths=[]
    weaknesses=[]
    feedback=[]

    if grammar_score>=80:
        strengths.append(
            "Good grammar and sentence structure"
        )
    else:
        weaknesses.append(
            "Grammar needs improvement"
        )

    if vocabulary_score>=50:
        strengths.append(
            "Strong vocabulary usage"
        )
    else:
        weaknesses.append(
            "Use more diverse vocabulary"
        )

    if readability_score>=70:
        strengths.append(
            "Essay is easy to read"
        )
    else:
        weaknesses.append(
            "Improve sentence readability"
        )

    if topic_score>=60:
        strengths.append(
            "Essay is relevant to the topic"
        )
    else:
        weaknesses.append(
            "Essay is weakly related to the topic"
        )

    if plagiarism_score>50:
        weaknesses.append(
            "High similarity detected"
        )

    if word_count<150:
        weaknesses.append(
            "Essay length is relatively short"
        )

    feedback.extend(weaknesses)

    if len(feedback)==0:
        feedback.append(
            "Excellent essay quality."
        )

    return {

        "word_count":word_count,

        "sentence_count":sentence_count,

        "paragraph_count":paragraph_count,

        "reading_time":reading_time,

        "avg_sentence_length":round(
            avg_sentence_length,
            2
        ),

        "essay_type":essay_type,

        "grammar_errors":grammar_errors,

        "grammar_score":round(
            grammar_score,
            2
        ),

        "vocabulary_score":round(
            vocabulary_score,
            2
        ),

        "readability_score":round(
            readability_score,
            2
        ),

        "ml_score":round(
            ml_score,
            2
        ),

        "topic_score":round(
            topic_score,
            2
        ),

        "plagiarism_score":round(
            plagiarism_score,
            2
        ),

        "overall_score":round(
            final_score,
            2
        ),

        "strengths":strengths,

        "weaknesses":weaknesses,

        "feedback":feedback
    }