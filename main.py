# coding:utf-8
import os
import htmlPy
#from PyQt4 import QtGui

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = htmlPy.AppGUI(title=u"Application", maximized=False, plugins=True, developer_mode=True)

app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")



from back_end import BackEnd
app.bind(BackEnd(app))
#app.template = ("index.html", {})
# 初始化template
template_dic = {}
template_dic['login_state'] = ''
app.template = ("index.html", template_dic)

if __name__ == "__main__":
	app.start()
