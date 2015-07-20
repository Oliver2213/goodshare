import hashlib
import json
import requests


class BookshareAPI(object):

 def __init__(self, API_key=None, username=None, password=None, base_url='https://api.bookshare.org'):
  self.API_key = API_key
  self.base_url = base_url
  self.session = requests.session()
  self.username = None
  self.password = None
  if username or password:
   self.set_credentials(username, password)

 def set_credentials(self, username, password):
  self.username = username
  self.password = hashlib.md5(password).hexdigest()

 def get(self, API_method, arg=None, page=None, format=None, chunk_size=None):
  url = self.base_url + '/' + API_method
  if arg:
   url += '/%s' % arg
  if format:
   url += '/format/%s' % format
  if page is not None:
   url += '/page/%s' % page
  params = {}
  headers = {}
  params['api_key'] = self.API_key
  if self.username is not None:
   url += '/for/%s' % self.username
   headers['X-password'] = self.password
  response = self.session.get(url, params=params, headers=headers)
  response.raise_for_status()
  if not chunk_size:
   return response.content
  else:
   return response.iter_content(chunk_size)

 def API_call(self, API_method, arg=None, page=None):
  return json.loads(self.get(API_method, arg=arg, format='json', page=page))['bookshare']

 def isbn_lookup(self, isbn):
  return self.API_call('/book/isbn', isbn)

 def book_lookup(self, id):
  return self.API_call('book/id', id)

 def periodical_lookup(self, id):
  return self.API_call('periodical/id', id)

 def periodical_edition_lookup(self, id, edition):
  return self.API_call('periodical/id/%s/edition' % id, edition)

 def full_text_search(self, text, page=1):
  return self.API_call('book/searchFTS', text, page=page)

 def title_search(self, title, page=1):
  return self.API_call('book/search/title', title, page=page)

 def author_search(self, author, page=1):
  return self.API_call('book/search/author', author, page=page)

 def author_and_title_search(self, text, page=1):
  return self.API_call('book/search', text, page=page)

 def category_list(self):
  return self.API_call('reference/category', 'list')

 def category_search(self, category, page=1):
  return self.API_call('book/search/category', category, page=page)

 def grade_list(self):
  return self.API_call('reference/grade', 'list')

 def grade_search(self, grade, page=1):
  return self.API_call('book/search/grade', grade, page=page)

 def latest(self, page=1):
  return self.API_call('book/latest', page=page)

 def popular(self, page=1):
  return self.API_call('book/popular', page=page)

 def periodical_list(self, page=1):
  return self.API_call('periodical', 'list', page=page)

 def download(self, id, version=1):
  return self.get('download/content/%s/version' % id, version, chunk_size=8192)

 def user_info(self):
  return self.API_call('user/info', 'display')
