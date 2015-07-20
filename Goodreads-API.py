import collections

from rauth.service import OAuth1Service, OAuth1Session
import xmltodict

class InvalidResponse(KeyError):
	pass

class GoodreadsAPI(object):
	"A simple wrapper for the Goodreads.com Web API."""

	def __init__(self, consumer_key, consumer_secret, key=None, secret=None):
		self.service = OAuth1Service(
			consumer_key=consumer_key,
			consumer_secret=consumer_secret,
			name='goodreads',
			request_token_url='https://www.goodreads.com/oauth/request_token',
			authorize_url='https://www.goodreads.com/oauth/authorize',
			access_token_url='https://www.goodreads.com/oauth/access_token',
			base_url='https://www.goodreads.com/',
		)
		self.request_token = None
		self.request_secret = None
		self.session = None
		if key and secret:
			self.session = OAuth1Session(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=key, access_token_secret=secret)

	def is_logged_in(self):
		return self.session is not None

	def get_request_token(self):
		self.request_token, self.request_secret = self.service.get_request_token(header_auth=True)

	def get_authorize_url(self, oauth_callback=None, mobile=False):
		"""Retrieve the URL to redirect the user to so that they may authorize your app.
		The oauth_callback argument should be set to the URL which you wish Goodreads to call when the user finishes authorizing your application."""
		url = self.service.get_authorize_url(self.request_token)
		if oauth_callback is not None:
			url = '%s&oauth_callback=%s' % (url, oauth_callback)
		if mobile:
			url = '%s&mobile=1' % url
		return url

	def login_complete(self):
		self.session = self.service.get_auth_session(self.request_token, self.request_secret)

	##API methods

	def auth_user(self, **kwargs):
		"""Get a response with the Goodreads user_id for the user who authorized access using OAuth."""
		return self.API_call(self.get, 'api/auth_user', container='user', **kwargs)

	def author_books(self, **kwargs):
		"""Get a response with a paginated list of an authors books."""
		return self.API_call(self.get, 'author/list.xml', container='author', **kwargs)

	def author_show(self, **kwargs):
		"""Get a response with info about an author."""
		return self.API_call(self.get, 'author/show.xml', container='author', **kwargs)

	def isbn_to_id(self, **kwargs):
		"""Get the Goodreads book ID given an ISBN."""
		return self.API_call(self.get, 'book/isbn_to_id', raw=True, **kwargs)

	def add_review(self, **kwargs):
		"""Add book reviews for members"""
		return self.API_call(self.post, 'review.xml', container='review', **kwargs)


	def create_user_status(self, **kwargs):
		"""Add status updates for members"""
		return self.API_call(self.post, 'user_status.xml', container='user-status', **kwargs)

	def search(self, **kwargs):
		"""Get a response with the most popular books for the given query. This will search all books in the title/author/ISBN fields and show matches, sorted by popularity on Goodreads. There will be cases where a result is shown on the Goodreads site, but not through the API. This happens when the result is an Amazon-only edition and we have to honor Amazon's terms of service."""
		return self.API_call(self.get, 'search/index.xml', container='search', **kwargs)

	def get_friend_requests(self, **kwargs):
		"""Returns the current user's friend requests"""
		return self.API_call(self.get, 'friend/requests.xml', container='requests', **kwargs)

	def add_to_shelf(self, **kwargs):
		"""Add a book to a shelf"""
		return self.API_call(self.post, 'shelf/add_to_shelf.xml', **kwargs)

	def list_shelves(self, **kwargs):
		"""Lists shelves for a user"""
		return self.API_call(self.get, 'shelf/list.xml', container='shelves', **kwargs)

	def list_books(self, **kwargs):
		"""Get the books on a members shelf."""
		return self.API_call(self.get, 'review/list.xml', container='books', **kwargs)


	def API_call(self, method, path, container=None, raw=False, **kwargs):
		return self.parse_response(method(path, **self.prepare_call(**kwargs)), container=container, raw=raw)

	def get(self, path, **kwargs):
		"""Utility method for GETting from the Goodreads API"""
		url = self.service.base_url + path
		response = self.session.get(url, data=kwargs)
		response.raise_for_status()
		return response.content

	def post(self, path, **kwargs):
		"""Utility method for POSTing to the Goodreads API"""
		url = self.service.base_url + path
		response = self.session.post(url, data=kwargs)
		response.raise_for_status()
		return response.content

	def prepare_call(self, **kwargs):
		data = {}
		for key, val in kwargs.iteritems():
			if isinstance(val, collections.MutableMapping):
				for subkey, subval in val.iteritems():
					new_key = '%s[%s]' % (key, subkey)
					data[new_key] = subval
			else:
				data[key] = val
		return data

	def parse_response(self, result, container=None, raw=False):
		if not raw:
			result = xmltodict.parse(result)
			result = result.get('GoodreadsResponse', result)
		elif raw:
			result = result.split('\n')[0]
		if container is not None:
			try:
				result = result[container]
			except KeyError:
				raise InvalidResponse("The response %r did not contain an item called %r" % (result, container))
		return result
