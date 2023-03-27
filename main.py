from flask import Flask 
from datetime import timedelta
import random
from hashlib import sha512
from sys import platform
import pandas as pd
import os,shutil,random
from flask import render_template ,request,redirect,url_for,session
app = Flask(__name__)
app.secret_key = "RBS9clfn77yxojqz"
app.permanent_session_lifetime = timedelta(days=5)


# articles ka pehle dekh usme different os and articles ka alag folder bana with photos
# 
#  
# message flashing

fields = ["ID","User Name","Email_id","Phone_number","Password","Salt","First_login"]
fields_details = ["ID","age","weight","height","blood group"]
class articles:
    # locs = {1:"\article1.txt", 2:"\article2.txt", 3:"\article3.txt", 4:"\article4.txt", 5:"\article5.txt", 6:"\article6.txt", 7:"\article7.txt", 8:"\article8.txt", 9:"\article9.txt", 10:"\article10.txt", 11:"\article11.txt", 12:"\article12.txt", 13:"\article13.txt", 14:"\article14.txt", 15:"\article15.txt", 16:"\article16.txt", 17:"\article17.txt", 18:"\article18.txt", 19:"\article19.txt", 20:"\article20.txt", 21:"\article21.txt", 22:"\article22.txt", 23:"\article23.txt", 24:"\article24.txt", 25:"\article25.txt", 26:"\article26.txt", 27:"\article27.txt", 28:"\article28.txt", 29:"\article29.txt", 30:"\article30.txt", 31:"\article31.txt"}
    def locs_list():
        locs = {}
        if platform == 'win32':
            working_folder = os.getcwd() + r"\resources\articles"
            articles_list = os.listdir(working_folder)
            for i in range(len(articles_list)):
                locs[i+1] = working_folder +"\\" + articles_list[i]

        else:
            working_folder = os.getcwd() + "/resources/articles"
            articles_list = os.listdir(working_folder)
            for i in range(len(articles_list)):
                locs[i+1] = working_folder + "/" + articles_list[i]
        return locs


    def random_article(locs):
        a = len(locs)
        val = random.randint(1, a)
        return locs[val]
    def read_heading(file):
        with open(file,mode='r') as curr_file:
            heading = curr_file.readline()
        return heading
    def read_body(file):
        body_arr = []
        with open(file,mode='r') as curr_file:
            heading = curr_file.readline()
            body = curr_file.readlines()
            for i in body:
                body_arr.append(i)
        return body_arr
#  random article generation and reading and have a done file   
class file_id:

    def User_info():
        cwd = os.getcwd()
        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\User_info.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/User_info.csv"
        
        try:
            os.mkdir(working_dir)
        except:
            pass
        return working_file
    
    def details():
        cwd = os.getcwd()
        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + r"\details.csv"
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + "/details.csv"
        
        return working_file
    def articles(name):
        Name = name
        cwd = os.getcwd()
        if platform == 'win32':
            working_dir = cwd + r"\resources"
            working_file = working_dir + Name
        elif platform == 'darwin' or platform =='linux':
            working_dir = cwd + "/resources"
            working_file = working_dir + Name
        
        return working_file


@app.route("/",methods =['GET','POST'])
def landing_page():
   
    return render_template("landing_page.html")
 
@app.route("/mainpage")
def main_page():
    if 'Id' in session:
        Id = session['Id']
        locs = articles.locs_list()
        article = articles.random_article(locs)
        head = articles.read_heading(article)
        body = articles.read_body(article)
        return render_template('main.html',Id = Id,head = head,body= body)
    else: 
        return redirect('signinpage')
