import htmlPy
import requests
import json
import re

class BackEnd(htmlPy.Object):
	def __init__(self, app):
		super(BackEnd, self).__init__()
		self.app = app

	@htmlPy.Slot()
	def say_hello_world(self):
		self.app.html = u"Hello, world"

	@htmlPy.Slot(str, result=str)
	def login(self, json_str):
		print(json_str)
		print(type(json_str))
		json_tab = json.loads(json_str)
		userName = json_tab['userName']
		passWord = json_tab['passWord']
		payload = {
			'userName':userName,
			'passWord':passWord,
			'image.x':"32",
			'image.y':"17"
		}
		proxies = {
			#"http":"http://127.0.0.1:8081"
		}
		try:
			r = requests.post("http://202.108.212.74:8000/cnvd_admin/login/loginCheck",allow_redirects=False,data=payload,proxies=proxies,timeout=3)
			print(r.text)
			print(r.status_code)
			print(r.headers['Location'])
			if r.status_code == 302 and r.headers['Location'] == 'http://202.108.212.74:8000/cnvd_admin/login/loginFail':
				print('login failed')
				login_state = 'login failed'
			if r.status_code == 302 and r.headers['Location'] == 'http://202.108.212.74:8000/cnvd_admin/login/loginSuccess':
				print('login success')
				print(r.cookies['JSESSIONID'])
				login_state = 'Cookie: '+r.cookies['JSESSIONID']
				return r.cookies
		except BaseException, e:
			login_state = e.__class__.__name__
			print(type(login_state))
			print(login_state)
		finally:
			#self.app.template.render(login_state="test")
			self.app.template = ("index.html", {"login_state": login_state,"userName":userName,"passWord":passWord})

	@htmlPy.Slot()
	def getCookie(self):
		#print(self.app.html)
		Cookie = "null"
		print(self.app.template)
		login_state = self.app.template[1]['login_state']
		if re.search(r'Cookie: (.*)',login_state) != None:
			Cookie = re.search(r'Cookie: (.*)',login_state).group(1)
		print(Cookie)
		return Cookie

	@htmlPy.Slot()
	def firstExamineList(self):
		if self.getCookie() != "null":
			try:
				r = requests.post("http://202.108.212.74:8000/cnvd_admin/login/loginCheck", allow_redirects=False,
								  data=payload, proxies=proxies, timeout=3)
				print(r.text)
				print(r.status_code)
				print(r.headers['Location'])
				if r.status_code == 302 and r.headers[
					'Location'] == 'http://202.108.212.74:8000/cnvd_admin/login/loginFail':
					print('login failed')
					login_state = 'login failed'
				if r.status_code == 302 and r.headers[
					'Location'] == 'http://202.108.212.74:8000/cnvd_admin/login/loginSuccess':
					print('login success')
					print(r.cookies['JSESSIONID'])
					login_state = 'Cookie: ' + r.cookies['JSESSIONID']
					return r.cookies
			except BaseException, e:
				login_state = e
			finally:
				# self.app.template.render(login_state="test")
				self.app.template = (
				"index.html", {"login_state": login_state, "userName": userName, "passWord": passWord})

		cnvd_bianhaos={
			123,321,111,222,333
		}
		template_dic = self.app.template[1]
		print(template_dic)
		template_dic['cnvd_bianhaos'] = cnvd_bianhaos
		print(template_dic)
		self.app.template = ("index.html", template_dic)

		#http://202.108.212.74:8000/cnvd_admin/flaw/firstExamineList

