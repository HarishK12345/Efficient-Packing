from flask import Flask, render_template,request,session
from knapsack_01 import knapsack_dynamic_programming
from knapsack_frac import knapsack_frac
from adt import item
import sqlite3


app = Flask(__name__)

app.secret_key='abc@123'

@app.route('/')
def home():
    try:
        if session['loggedin']==True:
            return render_template('logout.html')
        else:
            return render_template('index.html')
    except:
        return render_template('index.html') 

@app.route('/login', methods=['GET','POST'])
def loginchk():
    msg=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        mail=str(request.form['email'])
        pasw=str(request.form['password'])
        connection=sqlite3.connect('Customer.db')
        cursor=connection.cursor()
        cursor.execute("SELECT NAME,MAIL,PASSWORD FROM CUSTOMER WHERE MAIL = ? and PASSWORD = ?;",(mail,pasw))
        row=cursor.fetchall()
        if len(row)==1:
            session['loggedin'] = True
            session['name']=row[0][0]
            return render_template('logout.html')
        else:
            msg='incorrect login credentials! please recheck'
    return render_template('login.html',msg=msg)

@app.route('/register', methods=['GET','POST'])
def register():
    msg=''
    if request.method == 'POST':
        name=str(request.form['name'])
        mail=str(request.form['email'])
        ph=int(request.form['phone'])
        pasw=str(request.form['password'])
        if len(name)<15:
            if len(mail)<25:
                if '@gmail.com'in mail:
                    if len(str(ph))==10:
                        if len(pasw)<8:
                            connection=sqlite3.connect('Customer.db')
                            cursor=connection.cursor()
                            cursor.execute('''INSERT INTO CUSTOMER VALUES(?,?,?,?);''',(name,mail,ph,pasw))
                            connection.commit()
                            msg='registered successfully!'
                            session['loggedin'] = True
                            session['name']=name
                            return render_template('logout.html')
                        else:
                            msg='password length should be within 8 characters!'
                    else:
                        msg='enter a valid phone number!'
                else:
                    msg='email id should contain @gmail.com!'
            else:
                msg='email-id too long!'
        else:
            msg='name is more than the limit of 14 letters!'
    return render_template('register.html',msg=msg)

@app.route('/logout', methods=['GET','POST'])
def logout():
    session['loggedin']=False
    return render_template('index.html')

@app.route('/knapsack')
def knapsack():
    try:
        if session['loggedin']==True:
            return render_template('knapsack.html')
        else:
            return render_template('login.html')
    except:
        return render_template('login.html')    

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/weights-and-values', methods=['POST'])
def weights_and_values():
    num_products = int(request.form['num-products'])
    capacity = int(request.form['capacity'])
    return render_template('weights_and_values.html', num_products=num_products,capacity=capacity)

@app.route('/result', methods=['POST'])
def result():
    num_products = int(request.form['num-products'])
    capacity = int(request.form['capacity'])
    weights = []
    values = []
    names=[]
    types=[]

    for i in range(num_products):
        name = str(request.form[f'name{i}'])
        weight = int(request.form[f'weight{i}'])
        value = int(request.form[f'value{i}'])
        category=int(request.form[f'divisible{i}'])
        names.append(name)
        weights.append(weight)
        values.append(value)
        types.append(category)

    # if all products are indivisible it will choose 0/1 knapsack method
    global notincluded
    if 1 not in types:
        result,notincluded=knapsack_dynamic_programming(names,weights, values, capacity)
    else:
        objs=[]
        for i in range(len(weights)):
            if types[i]==1:
                item_type='Divisible'
            else:
                item_type='InDivisible'
            obj=item(names[i],weights[i],values[i],item_type)
            objs+=[obj]
        
        
        result,notincluded=knapsack_frac(objs,capacity)
    global selected_products
    optimal_solution = result[0]
    selected_products = result[1]
    global selp
    selp=""
    noti=""
    for i in selected_products:
        selp+=i.name+" "
    for i in notincluded:
        noti+=i.name+" "
    if notincluded==[]:
        return render_template('result1.html', optimal_solution=optimal_solution, selected_products=selp)
    else:
        return render_template('result2.html', optimal_solution=optimal_solution, selected_products=selp,not_included=noti)

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/final1')
def final():
    return render_template('final1.html', selected_products=selp,not_included=notincluded)

if __name__ == '__main__':
    app.run(debug=True)