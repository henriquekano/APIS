import requests

class ReadmeClient:

	def __init__(self, readme_creds, project_name, version):
		self.readme_creds = readme_creds
		self.cookies = readme_creds.get('cookie')
		self.base_url = 'https://dash.readme.io/api/projects/{0}/{1}'.format(project_name, version)

	def _get_url(self, path):
		return self.base_url + str(path)

	def _get_session(self, session):
		response = session.post("https://dash.readme.io/users/session", 
		data={
			'email': self.readme_creds.get('email'),
			'password': self.readme_creds.get('password')
		},
		headers={
			'Cookie': self.cookies
		})
		return session

	def get_data(self):
		with requests.Session() as session:
			self._get_session(session)
			url = self._get_url('/data')
			response = session.get(url)
		return response

	# Page must be in ref/{page} or docs/{page} format
	def get_page(self, page):
		with requests.Session() as session:
			self._get_session(session)
			url = self._get_url(page)
			response = session.get(url)
		return response

	def put_page(self, page, new_params):
		with requests.Session() as session:
			self._get_session(session)
			url = self._get_url(page)
			response.put(url, json=new_params)
		return response