from flask import render_template
from flask import Flask
import random

app = Flask(__name__,static_url_path='', 
            static_folder='static',
            template_folder='templates')

delay_options = [50,500,1000]


with open('question_set1.csv') as f:
    data = f.readlines()

question_answers = [x.split(',') for x in data]

@app.route('/')
def index():

    qas = []
    for i in range(6):
        n = random.randint(0,len(question_answers)-1)
        # if n in var list, go again
        qas.append(question_answers[n])
        # add n to var list
    
    delay = delay_options[random.randint(0,len(delay_options)-1)]
    #i = (i+1)% len(delay_options)
    print(qas)
    return render_template('index.html', delay=delay, qas=qas)
