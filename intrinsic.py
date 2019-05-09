import copy
import sys
import json
import csv
import itertools
import networkx as nx
import pandas as pd
from matplotlib import pyplot
from pprint import pprint
from random import randint
from textstat.textstat import textstat
import nltk
from nltk import ngrams
import pandas as pd

dataques = pd.read_csv("Questions.csv")
dateans = pd.read_csv("Answers.csv")
print("blah")

file1 = open('ques.csv', 'w')
writer1 = csv.writer(file1)

file2 = open('ans.csv','w')
writer2 = csv.writer(file2)
print("blah1")

line=["question_id","question_automated_readability_index","question_avg_letter_per_word","question_avg_sentence_length","question_avg_sentence_per_word","question_avg_syllables_per_word","question_char_count","question_coleman_liau_index","question_dale_chall_readability_score","question_difficult_words","question_flesch_kincaid_grade","question_flesch_reading_ease","question_gunning_fog","question_lexicon_count","question_linsear_write_formula","question_lix","question_polysyllabcount","question_sentence_count","question_smog_index","question_syllable_count","question_text_standard","Answer count","Comment Count"]
writer1.writerow(line)
line=["answer_id","answer_automated_readability_index","answer_avg_letter_per_word","answer_avg_sentence_length","answer_avg_sentence_per_word","answer_avg_syllables_per_word","answer_char_count","answer_coleman_liau_index","answer_dale_chall_readability_score","answer_difficult_words","answer_flesch_kincaid_grade","answer_flesch_reading_ease","answer_gunning_fog","answer_lexicon_count","answer_linsear_write_formula","answer_lix","answer_polysyllabcount","answer_sentence_count","answer_smog_index","answer_syllable_count","answer_text_standard","Comment Count"]
writer2.writerow(line)


for x in range(len(dataques)):
	question = dataques.iloc[x]

	body_text = question["body_text"]

	anscount = question["AnswerCount"]
	commcount = question["CommentCount"]

	# print(body_text)

	#,"body_text"]#[x]["body_text"]
	question_id = question["id"]
	#usage items
	question_score=question["Score"]
	#question_anscomments=["Answercount"]

	#question_views=

	question_char_count = textstat.char_count(body_text)
	question_avg_letter_per_word = textstat.avg_letter_per_word(body_text)
	question_avg_sentence_length = textstat.avg_sentence_length(body_text)
	question_sentence_count = textstat.sentence_count(body_text)
	question_avg_syllables_per_word = textstat.avg_syllables_per_word(body_text)
	question_avg_sentence_per_word = textstat.avg_sentence_per_word(body_text)
	question_syllable_count = textstat.syllable_count(body_text)
	question_coleman_liau_index = textstat.coleman_liau_index(body_text)
	question_text_standard = textstat.text_standard(body_text,float_output=True)
	question_difficult_words = textstat.difficult_words(body_text)
	question_lexicon_count = textstat.lexicon_count(body_text)
	question_flesch_reading_ease = textstat.flesch_reading_ease(body_text)
	question_automated_readability_index = textstat.automated_readability_index(body_text)
	question_dale_chall_readability_score = textstat.dale_chall_readability_score(body_text)
	question_flesch_kincaid_grade = textstat.flesch_kincaid_grade(body_text)
	question_gunning_fog = textstat.gunning_fog(body_text)
	question_smog_index = textstat.smog_index(body_text)
	question_linsear_write_formula = textstat.linsear_write_formula(body_text)
	question_polysyllabcount = textstat.polysyllabcount(body_text)
	question_lix = textstat.lix(body_text)
	question_ngrams = ngrams(body_text.split(), 5)

	y = [question_id,question_automated_readability_index, question_avg_letter_per_word, question_avg_sentence_length, question_avg_sentence_per_word, question_avg_syllables_per_word, question_char_count, question_coleman_liau_index, question_dale_chall_readability_score, question_difficult_words, question_flesch_kincaid_grade, question_flesch_reading_ease, question_gunning_fog, question_lexicon_count, question_linsear_write_formula, question_lix, question_polysyllabcount, question_sentence_count,  question_smog_index, question_syllable_count, question_text_standard,anscount,commcount]
	writer1.writerow(y)
print("blah2")

for x in range(len(dateans)):

	answer = dateans.iloc[x]
	body_text = answer["body_text"]
	answer_id = answer["id"]
	#usage items
	answer_score=answer["Score"]
	# answer_Cnts=answer["AnswerCount"]

	#answer_views=

	answer_char_count = textstat.char_count(body_text)
	answer_avg_letter_per_word = textstat.avg_letter_per_word(body_text)
	answer_avg_sentence_length = textstat.avg_sentence_length(body_text)
	answer_sentence_count = textstat.sentence_count(body_text)
	answer_avg_syllables_per_word = textstat.avg_syllables_per_word(body_text)
	answer_avg_sentence_per_word = textstat.avg_sentence_per_word(body_text)
	answer_syllable_count = textstat.syllable_count(body_text)
	answer_coleman_liau_index = textstat.coleman_liau_index(body_text)
	answer_text_standard = textstat.text_standard(body_text,float_output=True)
	answer_difficult_words = textstat.difficult_words(body_text)
	answer_lexicon_count = textstat.lexicon_count(body_text)
	answer_flesch_reading_ease = textstat.flesch_reading_ease(body_text)
	answer_automated_readability_index = textstat.automated_readability_index(body_text)
	answer_dale_chall_readability_score = textstat.dale_chall_readability_score(body_text)
	answer_flesch_kincaid_grade = textstat.flesch_kincaid_grade(body_text)
	answer_gunning_fog = textstat.gunning_fog(body_text)
	answer_smog_index = textstat.smog_index(body_text)
	answer_linsear_write_formula = textstat.linsear_write_formula(body_text)
	answer_polysyllabcount = textstat.polysyllabcount(body_text)
	answer_lix = textstat.lix(body_text)
	answer_ngrams = ngrams(body_text.split(), 5)

	y = [answer_id,answer_automated_readability_index, answer_avg_letter_per_word, answer_avg_sentence_length, answer_avg_sentence_per_word, answer_avg_syllables_per_word, answer_char_count, answer_coleman_liau_index, answer_dale_chall_readability_score, answer_difficult_words, answer_flesch_kincaid_grade, answer_flesch_reading_ease, answer_gunning_fog, answer_lexicon_count, answer_linsear_write_formula, answer_lix, answer_polysyllabcount, answer_sentence_count,  answer_smog_index, answer_syllable_count, answer_text_standard]
	writer2.writerow(y)

print("blah4")
file1.close()
file2.close()
