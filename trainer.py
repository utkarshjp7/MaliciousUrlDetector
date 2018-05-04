'''
Utkarsh Patel & Mayank Jain
CIS 475 Final Project
'''

import pandas
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import numpy
from sklearn import svm
from sklearn import cross_validation as cv
import matplotlib.pylab as plt
import warnings

def return_nonstring_col(data_cols):
	cols_to_keep=[]
	train_cols=[]
	for col in data_cols:
		if col!='URL' and col!='host' and col!='path':
			cols_to_keep.append(col)
			if col!='malicious' and col!='result':
				train_cols.append(col)
	return [cols_to_keep,train_cols]

def svm_classifier(train, query, train_cols, is_gui):
	clf = svm.SVC()

	train[train_cols] = preprocessing.scale(train[train_cols])
	query[train_cols] = preprocessing.scale(query[train_cols])
	
	print clf.fit(train[train_cols], train['malicious'])
	if not is_gui:
		scores = cv.cross_val_score(clf, train[train_cols], train['malicious'], cv=30)
		print('Estimated score SVM: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))

	query['result'] = clf.predict(query[train_cols])
	print query[['URL','result']]
	return query['result']

def train(db, test_db):
	query_csv = pandas.read_csv(test_db)
	cols_to_keep,train_cols=return_nonstring_col(query_csv.columns)
	#query=query_csv[cols_to_keep]

	train_csv = pandas.read_csv(db)
	cols_to_keep,train_cols=return_nonstring_col(train_csv.columns)
	train=train_csv[cols_to_keep]

	svm_classifier(train_csv, query_csv, train_cols, False)

	forest_classifier(train_csv,query_csv,train_cols)

def gui_caller(db, test_db):
	
	query_csv = pandas.read_csv(test_db)
	cols_to_keep,train_cols=return_nonstring_col(query_csv.columns)
	#query=query_csv[cols_to_keep]

	train_csv = pandas.read_csv(db)
	cols_to_keep,train_cols=return_nonstring_col(train_csv.columns)
	train=train_csv[cols_to_keep]

	return svm_classifier(train_csv, query_csv, train_cols, True)	

