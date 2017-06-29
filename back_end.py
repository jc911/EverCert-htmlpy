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
				r = requests.post(url, allow_redirects=False, cookies=cookies, data=payload, proxies=proxies, timeout=5)
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

	# get请求函数
	def getQuery(self, url, payload):
		cookie = self.getCookie()
		cookies = {'JSESSIONID': cookie}
		proxies = {
			# "http": "http://127.0.0.1:8081"
		}
		login_state = self.app.template[1]['login_state']
		if cookie != "null":
			try:
				r = requests.get(url, params=payload, allow_redirects=False, cookies=cookies, proxies=proxies, timeout=3)
				# print(r.text)
				# print(r.status_code)
				if r.status_code == 302 and r.headers['Location'] == 'http://202.108.212.74:8000/cnvd_admin/login/loginFail':
					# print('login failed')
					login_state = 'login failed'
					# 刷新js
					self.app.evaluate_javascript("alert('" + u'session失效，请重新登录' + "');")
				if r.status_code == 200:
					# print(r.text)
					return r.text
			except BaseException, e:
				login_state = e.__class__.__name__
				print('except:', e)
				print(login_state)
				# 刷新js
				self.app.evaluate_javascript("alert('" + login_state + "');")
				return
			finally:
				pass
		elif cookie == "null":
			# 更新template
			template_dic = self.app.template[1]
			template_dic['login_state'] = u'请先登录'
			self.app.template = ("index.html", template_dic)
			# 刷新js
			self.app.evaluate_javascript("alert('" + u'请先登录' + "');")
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

	# 三级审核检索
	@htmlPy.Slot(str, result=str)
	def thirdExamineList(self, json_str):
		json_tab = json.loads(json_str)
		print(json_tab)
		payload = {
			'number' : '',
			'numberType' : '',
			'title' : '',
			'isEvent' : json_tab['isEvent'],
			'hangye' : '',
			'serverityId' : '',
			'isAdditional' : '',
			'email' : '',
			'description' : '',
			'causeId' : '',
			'threadId' : '',
			'positionId' : '',
			'softStyleId' : '',
			'isCancel' : json_tab['isCancel'],
			'isu' : json_tab['isu'],
			'industryId' : '',
			'timeType' : json_tab['timeType'],
			'storageTimeStartStr' : json_tab['storageTimeStartStr'],
			'storageTimeEndStr' : json_tab['storageTimeEndStr'],
			'referenceType' : '',
			'ref_id' : '',
			'is_repeat' : json_tab['is_repeat'],
			'isv' : '',
			'ivp' : '',
			'status' : json_tab['status'],
			'isCut' : ''
		}
		response = self.postQuery("http://202.108.212.74:8000/cnvd_admin/flaw/list", payload)
		#print(response)
		if response != None:
			tree = etree.HTML(response)
			flawId_list = tree.xpath('//*[@target="flawIds"]/attribute::rel')
			bianhao_list = tree.xpath('//*[@target="flawIds"]/td[3]/text()')
			biaoti_list = tree.xpath('//*[@target="flawIds"]/td[5]/text()')
			lurushijian_list = tree.xpath('//*[@target="flawIds"]/td[8]/text()')
			gongxianzhe_list = tree.xpath('//*[@target="flawIds"]/td[10]/text()')
			pingfen_list = tree.xpath('//*[@target="flawIds"]/td[14]/text()')
			sanjishenhe_lists = []
			for i in range(len(bianhao_list)):
				flawId = flawId_list[i].strip()
				bianhao = bianhao_list[i].strip()
				biaoti = biaoti_list[i].strip()
				lurushijian = lurushijian_list[i].strip()
				gongxianzhe = gongxianzhe_list[i].strip()
				pingfen = pingfen_list[i].strip()
				sanjishenhe_list = [flawId,bianhao,biaoti,lurushijian,gongxianzhe,pingfen]
				sanjishenhe_lists.append(sanjishenhe_list)
				#print(flawId)
			# 更新template
			template_dic = self.app.template[1]
			template_dic['sanjishenhe_lists'] = sanjishenhe_lists
			self.app.template = ("index.html", template_dic)
			# 刷新js
			self.app.evaluate_javascript("$('div#sanjishenhe').show();")

	# 三级审核评分查询
	@htmlPy.Slot(str, result=str)
	def calScoreCreate(self, json_str):
		json_tab = json.loads(json_str)
		print(json_tab)
		flawId = json_tab['flawId']
		payload = {'flawId':flawId}
		response = self.getQuery('http://202.108.212.74:8000/cnvd_admin/flaw/calScoreCreate',payload)
		#print(response)
		if response != None:
			tree = etree.HTML(response)
			flawId = tree.xpath('//*[@name="flawId"]/@value')[0]
			basemetric_id = tree.xpath('//*[@name="basemetric.id"]/@value')[0]
			temporalMetric_id = tree.xpath('//*[@name="temporalMetric.id"]/@value')[0]
			environmentalMetric_id = tree.xpath('//*[@name="environmentalMetric.id"]/@value')[0]
			freshId = tree.xpath('//*[@name="freshId"]/@value')[0]
			#提取selected函数
			def tryGetSelected(name):
				try:
					result = tree.xpath('//*[@name="'+name+'"]/option[@selected="selected"]/@value')[0]
					print result
					return result
				except BaseException, e:
					#print(BaseException)
					return
			#基本度量
			accessVector_id = tryGetSelected('accessVector.id')
			accessComplexity_id = tryGetSelected('accessComplexity.id')
			authentication_id = tryGetSelected('authentication.id')
			confidentialityImpact_id = tryGetSelected('confidentialityImpact.id')
			integrityImpact_id = tryGetSelected('integrityImpact.id')
			availabilityImpact_id = tryGetSelected('availabilityImpact.id')
			#时间度量
			exploitability_id = tryGetSelected('exploitability.id')
			remediationLevel_id = tryGetSelected('remediationLevel.id')
			reportConfidence_id = tryGetSelected('reportConfidence.id')
			#环境度量
			collateralDamagePotential_id = tryGetSelected('collateralDamagePotential.id')
			targetDistribution_id = tryGetSelected('targetDistribution.id')
			confidentialityRequire_id = tryGetSelected('confidentialityRequire.id')
			integrityRequire_id = tryGetSelected('integrityRequire.id')
			availabilityRequire_id = tryGetSelected('availabilityRequire.id')
			print(accessVector_id)
			# 更新template
			template_dic = self.app.template[1]
			template_dic['flawId'] = flawId
			template_dic['basemetric_id'] = basemetric_id
			template_dic['temporalMetric_id'] = temporalMetric_id
			template_dic['environmentalMetric_id'] = environmentalMetric_id
			template_dic['freshId'] = freshId
			##时间度量
			template_dic['exploitability_id'] = exploitability_id
			template_dic['remediationLevel_id'] = remediationLevel_id
			template_dic['reportConfidence_id'] = reportConfidence_id
			##环境度量
			template_dic['collateralDamagePotential_id'] = collateralDamagePotential_id
			template_dic['targetDistribution_id'] = targetDistribution_id
			template_dic['confidentialityRequire_id'] = confidentialityRequire_id
			template_dic['integrityRequire_id'] = integrityRequire_id
			template_dic['availabilityRequire_id'] = availabilityRequire_id
			self.app.template = ("index.html", template_dic)
			##基本度量
			def pushSelected(var,name):
				if var != None:
					# 刷新js
					self.app.evaluate_javascript("$('selected[name=\""+name+"\"]').val(\""+var+"\");")
			pushSelected(accessVector_id,"accessVector.id")
			pushSelected(accessComplexity_id, "accessComplexity.id")
			pushSelected(authentication_id, "authentication.id")
			pushSelected(confidentialityImpact_id, "confidentialityImpact.id")
			pushSelected(integrityImpact_id, "integrityImpact.id")
			pushSelected(availabilityImpact_id, "availabilityImpact.id")
			# 刷新js
			self.app.evaluate_javascript("$('div#sanjishenhe').show();")




