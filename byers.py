# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    byers.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: seronen <seronen@student.hive.fi>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/25 12:43:17 by seronen           #+#    #+#              #
#    Updated: 2020/11/25 23:31:04 by seronen          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from process_data import dataset

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
import sys
import re

class ByersError(Exception):
	pass

def split_train_test(data_pos=None, data_neg=None):
	if data_pos is None or data_neg is None:
		raise ByersError("No data to split!")
	pos_size = len(data_pos)
	neg_size = len(data_neg)
	neg_train_size = int(neg_size * 0.8)
	pos_train_size = int(pos_size * 0.8)
	train_pos = data_pos[:pos_train_size]
	train_neg = data_neg[:neg_train_size]
	test_pos = data_pos[pos_train_size:]
	test_neg = data_neg[neg_train_size:]
	return train_pos, train_neg, test_pos, test_neg

def handle_args():
	if len(sys.argv) < 2:
		raise ByersError("No reviews to classify! Try --help for more info!")
	if "help" in str(sys.argv):
		print("""usage: python3 byers.py (f.ex. "I hate this negative review" "can i get a positive result")
				--proba (Print probabilities [ [negative_proba] [positive_proba] ])
				--benchmark (prints the score for the classifier [1 best, 0 worst])
		""")
		sys.exit()

def init_byers():
	return CountVectorizer(), MultinomialNB()		# init classifier and vectorizer


def predict(counter, classifier, training_counts, training_labels, review):
	lemmatizer = WordNetLemmatizer()
	review_lem = lemmatizer.lemmatize(review)
	review_counts = counter.transform([review_lem])

	if "--proba" in sys.argv:
		prediction = classifier.predict_proba(review_counts)
	else:
		prediction = classifier.predict(review_counts)
	return prediction

def save_data(result, prediction):
	pass

def handle_result(prediction, text):
	print(text)
	if "--proba" in str(sys.argv):		# Display probabilities on stdout
		print(prediction)
		return 0
	if prediction is None:
		print("No prediction!")
		sys.exit()
	if prediction == 1:
		print("The text was classified as positive!")
	else:
		print("The text was classified as negative!")
	save_data(prediction, text)

def main(dataset):
	handle_args()

	text_data_neg = dataset.data["books_pos"]
	text_data_pos = dataset.data["books_neg"]

	train_pos, train_neg, test_pos, test_neg = split_train_test(text_data_pos, text_data_neg)
	
	counter, classifier = init_byers()
	counter.fit(train_neg + train_pos)
	training_counts = counter.transform(train_neg + train_pos)
	training_labels = [0] * len(train_neg) + [1] * len(train_pos)
	classifier.fit(training_counts, training_labels)
	if "--benchmark" in str(sys.argv):
		test_labels = [0] * len(test_neg) + [1] * len(test_pos)
		test_counts = counter.transform(test_neg + test_pos)			# Score the "AI" where 0 is the worst and 1 is the best.
		print(classifier.score(test_counts, test_labels))
		sys.exit()
	for review in sys.argv[1:]:
		if "--" in review:
			continue
		prediction = predict(counter, classifier, training_counts, training_labels, review)
		handle_result(prediction, review)

main(dataset)





