# coding:utf-8
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

	#登录模块
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
				#使cookie生效
				requests.get(r.headers['Location'], cookies=r.cookies, allow_redirects=False, proxies=proxies, timeout=3)
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
		print(self.app.template)
		try:
			login_state = self.app.template[1]['login_state']
			if re.search(r'Cookie: (.*)',login_state) != None:
				Cookie = re.search(r'Cookie: (.*)',login_state).group(1)
			else:
				Cookie = "null"
		except:
			Cookie = "null"
		print(Cookie)
		return Cookie

	#一级审核
	@htmlPy.Slot()
	def firstExamineList(self):
		if self.getCookie() != "null":
			pass

		cnvd_bianhaos={
			123,321,111,222,333
		}
		#更新template
		template_dic = self.app.template[1]
		print(template_dic)
		template_dic['cnvd_bianhaos'] = cnvd_bianhaos
		print(template_dic)
		self.app.template = ("index.html", template_dic)


	def post_query(self, url, payload):
		cookie = self.getCookie()
		cookies = {'JSESSIONID': cookie}
		proxies = {
			#"http": "http://127.0.0.1:8081"
			}
		login_state = self.app.template[1]['login_state']
		if cookie != "null":
			try:
				r = requests.post(url, allow_redirects=False, cookies=cookies, data=payload, proxies=proxies, timeout=3)
				#print(r.text)
				#print(r.status_code)
				if r.status_code == 302 and r.headers['Location'] == 'http://202.108.212.74:8000/cnvd_admin/login/loginFail':
					#print('login failed')
					login_state = 'login failed'
				if r.status_code == 200 :
					print(r.text)
			except BaseException, e:
				login_state = e.__class__.__name__
				print('except:',e)
				print(login_state)
			finally:
				return r.text
		elif cookie == "null":
			# 更新template
			template_dic = self.app.template[1]
			template_dic['login_state'] = u'请先登录'
			self.app.template = ("index.html", template_dic)



	#二级审核
	@htmlPy.Slot()
	def secondExamineList(self):
		payload = {
			'number':'',
			'title':'',
			'storageTimeStartStr':'',
			'storageTimeEndStr':'',
			'serverityId':'',
			'causeId':'',
			'threadId':'',
			'positionId':'',
			'softStyleId':'',
			'isv':'',
			'ivp':'',
		}
		cookie = self.getCookie()
		cookies = {'JSESSIONID':cookie}
		proxies = {"http":"http://127.0.0.1:8081"}
		login_state = self.app.template[1]['login_state']
		if cookie != "null":
			try:
				r = requests.post("http://202.108.212.74:8000/cnvd_admin/flaw/secondExamineList", allow_redirects=False, cookies=cookies, data=payload, proxies=proxies, timeout=3)
				print(r.text)
				print(r.status_code)
				if r.status_code == 302 and r.headers['Location'] == 'http://202.108.212.74:8000/cnvd_admin/login/loginFail':
					print('login failed')
					login_state = 'login failed'
				if r.status_code == 200 :
					print(r.text)
			except BaseException, e:
				login_state = e.__class__.__name__
				print('except:',e)
				print(login_state)
			finally:
				#更新template
				template_dic = self.app.template[1]
				#template_dic['cnvd_bianhaos'] = cnvd_bianhaos
				template_dic['login_state'] = login_state
				self.app.template = ("index.html", template_dic)
				#刷新js
				self.app.evaluate_javascript("$('div.content1').hide();$('div#erjishenhe').show();")
		elif cookie == "null":
			# 更新template
			template_dic = self.app.template[1]
			template_dic['login_state'] = u'请先登录'
			self.app.template = ("index.html", template_dic)

