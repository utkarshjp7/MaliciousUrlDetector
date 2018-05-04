'''
Utkarsh Patel & Mayank Jain
CIS 475 Final Project
'''

from Tkinter import *
import tkMessageBox
import trainer as tr
import pandas
import main
import feature_extractor
import os

root = Tk()
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

L1 = Label(frame, text="Enter the URL: ")
L1.pack( side = LEFT)
E1 = Entry(frame,bd =5, width=150)
E1.pack(side = RIGHT)

def submitCallBack():
	url = E1.get()
	urlFeature = feature_extractor.extract(url)
	test_file_name = 'gui_test_feature.csv'
	os.remove(test_file_name)
	main.write_feature(urlFeature, test_file_name, True)
	return_ans = tr.gui_caller('url_features.csv', test_file_name)
	a = str(return_ans).split()

	if int(a[1]) == 0:
		tkMessageBox.showinfo("CIS475", "The specified URL \'" + url + "\' is Benign")
	else:
		tkMessageBox.showinfo("CIS475", "The specified URL \'" + url + "\' is Malicious")
   		   
B1 = Button(bottomframe, text ="Submit", command = submitCallBack)

B1.pack()

root.mainloop()