@app.route("/signuppage",methods=['GET','POST'])
def SignUp_page():
    username = ""
    password = ""
    if request.method == 'POST':
        username = request.form['User_name']
        Email_id = request.form['Email_id']
        Phone = request.form['Phone_number']
        password = request.form['password']
        reenter =  request.form['re_password'] 
        
        df = pd.read_csv(file_id.User_info())
        user_list = df["User Name"]
        user_list = list(user_list)
        if len(Phone) != 10:
            return render_template("signuppage.html")

        if password == reenter :
            if username not in user_list:
                return account_creation(username, password,Email_id,Phone)
            else:
                return "<h1> User already exists please Sign In</h1>"
        else:
            return "<h1>Wrong Confirm Password go back to home page</h1>"
    else:
        return render_template("signuppage.html")

@app.route("/signinpage",methods=['GET','POST'])
def SignIn_page():
    if request.method == 'POST':
        username = request.form['User_name']
        password = request.form['password']
        rememberme = request.form.get('rememberme')
        password_encoded = sha512(password.encode()).hexdigest()
    
        df = pd.read_csv(file_id.User_info())
        user_list = df["User Name"]
        user_list = list(user_list)
        
        if username in user_list:
            password_list = df["Password"]
            password_list = list(password_list)
            num = user_list.index(username)
            pass_in_data = password_list[num]
            salt_list =  df["Salt"]
            salt_list = list(salt_list)
            salt = salt_list[num]
            log_list = df["First_login"]
            log_list = list(log_list)
            log = log_list[num]

            password_encoded = password_encoded + salt

            if pass_in_data == password_encoded:
                session['Id'] = num
                if rememberme == '1':
                    session.permanent = True   
                else:
                    session.permanent = False            
                if log==0:
                    df.at[num,'First_login'] = 1
                    
                    df1 = df[fields]
                    df1.to_csv(file_id.User_info())
                    
                    return redirect(url_for("more_detail")) # return more details page
                
                return redirect('mainpage') # return main page here
            else:
                return "<h1> Wrong Username or Password</h1>"
        else:
                return "<h1> Wrong Username or Password</h1>"
    if 'Id' in session:
        return redirect('mainpage')
    return render_template("signinpage.html")


@app.route("/accountdetails",methods=['GET','POST'])
def more_detail():  
    # if First_login == 1
    # if first login ==2 dont record data
    if 'Id' in session:
        Id = session['Id']

        df1 = pd.read_csv(file_id.details())
        df  = pd.read_csv(file_id.User_info())
        First_login_list = df['First_login']
        first_login = First_login_list[Id]
        
        if first_login == 1:
            if request.method == 'POST':
                
                age = request.form['age']
                weight  = request.form['weight']
                height = request.form['height']
                blood_group = request.form['blood_group']
                
                df1 = df1[fields_details]
                data = [[Id,age,weight,height,blood_group]]
                df2 = pd.DataFrame(data,columns=fields_details)
                df1 = df1.append(df2)
                df1 = df1[fields_details]
                df.at[Id,'First_login'] = 2
                df = df[fields]
                df.to_csv(file_id.User_info())
                df1.to_csv(file_id.details())

                return redirect('/mainpage')
        else:
            return redirect('/mainpage')
        return render_template('more_details.html')
    else:
        return redirect('/signinpage')

@app.route('/logout')
def logout():
    session.pop('Id',None)
    return redirect(url_for('SignIn_page'))



def account_creation(username , password,Email_id,Phone):
    # here we will create a private key and public key for the user
    password_encoded = sha512(password.encode()).hexdigest()
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    chars=[]

    for i in range(16):
        chars.append(random.choice(ALPHABET))
    salt = "".join(chars)
    password_encoded = password_encoded + salt
    # here we are appending the data to our files
    
    df = pd.read_csv(file_id.User_info())
    df1 = df[fields]
    Id_arr = df["ID"]
    num = Id_arr[len(Id_arr)-1] + 1
    log = 0
    data = [[num,username,Email_id,Phone,password_encoded,salt,log]]
    df2 = pd.DataFrame(data,columns=fields)
    df1 = df1.append(df2)
    df1 = df1[fields]
    df1.to_csv(file_id.User_info())
    return render_template("signupcomplete.html") # here we will return the account confirmation page

if(__name__ ==" __main__"):
    app.run()


