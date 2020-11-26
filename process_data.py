# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    process_data.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: seronen <seronen@student.hive.fi>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/25 13:29:56 by seronen           #+#    #+#              #
#    Updated: 2020/11/26 19:12:29 by seronen          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
import sys
import nltk
from nltk.stem import WordNetLemmatizer

# For errors, both inherit from Exception

class RegexifyError(Exception):
	pass

class TextError(Exception):
	pass

# Object to store the data / maybe in future might be helpful

class TextData():
	def __init__(self, data=None, name=None):
		self.data = data
		self.name = name
		if self.data is None or self.name is None:
			raise TextError("Invalid data for textData constructor!")
	def __repr__(self):
		print(self.name)

# Store all words in dataset to list items. "Tokenize"

def listify(string_data):
	new_lst = re.findall(r"[\w]+", string_data) # get individual words from data. Note to self: Check if this is unneccessary!!!
	lemmatizer = WordNetLemmatizer()
	for i in range(len(new_lst)):
		new_lst[i] = lemmatizer.lemmatize(new_lst[i]) # lemmatize words
	print(new_lst)
	return new_lst

# Apply regex to remove noise from data

def regexify_data(data_dict):
	if type(data_dict) is not dict:
		raise RegexifyError("Wrong data type for regexify")
	for data in data_dict:
		new_list = data_dict[data].split("#label#:")
		for i in range(len(new_list)):
			pre_parse = re.sub(r"<.*>|#.*#:|#.*#:|:\d|_|\.+|-|&quot"," ", new_list[i]) # remove all kinds of clutter in data
			remove_punct = re.sub(r"\!|\||\*|~|\^|=|\"|\?|\$|\'|\(|\)|\[|\]", "", pre_parse) # remove punctuations and other special marks
			new = re.sub(r"\s{2,12}", " ", remove_punct).lower() # remove unnecessary whitespaces and chance case to lower
			new_list[i] = new
		data_dict[data] = new_list
	return data_dict

def main():
	try:
		data_dict = {}
		with open("dataset/negative.review") as books_neg:
			books_neg_data = books_neg.read()
			data_dict["data_neg"] = books_neg_data
		with open("dataset/positive.review") as books_pos:
			books_pos_data = books_pos.read()
			data_dict["data_pos"] = books_pos_data
		list_data = regexify_data(data_dict)    # apply regex
		dataset = TextData(list_data, "dataset")
	except KeyboardInterrupt:
		print("\nAborted! Exiting...")
		sys.exit()
	return dataset

dataset = main()
#print(dataset.data["data_neg"])

