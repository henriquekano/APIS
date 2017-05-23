# -*- coding: utf-8 -*-

import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
			response = session.put(url, json=new_params)
		return response

	def backup_page(self, file_name, pages):
		with open(file_name, 'w') as file:
			for page in pages:
				response = self.get_page(page)
				page_json = response.json()
				body = page_json.get('body')
				page_json['body'] = body
				page_json_string = json.dumps(page_json, indent=4, ensure_ascii=False)
				file.write(page)
				file.write(page_json_string)
		return true