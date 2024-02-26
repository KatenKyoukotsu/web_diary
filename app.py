from flask import Flask,render_template,request,redirect,session,url_for,flash
import mysql.connector
from datetime import datetime
app=Flask(__name__,template_folder='temp')
connection = mysql.connector.connect(host="localhost",user="root",passwd="",database="project")
app.secret_key='super secret key'
@app.route('/')
def index():
    return render_template('login.html')
@app.route('/home')
def home():
    pk=session['name']
    cur = connection.cursor()
    cur.execute("SELECT  * FROM data where name=%s ",(pk,))
    y = cur.fetchall()
    return render_template('index.html',y=y,name=session['name'])
@app.route('/Signup')
def index2():
    return render_template('signup.html')
@app.route('/home2')
def home2():
    return render_template('index.html',name=session['name'])
#login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        cursor=connection.cursor()
        cursor.execute('select * from login where name=%s and password=%s',(name,password))
        record=cursor.fetchone()
        if record:
            session['loggedin']=True
            session['name']=record[1]
            ok=session['name']
            return redirect(url_for('home'))
        flash("Incorrect Name/Password")
        return redirect(url_for('index'))
#Sign Up
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        password=request.form['password']
        cursor=connection.cursor()
        cursor.execute('insert into login (name,phone,email,password) values(%s,%s,%s,%s)',(name,phone,email,password))
        connection.commit()
        cursor2=connection.cursor()
        cursor2.execute('select * from login where name=%s and password=%s',(name,password))
        record2=cursor2.fetchone()
        if record2:
            session['loggedin']=True
            session['name']=record2[1]
            return redirect(url_for('home2')) 
#Home
@app.route('/Welcome',methods=['GET','POST'])
def sweet():
    if request.method=='POST':
         user=request.form
         title=user['title']
         text=user['text']
         pk=session['name']
         now = datetime.now()
         year = now.strftime("%Y")
         month = now.strftime("%m")
         day = now.strftime("%d")
         time = now.strftime("%H:%M:%S")
         date_time = now.strftime("%d/%m/%Y %H:%M:%S")
         cur=connection.cursor()
         cur.execute("insert into data (name,date,title,text) values(%s,%s,%s,%s)",(pk,date_time,title,text))
         connection.commit()
         cur2=connection.cursor()
         cur2.execute("select * from data where name=%s",(pk,))
         y=cur2.fetchall()
    return render_template('index.html',y=y,name=session['name'])
#Update home
@app.route('/edit/<string:id>', methods = ['POST', 'GET'])
def get(id):
    cur = connection.cursor()
    cur.execute('SELECT * FROM data WHERE id = %s', (id,))
    y = cur.fetchall()
    cur.close()
    return render_template('EDIT.html', y=y,name=session['name'])
@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        user=request.form
        title = user['title']
        text = user['text']  
        cur = connection.cursor()
        cur.execute("""
            UPDATE data
            SET title = %s,
                text = %s
            WHERE id = %s
        """, (title, text,  id))
        connection.commit()
        return redirect(url_for('home'))
#Delete home
@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    cur = connection.cursor()
    pk=session['name']
    cur.execute("delete from data where id =%s and name=%s",(id,pk))
    connection.commit()
    return redirect(url_for('home'))
#User
@app.route('/users')
def users():
    pk=session['name']
    cur =connection.cursor()
    cur.execute("SELECT  * FROM login where name=%s" ,(pk,))
    y= cur.fetchall()
    cur.close()
    return render_template('users.html',y=y,name=session['name'])
#Update User
@app.route('/edit2/<string:id>', methods = ['POST', 'GET'])
def get2(id):
    cur = connection.cursor()
    cur.execute('SELECT * FROM login WHERE id = %s', (id,))
    y = cur.fetchall()
    cur.close()
    return render_template('USEREDIT.html', y=y,name=session['name'])
@app.route('/update2/<string:id>', methods=['POST'])
def update2(id):
    if request.method == 'POST':
        user=request.form
        name = user['name']
        phone = user['phone']
        email = user['email']
        password = user['password']
        cur = connection.cursor()
        cur.execute("""
            UPDATE login
            SET name = %s,
                phone = %s,
                email = %s,
                password = %s
            WHERE id = %s
        """, (name,phone,email, password,  id))
        connection.commit()
        return redirect(url_for('users'))
#Delete User 
@app.route('/deleteuser/<string:id>', methods = ['GET'])
def deleteuser(id):
    cur = connection.cursor()
    pk=session['name']
    cur.execute("delete from login where id =%s and name=%s",(id,pk))
    connection.commit()
    cur2=connection.cursor()
    cur2.execute("delete  from data where name=%s",(pk,))
    connection.commit()
    cur3=connection.cursor()
    cur3.execute("delete  from appointment where name=%s",(pk,))
    connection.commit()
    return redirect(url_for('index'))
@app.route('/app') 
def index3():
    pk=session['name']
    cur3=connection.cursor()
    cur3.execute("select * from appointment where name=%s",(pk,))
    y=cur3.fetchall()
    return render_template('appointment.html',xyz=y,name=pk)
#Appointment
@app.route('/appointment')
def appointment():
    pk=session['name']
    cur = connection.cursor()
    cur.execute("SELECT  * FROM appointment where name=%s ",(pk,))
    y = cur.fetchall()
    return render_template('appointment.html',xyz=y,name=session['name'])
@app.route('/appointments',methods=['GET','POST'])
def sweet2():
    if request.method=='POST':
         user=request.form
         title=user['title']
         datetime=user['datetime']
         pk=session['name']
         cur=connection.cursor()
         cur.execute("select * from appointment where name=%s and date=%s",(pk,datetime))
         result=cur.fetchone()
         if result:
             if datetime==result[2]:
                 flash("🙁 You already had appointment")
             return redirect(url_for('index3'))
         cur2=connection.cursor()
         cur2.execute("insert into appointment (name,date,title) values(%s,%s,%s)",(pk,datetime,title))
         connection.commit()
         cur3=connection.cursor()
         cur3.execute("select * from appointment where name=%s",(pk,))
         y=cur3.fetchall()
    return render_template('appointment.html',xyz=y,name=session['name'])
#Update appointment
@app.route('/edit3/<string:id>', methods = ['POST', 'GET'])
def get3(id):
    cur = connection.cursor()
    cur.execute('SELECT * FROM appointment WHERE id = %s', (id,))
    y = cur.fetchall()
    cur.close()
    return render_template('EDITAPP.html', y=y,name=session['name'])
@app.route('/update3/<string:id>', methods=['POST'])
def update3(id):
    if request.method == 'POST':
        user=request.form
        title = user['title']
        date = user['datetime']  
        cur = connection.cursor()
        cur.execute("""
            UPDATE appointment
            SET title = %s,
                date = %s
            WHERE id = %s
        """, (title, date,  id))
        connection.commit()
        return redirect(url_for('appointment'))
#Delete Appointment
@app.route('/deleteapp/<string:id>', methods = ['GET'])
def deleteapp(id):
    cur = connection.cursor()
    pk=session['name']
    cur.execute("delete from appointment where id =%s and name=%s",(id,pk))
    connection.commit()
    return redirect(url_for('appointment'))
#Log Out
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('name',None)
    return redirect(url_for('index'))
app.run(debug=True)