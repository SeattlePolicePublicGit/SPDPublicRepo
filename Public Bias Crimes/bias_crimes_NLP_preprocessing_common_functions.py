import nltk

nltk.download('stopwords', quiet=True)
nltk.download('omw-1.4')    
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

import re
import string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag

# Defining pre-processing functions
def removeStopWords(data_str):
    stops = set(stopwords.words("english"))
    cleaned_str = []
        
    for word in data_str.split():
        if word not in stops:
            cleaned_str.append(word)
        
    return ' '.join(cleaned_str)

def removeFeatures(data_str):
    # compile regex
    url_re = re.compile('https?://(www.)?\w+\.\w+(/\w+)*/?')
    num_re = re.compile(r'\d+')
    mention_re = re.compile('@\w+')
    alpha_num_re = re.compile("^[a-z0-9_.]+$")
        
    # Convert to lowercase
    data_str = data_str.lower()
        
    # Remove punctuation
    data_str = data_str.translate(str.maketrans('', '', string.punctuation))
        
    # Remove hyperlinks
    data_str = url_re.sub(' ', data_str)
        
    # Remove mentions
    data_str = mention_re.sub(' ', data_str)
        
    # Remove numeric 'words'
    data_str = num_re.sub(' ', data_str)
        
    # Remove non a-z 0-9 characters and words shorter than 3 characters
    cleaned_str = []
        
    for word in data_str.split():
        if alpha_num_re.match(word) and len(word) > 2:
            cleaned_str.append(word)
                
    return ' '.join(cleaned_str)

def lemmatize(data_str):
    cleaned_str = []
    lmtzr = WordNetLemmatizer()
    tagged_words = pos_tag(data_str.split())
        
    for word in tagged_words:
        if 'v' in word[1].lower():
            lemma = lmtzr.lemmatize(word[0], pos='v')
        else:
            lemma = lmtzr.lemmatize(word[0], pos='n')
        cleaned_str.append(lemma)
        
    return ' '.join(cleaned_str)

