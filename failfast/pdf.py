import PyPDF2

# creating a pdf file object
pdfFileObj = open('faradayiii.pdf', 'rb')
    
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
# printing number of pages in pdf file 
num_pages = pdfReader.numPages

# creating a page object
for page in range(0,num_pages):
	pageObj = pdfReader.getPage(page)

	_fragment = ""
	_fulltext = ""
	for _line in pageObj.extractText().split('\n'):
		_fragment = _fragment + _line
		if len(_fragment) > 190:
			for index, word in enumerate(_fragment.split(' ')):
				_fulltext = _fulltext + word + " "

				if len(_fulltext) > 190 and ("." in word or "?" in word or "!" in word or ";" in word):
					print("++++++++++++++++++++++++++")
					print(_fulltext)
					print("==========================")
					_fulltext = ""
					for index2, word2 in enumerate(_fragment.split(' ')):
						if index2 < index:
							continue
						else:
							_fulltext = _fulltext + word2 + " "
			_fragment = ""

# closing the pdf file object 
pdfFileObj.close() 
