import phrases
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

vectorizer = CountVectorizer()
keys = vectorizer.fit_transform(list(phrases.data_set.keys()))
values = vectorizer.fit_transform(list(phrases.data_set.values()))

print(keys)
print()
print(values)
print()
print(vectorizer.get_feature_names())
