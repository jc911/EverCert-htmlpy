import os
import htmlPy
#from PyQt4 import QtGui

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = htmlPy.AppGUI(title=u"Application", maximized=False, plugins=True, developer_mode=True)

app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR)



from back_end import BackEnd
app.bind(BackEnd(app))

app.template = ("index.html", {})

if __name__ == "__main__":
	app.start()