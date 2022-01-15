import pandas as pd
import nltk.stem
from sklearn.feature_extraction.text import CountVectorizer


data = pd.read_csv('/Users/mineq/us-aufgaben/PersonalityTypes/mbti_1.csv')
data.columns =["target_variable", "posts"]


# Versuch 1 - StemmedCountVectorizer:
engl_stemmer = nltk.stem.SnowballStemmer('english')
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([engl_stemmer.stem(w) for w in analyzer(doc)])
count_vect = StemmedCountVectorizer(min_df=50, token_pattern = r'(?u)\b[A-Za-z]+\b', stop_words="english", ngram_range=(1,2))


X = count_vect.fit_transform(data['posts']) #document_term_matrix or bag_of_words
dtm = pd.DataFrame(X.toarray()) # transform x to array
dtm.columns = count_vect.get_feature_names() # stores column names
data_dtm = pd.concat([data, dtm], axis=1)


#generate training and test data
import random
sample = random.sample(range(len(data_dtm.index)), k=int(len(data_dtm.index)*0.8))
training = data_dtm.iloc[sample]
test = data_dtm.drop(sample)

#apply classifier
#http://scikit-learn.org/stable/tutorial/machine_learning_map/
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier()
X_train = training.iloc[:,2:] # select columns 2 through end
X_test = test.iloc[:,2:]
model = forest.fit(X_train, training["target_variable"])
prediction_score = forest.score(X_test, test["target_variable"])
#print(prediction_score)
