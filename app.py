from flask import Flask, render_template, request, redirect, url_for, session
import dataset, random, os

app = Flask(__name__)
# app.secret_key = os.urandom(24)


db = dataset.connect("postgres://feigvvdnvgpvix:c33f2567b16aafc2924b6d46d27255fc601b6bd1707d037428271e71707febf3@ec2-107-21-224-61.compute-1.amazonaws.com:5432/d5u2ntdkbbbn86")
logged_in_user = ""

user_table = db["users"]
gamevote = db["games"]

@app.route('/<page_name>')
def go_to_page(page_name):
   return render_template(page_name + ".html")


# @app.route('/<page_name>/')
# def go_to_page_slash(page_name):
#    return render_template(page_name + ".html")

# @app.route('/<page_name>/')
# def go_to_page_slash_html(page_name):
#    return render_template(page_name + ".html")

@app.route('/home')
def homepage():
	return render_template('home.html')

@app.route('/handleuser', methods=["GET","POST"])
def handle_userform():
	# 1. Get information that the user typed into form
	username = request.form["username"]
	password = request.form["password"]
	# 2. Put this information into the DataBase
	return add_user(username, password)

def add_user(username, password):
	# CHECK IF THE USER ALREADY EXISTS
	if user_table.find_one(name=username):
		return "ERROR: USER ALREADY REGISTER"
	user_table.insert(dict(name=username, pw=password))
	return "User has been added!"

@app.route('/login')
def login_form():
	return render_template("thelogin.html")


@app.route('/handlelogin', methods=["POST"])
def handle_login():
	global logged_in_user 
	# 1. Get what the user typed in
	username = request.form["username"]
	password = request.form["password"]
	# 2. CHECK IF THE USER ALREADY EXISTS
	if user_table.find_one(name = username, pw = password):
		logged_in_user = username
		return "Success! Logged in"
	else:
		return "Failure! User or password is wrong"


#If the user clicked basketball ---> add vote to basketball


def add_vote(user, basketball, football , frisbee):
	gamevote.insert(dict(user = user, basketball = basketball, football = football, frisbee = frisbee))



@app.route("/handlevote", methods=["GET","POST"])
def handle_vote():
	basketball,football,frisbee=0,0,0
	value=request.form["sport"]
	if(value=="BB"):
		basketball=1
	elif(value=="FB"):
		football=1
	elif(value=="F"):
		frisbee=1
	if not gamevote.find_one(user=logged_in_user):
		gamevote.insert(dict(user =logged_in_user,basketball=basketball,football=football,frisbee=frisbee))
		listResult=list(db['games'].all())
		result=calculate_rate(listResult)

		return render_template("showrate.jinja",result=result)
	else:
		return "please login!"
def calculate_rate(listRes):
	sum1,sum2,sum3=0,0,0
	for i in listRes:
		sum1=sum1+i['basketball']
		sum2=sum2+i['football']
		sum3=sum3+i['frisbee']
	result=[]
	result[0]=(sum1/len(listRes))*100
	result[1]=(sum2/len(listRes))*100
	result[2]=(sum3/len(listRes))*100
	return result


@app.route("/showdb")
def show_db():
	gameList = list(db['games'].all())
	return render_template("showdb.jinja",list=gameList)





#-User- -Basketball- -Football- -Frisbee- --------#
#								         		  #
#										          #
#										          #
#										          #
#										          #
#										          #
#										          #
#										          #
# 				          				          #
#										          #
# 				          				          #
#										          #
# 				          				          #
#-------------------------------------------------#




# TODO: route to /register

# TODO: route to /error

if __name__ == "__main__":
	app.debug = True
	app.run(port=3000)