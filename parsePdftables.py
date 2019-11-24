import pandas as pd 
import numpy as np 
import PyPDF2 as pypdf 
import re
import sys



def cleanPage(page):
	text = page.split('\n ')
	text = map(lambda ch: ch.replace("\n", ""), text)
	text = filter(lambda ch: ch.strip() != '', text)
	return text

def parsePage(data , textIter , headers_len ):

	text = (list(textIter))
	text_len = len(text)
	header_len = len(headers)
	begList = []
	for i in range(text_len):
		if(re.match(r"^(\w+/\w+/\w+/\w+/\w+)", text[i])):
			begList.append(i)
	for i in range(len(begList)):
		row = text[begList[i]:begList[i]+header_len]
		if( len(row) > 8 and not re.match(r"^\d+-\d+-\d+",row[7])): # The value seven is very specific to how data is formatted
			row.insert(7, "")
			if(len(row) > header_len):
				row = row[:-1]
		data.append(row)
		end = begList[i+1] if ((i+1) < len(begList)) else text_len
		data[i][header_len-1] += " ".join(text[begList[i]+header_len+1:end])

	return data




def readPDF(filename ,headers):
	pdfFileObj = open(filename, 'rb')
	pdfReader = pypdf.PdfFileReader(pdfFileObj)
	print("log: Found {} pages".format(pdfReader.numPages))


	pagesText = map(lambda i: pdfReader.getPage(i).extractText() ,range(0, pdfReader.numPages))


	pagesText = filter(lambda pageText: (	"disease alerts/outbreaks reported" not in pageText and 
											"WEEKLY OUTBREAK REPORT" not in pageText
											) , pagesText)


	# print("log: Found relevant {} pages with data to scrap".format(len(list(pagesText))))

	data = []
	for page in pagesText:
		data = parsePage(data , cleanPage(page), len(headers))

	print("log: Found {} rows of data from gived pdf".format(len(data)))
	return 	data





if __name__ == '__main__':
	if(len(sys.argv) < 3):
		print(" Give file name: Usage example => parsePdftables.py ***.pdf ")
	
	filename = sys.argv[1]
	outputfile = sys.argv[2]

	headers = ['Unique ID.', 'Name of State/UT', 'Name of District', 'Disease/ Illness', 'No. of Cases', 
	'No. of Deaths', 'Date of Start Outbreak' ,'Date of Reporting' ,'Current Status', 'Comments/ Action Taken',]

	pdfdata = readPDF(filename, headers)
	pd.set_option('display.max_columns', None)
	# To be considered that the pdf is exteremely disorganised
	# text is still messed up courtsey of being the last column
	# also there are two type of data one for late reported and and one for already reported
	# the "Date of Reporting" field is empty for the 1st kind so for that column the data will be nill
	# This will help in seggragating the data
	data = pd.DataFrame(pdfdata, columns=headers)
	data.to_csv(outputfile)
