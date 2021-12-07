import pandas as pd
data = pd.read_csv('/Users/mineq/us-aufgaben/PersonalityTypes/mbti_1.csv')
data.columns =["target_variable", "posts"]

#extract features from text
#https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html

# import nltk.stem
# import re
# from nltk.stem.porter import PorterStemmer


# Versuch 1 - SnowballStemmer auf StemmedCountVectorizer:
#
# engl_stemmer = nltk.stem.SnowballStemmer('english')
# class StemmedCountVectorizer(CountVectorizer):
#     def build_analyzer(self):
#         analyzer = super(StemmedCountVectorizer, self).build_analyzer()
#         return lambda doc: ([engl_stemmer.stem(w) for w in analyzer(doc)])
# count_vect = StemmedCountVectorizer(min_df=250, token_pattern = r'(?u)\b[A-Za-z]+\b', stop_words="english")


# Versuch 2 - PorterStemmer auf CountVectorizer:
#
# def stemming_tokenizer(str_input):
#     porter_stemmer = PorterStemmer()
#     words = re.sub(r"[^A-Za-z0-9\-]", " ", str_input).lower().split()
#     words = [porter_stemmer.stem(word) for word in words]
#     return words
# count_vect = CountVectorizer(min_df = 250, tokenizer=stemming_tokenizer)


# Versuch 3 - TfidfVectorizer
#
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vect = TfidfVectorizer(min_df = 250, token_pattern = r'(?u)\b[A-Za-z]+\b', stop_words="english")
X = tfidf_vect.fit_transform(data['posts']) #document_term_matrix or bag_of_words
dtm = pd.DataFrame(X.toarray()) # transform x to array
dtm.columns = tfidf_vect.get_feature_names() # stores column names
data_dtm = pd.concat([data, dtm], axis=1)


# Versuch 4 - klassischer CountVectorizer:
#
# from sklearn.feature_extraction.text import CountVectorizer
# count_vect = CountVectorizer(min_df = 250, token_pattern = r'(?u)\b[A-Za-z]+\b', stop_words="english")
# X = count_vect.fit_transform(data['posts']) #document_term_matrix or bag_of_words
# dtm = pd.DataFrame(X.toarray()) # transform x to array
# dtm.columns = count_vect.get_feature_names() # stores column names
# data_dtm = pd.concat([data, dtm], axis=1)


#generate training and test data
import random
sample = random.sample(range(len(data_dtm.index)), k=int(len(data_dtm.index)*0.8))
training = data_dtm.iloc[sample]
test = data_dtm.drop(sample)

#apply classifier
#http://scikit-learn.org/stable/tutorial/machine_learning_map/
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier()
forest.fit(training.iloc[:,2:], training["target_variable"]) #X = data[:, 2:] - select columns 2 through end (the text); y = data[:, 0] - select column 0 (the target_variable)
print(forest.score(test.iloc[:,2:],test["target_variable"]))


#explore predictions
# pred_class = forest.predict(test.iloc[:,2:])
# test_copy = test.copy()
# test_copy['pred_class'] = pred_class
# probabilities = forest.predict_proba(test.iloc[:,2:])
# test_copy['probabilities'] = probabilities[:,1]

#consider problem of inbalanced datasets, e.g. spam filter
# from sklearn.metrics import confusion_matrix
# cfm = confusion_matrix(test['target_variable'], pred_class, labels=['INFJ','ISTP']) # *

#explore feature weights
# importance_df = pd.DataFrame(forest.feature_importances_)
# importance_df['feature'] = test.columns[2:]