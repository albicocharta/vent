import os
import subprocess
from subprocess import Popen, PIPE, check_output
#from flask import Flask, redirect, session, render_template
from flask import *

from jinja2 import Environment, FileSystemLoader


key_dict = {'зрительный':1, 'торжественный':2, 'гостиная':3, 'администрация':4, 'студия':5, 'приточка':6 }

key_arr = [False]*9

passport_vent = 'passport_vent'
passport_zvuk = 'passport_zvuk'


def vent():
    f = open('/var/vent/auto.txt', 'r')
    if f.read().split('\n')[0] == 'True':
        key_arr[0] = True
    else:
        key_arr[0] = False
    f.close()

    bashCommand = "usbrelay"
    session =  subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, stderr = session.communicate()
    if stderr:
        raise Exception("Error "+str(stderr))
    
    output = output.split()
    output = list(map(lambda x: x.decode('utf-8'), output))
    output = list(map(lambda x: x[6:], output))
    for i in range(1,7):
        if (str(i) + '=1') in output:
            key_arr[i] =  True
            print('start')
        if (str(i) + '=0') in output:
            key_arr[i] =  False
            print('stop')

    
vent()


environment_index = Environment(loader=FileSystemLoader("templates/"))
template_index = environment_index.get_template("index.html")
def index_html():
    vent()
    global template_index
    class_card = ['', '', '', '', '', '', '']
    card_title = ['', '', '', '', '', '', '']
    a_btn_class = ['', '', '', '', '', '', '']
    a_btn_text = ['', '', '', '', '', '', '']

    
    for i in [0, 1, 2, 3, 4, 5, 6]:
        if key_arr[i]:
            class_card[i] = 'card text-bg-danger mb-3'
            card_title[i] = 'ВКЛ'
            a_btn_class[i] = 'btn btn-dark'
            a_btn_text[i] = 'Отключить'
        else:
            class_card[i] = 'card'
            card_title[i] = 'ОТКЛ'
            a_btn_class[i] = 'btn btn-success'
            a_btn_text[i] = 'Включить'

    if class_card[0] == 'card text-bg-danger mb-3':
        class_card[0] = 'card text-bg-secondary mb-3'


    f=open('/var/vent/auto.txt')
    text_auto = f.read().split('\n')
    f.close()
    text_auto ='<p>' +  '</p> <p>'.join(text_auto) + '</p>'
 
    content = template_index.render(
            class_card0 = class_card[0],
            class_card1 = class_card[1],
            class_card2 = class_card[2],
            class_card3 = class_card[3],
            class_card4 = class_card[4],
            class_card5 = class_card[5],
            class_card6 = class_card[6],
            

            card_title0 = card_title[0],
            card_title1 = card_title[1],
            card_title2 = card_title[2],
            card_title3 = card_title[3],
            card_title4 = card_title[4],
            card_title5 = card_title[5],
            card_title6 = card_title[6],
            

            a_btn_class0 = a_btn_class[0],
            a_btn_class1 = a_btn_class[1],
            a_btn_class2 = a_btn_class[2],
            a_btn_class3 = a_btn_class[3],
            a_btn_class4 = a_btn_class[4],
            a_btn_class5 = a_btn_class[5],
            a_btn_class6 = a_btn_class[6],
            
            a_btn_text0 = 'Редактировать',
            a_btn_text1 = a_btn_text[1],
            a_btn_text2 = a_btn_text[2],
            a_btn_text3 = a_btn_text[3],
            a_btn_text4 = a_btn_text[4],
            a_btn_text5 = a_btn_text[5],
            a_btn_text6 = a_btn_text[6],

            card_text_auto = text_auto
        )
    return content






environment_auto = Environment(loader=FileSystemLoader("templates/"))
template_auto = environment_index.get_template("auto.html")
def auto_html():
    vent()
    global template_auto

    f=open('/var/vent/auto.txt')
    text_auto = f.read()
    f.close()
    content = template_auto.render(
            card_text_auto = text_auto
        )
    return content


environment_zvuk = Environment(loader=FileSystemLoader("templates/"))
template_zvuk = environment_zvuk.get_template("index_zvuk.html")
def index_html_zvuk():
    vent()
    global template_zvuk
    class_card = ['', '', '', '', '', '', '']
    card_title = ['', '', '', '', '', '', '']
    a_btn_class = ['', '', '', '', '', '', '']
    a_btn_text = ['', '', '', '', '', '', '']
    
    for i in [5]:
        if key_arr[i]:
            class_card[i] = 'card text-bg-danger mb-3'
            card_title[i] = 'ВКЛ'
            a_btn_class[i] = 'btn btn-dark'
            a_btn_text[i] = 'Отключить'
        else:
            class_card[i] = 'card'
            card_title[i] = 'ОТКЛ'
            a_btn_class[i] = 'btn btn-success'
            a_btn_text[i] = 'Включить'
            
    content_zvuk = template_zvuk.render(
            class_card5 = class_card[5],
            
            card_title5 = card_title[5],
            
            a_btn_class5 = a_btn_class[5],
            
            a_btn_text5 = a_btn_text[5]   
        )
    return content_zvuk

















app = Flask(__name__)

import config 
app.secret_key = config.secret_key


@app.route('/',methods=['GET'])
def home():
    if passport_vent == session.get('visit'):
        return index_html()
    elif passport_zvuk == session.get('visit'):
        return index_html_zvuk()
    else:
        return redirect(f"/login")


@app.route('/relay/<num_relay>',methods=['GET'])
def relay(num_relay):
    if passport_vent == session.get('visit') or passport_zvuk == session.get('visit'):
        i = int(num_relay[-1])
        key_arr[i] = not key_arr[i]
        if key_arr[i]:
            s = 'HW554_' + str(i) + '=1'
        else:
            s = 'HW554_' + str(i) + '=0'
        subprocess.call(["usbrelay", s], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
        return redirect(f"/")
    else:
        return redirect(f"/login")




@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')



@app.route('/success',methods = ["POST"]) 
def success(): 
    if request.method == "POST": 
        session['visit']=request.form['pass'] 
    return redirect(f"/")

@app.route('/delpass',methods = ["GET"]) 
def delpass(): 
    session['visit'] = None
    return redirect(f"/")


@app.route('/auto',methods=['GET'])
def auto():
    return auto_html()


@app.route('/auto_success',methods = ["POST"]) 
def success_auto(): 
    if passport_vent == session.get('visit'):
        if request.method == "POST": 
            s = request.form['text']
            f = open('/var/vent/auto.txt', 'w')
            f.write(s)
            f.close()
    return redirect(f"/")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=False)
