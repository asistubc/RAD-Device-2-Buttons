# Goodreads to RAD Booklist Generator 
# For use with ASIS&T@UBC's 2-button Readers Advisory Device (RAD)
# See https://github.com/asistubc/RAD-Device-2-Buttons.
#
# Based on an existing Goodreads shelf, generates a booklist CSV compatible with the RAD (max 200 entries).
# Includes title, author, and desciption.
# After running, add the new booklist's filepath to the appropriate field in RADPrinter?.py.
#
# Created: Sept 19 2016
# Edited: Sept 21 2016
# Author: Rebecca Dickson (http://github.com/rebeckson)
########################################################################################################

import requests
import lxml
from lxml import etree
import lxml.html
import unicodecsv

# ADD YOUR INFO TO THE FIELDS BELOW!
# Get your key and secret at https://www.goodreads.com/api/keys.
# User's 8-digit Goodreads ID is displayed in the address bar when you visit their profile or shelves (e.g. "56241443")
# Shelf name should be entered exactly as displayed (e.g. "science-fiction")
# file_location is the path where the new CSV will be stored.
# Max description length can be set to whatever you want. Default 500 chars. Longer descriptions are truncated with an ellipsis.
key = "YOUR_KEY_HERE"
secret = "YOUR_SECRET_HERE"
goodreads_id = "GOODREADS_ID_HERE"
shelf = "SHELF_NAME_HERE"
file_location = "YOUR_FILE_LOCATION_HERE.csv"
max_descrip_length = 500 #default


def get_shelf(api_key, user_id, shelf):
	"Calls the Goodreads API, and returns XML metadata for all books on the user's indicated shelf (maximum 200 titles)."
	request_url = "http://www.goodreads.com/review/list"
	parameters = {'key':api_key, 'v':'2', 'id':user_id, 'shelf' : shelf, 'per_page': '200'}
	r = requests.get(request_url, params = parameters)
	print("Response returned from" + r.url)
	return r

def get_book_data(response):
	"Takes an XML response from a call to the Goodreads API, and returns a List formatted for the RAD (title, author, and description for each book)."
	root = etree.fromstring(resp.content)
	all_books = []
	for book in root.iterfind(".//book"):
		title = book.find("title").text.encode('utf8')
		authors = []
		for auth in book.find("authors"):
			authors.append(auth.find("name").text.encode('utf8'))
		auth_string = ",".join(authors)
		description_full = (lxml.html.document_fromstring(book.find("description").text.encode('utf8'))).text_content()
		description = (description_full[:max_descrip_length] + '...') if len(description_full) > (max_descrip_length + 3) else description_full
		book_info = [title, auth_string, description]
		all_books.append(book_info)
	return all_books

# call Goodreads
resp = get_shelf(key, goodreads_id, shelf)
# format title, author, and description
book_data = get_book_data(resp)
# write to CSV (formatted for use with RADDevice.py)
with open(file_location, 'wb') as file:
	writer = unicodecsv.writer(file, delimiter='|')
	writer.writerows(book_data)
file.close()