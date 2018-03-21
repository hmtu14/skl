from sklearn.feature_extraction.text import CountVectorizer


sents = []
sents.append("Today I want to sleep at home. But I can't do it.")
sents.append("He was a good boy")
vectorizer = CountVectorizer()
vectorizer.fit_transform(sents)
analyze = vectorizer.build_analyzer()