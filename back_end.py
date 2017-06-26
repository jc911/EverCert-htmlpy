# coding:utf-8
import htmlPy
import requests
import json
import re
from lxml import etree

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
		#print(self.app.template)
		try:
			login_state = self.app.template[1]['login_state']
			if re.search(r'Cookie: (.*)',login_state) != None:
				Cookie = re.search(r'Cookie: (.*)',login_state).group(1)
			else:
				Cookie = "null"
		except:
			Cookie = "null"
		#print(Cookie)
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

	#post请求函数
	def postQuery(self, url, payload):
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
					# 刷新js
					self.app.evaluate_javascript("alert('"+u'session失效，请重新登录'+"');")
				if r.status_code == 200 :
					#print(r.text)
					return r.text
			except BaseException, e:
				login_state = e.__class__.__name__
				print('except:',e)
				print(login_state)
				#刷新js
				self.app.evaluate_javascript("alert('"+login_state+"');")
				return
			finally:
				pass
		elif cookie == "null":
			# 更新template
			template_dic = self.app.template[1]
			template_dic['login_state'] = u'请先登录'
			self.app.template = ("index.html", template_dic)
			# 刷新js
			self.app.evaluate_javascript("alert('"+u'请先登录'+"');")
			return



	#二级审核检索
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
		response = self.postQuery("http://202.108.212.74:8000/cnvd_admin/flaw/secondExamineList", payload)
		# print(response)
		if response != None:
			tree = etree.HTML(response)
			flawId_list = tree.xpath('//*[@target="ids"]/attribute::rel')
			bianhao_list = tree.xpath('//*[@target="ids"]/td[3]/text()')
			biaoti_list = tree.xpath('//*[@target="ids"]/td[4]/text()')
			lurushijian_list = tree.xpath('//*[@target="ids"]/td[5]/text()')
			weixiandengji_list = tree.xpath('//*[@target="ids"]/td[6]/text()')
			gongxianzhe_list = tree.xpath('//*[@target="ids"]/td[7]/text()')
			erjishenhe_lists = []
			for i in range(len(bianhao_list)):
				flawId = flawId_list[i].strip()
				bianhao = bianhao_list[i].strip()
				biaoti = biaoti_list[i].strip()
				lurushijian = lurushijian_list[i].strip()
				weixiandengji = weixiandengji_list[i].strip()
				gongxianzhe = gongxianzhe_list[i].strip()
				erjishenhe_list = [bianhao,biaoti,lurushijian,weixiandengji,gongxianzhe,flawId]
				erjishenhe_lists.append(erjishenhe_list)
				#print(flawId)
			# 更新template
			template_dic = self.app.template[1]
			template_dic['erjishenhe_lists'] = erjishenhe_lists
			self.app.template = ("index.html", template_dic)
			# 刷新js
			self.app.evaluate_javascript("$('div#erjishenhe').show();")

	# 二级审核通过
	@htmlPy.Slot(str, result=str)
	def secondExamineUpdate_one(self, json_str):
		json_tab = json.loads(json_str)
		print(json_tab)
		flawId = json_tab['flawId']
		print('erji_update:' + flawId)
		payload = {
			'flawId':flawId,
			'status':'1',
			'isg':'0',
			'content':''
		}
		#response = self.postQuery("http://202.108.212.74:8000/cnvd_admin/flaw/secondExamineUpdate", payload)
		# print(response)
		self.secondExamineList()

	# 二级批量通过
	@htmlPy.Slot(str, result=str)
	def secondExamineUpdate_more(self, json_str):
		json_tab = json.loads(json_str)
		print(json_tab)
		flawIds = json_tab['flawIds']
		flawIds = flawIds.split(",")
		for flawId in flawIds:
			payload = {
				'flawId': flawId,
				'status': '1',
				'isg': '0',
				'content': ''
			}
			# response = self.postQuery("http://202.108.212.74:8000/cnvd_admin/flaw/secondExamineUpdate", payload)
			# print(response)
			print('erji_updates:'+flawId)
		self.secondExamineList()



