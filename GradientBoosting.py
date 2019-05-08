from sklearn import ensemble
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

import scikitplot as skplt
import matplotlib.pyplot as plt

# Implementing naive bayes with sklearn
#from sklearn.naive_bayes import GaussianNB
#from sklearn.feature_extraction.text import TfidfVectorizer
#import string
#import os
#from scipy.sparse.csr import csr_matrix #need this if you want to save tfidf_matrix
#import scipy.stats
#from sklearn.feature_extraction.text import TfidfVectorizer
#from nltk.stem.porter import PorterStemmer
#from sklearn.feature_selection import SelectKBest, mutual_info_classif
#import nltk
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, roc_auc_score
from sklearn.metrics import average_precision_score
#from sklearn import metrics

X = pd.read_csv("final_ans.csv")
Y = pd.read_csv("y_ans.csv")
# print(X)
X=X.drop(["answer_id","Comment Count"],axis = 1)#,"question_automated_readability_index","question_avg_letter_per_word","question_avg_sentence_length","question_avg_sentence_per_word","question_avg_syllables_per_word","question_char_count","question_coleman_liau_index","question_dale_chall_readability_score","question_difficult_words","question_flesch_kincaid_grade","question_flesch_reading_ease","question_gunning_fog","question_lexicon_count","question_linsear_write_formula","question_lix","question_polysyllabcount","question_sentence_count","question_smog_index","question_syllable_count","question_text_standard"],axis = 1)

Y = np.array(Y["Score"])
cnt = 0
for x in range(len(Y)):
    if Y[x]>=4:
        Y[x] = 1
        cnt+=1
    else:
        Y[x] = 0


newX = pd.DataFrame([])

newY = pd.DataFrame([])

for x in range(len(Y)):
    if Y[x] ==1:
        newX = newX.append(X.loc[x],ignore_index=True)
        newY = newY.append([1],ignore_index =True)
    else:
        if cnt>=1:
            cnt-=1;
            newX = newX.append(X.loc[x],ignore_index=True)
            newY = newY.append([0],ignore_index=True)

newY = np.array(newY[0])
# print(newY)
newX = preprocessing.normalize(newX)
print(len(newX),len(newY))

# nan_rows = X[X.isnull().T.any().T]


xTrain, xTest, yTrain, yTest = train_test_split(newX, newY, test_size = 0.2,shuffle=True)

clf = ensemble.GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=100, subsample=1.0,
	criterion='friedman_mse', min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=7,
	min_impurity_decrease=0.0, min_impurity_split=None, init=None, random_state=None, max_features=None, verbose=0,
	max_leaf_nodes=None, warm_start=False, presort='auto')

cclf = clf.fit(xTrain, yTrain)
predicted = clf.predict(xTest)


proba = clf.predict_proba(xTest)

skplt.metrics.plot_roc_curve(yTest,proba)
plt.show()

print(clf.feature_importances_)

t = clf.feature_importances_
u = X.columns
for i in range(len(t)):
    print(u[i],t[i],sep = "-------------------->")

accuracy = accuracy_score(yTest,predicted)

from sklearn.metrics import average_precision_score
average_precision = average_precision_score(yTest, predicted)




from sklearn.metrics import classification_report

#print('Average precision-recall score: {0:0.5f}'.format(average_precision))
# target_names =[""]
print(classification_report(yTest,predicted))#, target_names=target_names))
from sklearn.metrics import precision_recall_fscore_support








from sklearn.metrics import roc_auc_score

print(roc_auc_score(yTest,predicted))















#print(precision_recall_fscore_support(yTest, predicted, average=None))
print("Average Precision Score",average_precision_score(yTest,predicted),sep = " : ")

# Calculating accuracy, confusion matrix,roc area and f1 score
print ('Accuracy:', accuracy*100,sep= " ") # Accuracy = 93.0769230769
# Spam is True Positive & Non Spam is True Negative
# [[TN FP] [FN TP]]
#print('Confussion matrix: [[True Non Spam | False Spam] [False Non Spam | True Spam]]\n',confusion_matrix(yTest,predicted)) # Confusion Matrix = [[122   8],[ 10 120]]
#print ('F1 score:', f1_score(yTest,predicted)) # F1 score = 0.93023255814
#print ('ROC score:',roc_auc_score(yTest,predicted)) # ROC score = 0.930769230769
