from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.metrics import AUC
import numpy as np

from flask_mysqldb import *


app = Flask(__name__) #Initialize the flask App

app.secret_key = "fake"#databasename
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # Update with your MySQL root password
app.config['MYSQL_DB'] = 'fake'#databasename
mysql = MySQL(app)

dependencies = {
    'auc_roc': AUC
}
 

verbose_name = {
0: 'Fake', 
1: 'Real'
           }
 


model = load_model('currency.h5')
 

def predict_label(img_path):
	test_image = image.load_img(img_path, target_size=(224,224))
	test_image = image.img_to_array(test_image)/255.0
	test_image = test_image.reshape(1, 224,224,3)

	predict_x=model.predict(test_image) 
	classes_x=np.argmax(predict_x,axis=1)
	
	return verbose_name[classes_x[0]]
    
 
 
@app.route("/")
@app.route("/home")
def first():
	return render_template('home.html')
    
@app.route("/login")
def login():
	return render_template('login.html')     
@app.route("/index", methods=['GET', 'POST'])
def index():
	return render_template("index.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/tests/" + img.filename	
		img.save(img_path)

		predict_result = predict_label(img_path)

	return render_template("prediction.html", prediction = predict_result, img_path = img_path)



    

@app.route("/performance")
def performance():
	return render_template('performance.html')
@app.route("/register")
def register():
	return render_template('register.html')


@app.route('/insertvalues', methods=['POST'])
def insertvalues():
        cursor = mysql.connection.cursor()
        uname = request.form['uname']
        pwd = request.form['pwd']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute('INSERT INTO register (username, password, email, phone) VALUES (%s, %s, %s, %s)', (uname, pwd, email, phone,))
        mysql.connection.commit()
        cursor.close()
        return render_template('login.html')

@app.route('/loginvalidation', methods=['POST'])
def loginvalidation():
	cursor = mysql.connection.cursor()
	uname = request.form['uname']
	pwd = request.form['pwd']
	cursor.execute('select * from register where username=%s and password=%s', (uname, pwd,))
	if(cursor.fetchone()):
		return render_template('index.html')
	else:
		return render_template('login.html')		

@app.route("/chart")
def chart():
	return render_template('chart.html') 

	
if __name__ =='__main__':
	app.run(debug = True)


	

	


