import re
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import spacy

nlp = spacy.load("en_core_web_sm")

def process_emails(year):
    emails = pd.read_csv("dpwillis67_emails_with_body_new.csv")
    mask = emails['year'] == year
    emails_year = emails[mask]

    emails_year['subject_processed'] = \
    emails_year['subject'].map(lambda x: re.sub('[,\.!?]', '', str(x)))

    emails_year['subject_processed'] = \
    emails_year['subject_processed'].map(lambda x: x.lower())
    emails_year['subject_processed'].fillna('', inplace=True)

    emails_year['body_processed'] = \
    emails_year['body'].map(lambda x: re.sub('[,\.!?]', '', str(x)))

    emails_year['body_processed'] = \
    emails_year['body_processed'].map(lambda x: x.lower())
    return emails_year

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def frequent_subjects(emails_year):
    corpus = emails_year['subject_processed'].tolist()
    vectorizer = CountVectorizer(min_df=2, max_df=0.5, ngram_range=(5, 6))
    count_matrix = vectorizer.fit_transform(corpus)

    # Sum the occurrences of each phrase across all documents
    phrase_frequencies = count_matrix.sum(axis=0)

    # Convert the phrase frequencies to a dictionary
    phrase_frequencies_dict = dict(zip(vectorizer.get_feature_names_out(), phrase_frequencies.A1))

    # Sort the dictionary by frequency in descending order
    sorted_phrases = sorted(phrase_frequencies_dict.items(), key=lambda x: x[1], reverse=True)

    # Extract the sorted phrases
    feature_names = [phrase for phrase, frequency in sorted_phrases]

    print(feature_names[0:25])


def unique_phrases(emails_year):
    corpus = emails_year['body_processed'].tolist()  # Assuming 'body' is the column containing the email body
    vectorizer = TfidfVectorizer(min_df=2, max_df=0.5, ngram_range=(5, 6))
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()

    # Print unique phrases
    for phrase in feature_names[0:25]:
        print(phrase)

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def body_entities(emails_year):
    emails_year["entities"] = emails_year["body_processed"].apply(extract_entities)
    emails_year.to_csv("emails_with_entities.csv", index=False)

def subject_entities(emails_year):
    emails_year["entities_subjects"] = emails_year["subject_processed"].apply(extract_entities)
    emails_year.to_csv("emails_with_entities_subjects.csv", index=False)
