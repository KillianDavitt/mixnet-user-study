from flask import render_template, session, request, redirect
from flask import Flask
import random

app = Flask(__name__,static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.secret_key = "dskfsdfds"
delay_options = [1,500,1000]
app.debug = False


with open('question_set1.csv') as f:
    data = f.readlines()

question_answers = [x.strip().split(',') for x in data]

def run_consent_page():
    if request.method == 'POST':
        d = request.form
        consent = d.get('1') and d.get('2') and d.get('3')
        consent = consent and d.get('4') and d.get('5') and d.get('6')
        print(consent)
        session['consent'] = consent
        return redirect('/')
        
    return render_template('consent.html', debug=app.debug)

def run_survey_page():
    if 'filled' in request.form:
        print(request.form)
        # get all the survey.html results and record them

        return redirect('/')

    try: 
        completed_qs = session['completed_qs'].split(',')
            
    except KeyError:
        completed_qs = []

    try: 
        qas = session['current_qs'].split(',')
    except KeyError:
        qas = []

    completed_qs+=(qas)
    session['completed_qs'] = ','.join(completed_qs)
    del session['current_qs']
    return render_template('survey.html', debug=app.debug)

def run_questions_page():
    # Get the list of questions this user has already faced
    qas = []
    try: 
        completed_qs = session['completed_qs'].split(',')
        
    except KeyError:
        completed_qs = []

    try: 
        current_qs = session['current_qs'].split(',')
        for i in range(6):
            qas.append(question_answers[int(current_qs[i])])
        
    except KeyError:
        current_qs = []
        
    # Finished all available questions
    if len(completed_qs) >= len(question_answers):
        return render_template('end.html', debug=app.debug)

    for i in range(6):
        if len(current_qs)>5:
            break
        found_n = False
        while not found_n:
            n = random.randint(0,len(question_answers)-1)
            print(n)
            if not str(n) in completed_qs+current_qs:
                found_n = True
        
        qas.append(question_answers[n])
        current_qs.append(str(n))
        
    session['current_qs'] = ','.join(current_qs)
    
    delay = delay_options[random.randint(0,len(delay_options)-1)]
    
    return render_template('index.html', delay=delay, qas=qas, debug=app.debug)

@app.route('/', methods=['GET', 'POST'])
def index():
    app.debug=True

    if 'consent' not in session:
        return run_consent_page()
        

    if not session['consent']:
        print("Error: bad state")
        session.pop('consent',None)
        return render_template('consent.html', debug=app.debug)
    
    if request.method == 'POST':
        return run_survey_page()

    return run_questions_page()

@app.route('/delete_cookies', methods=['GET'])
def delete_cookies():
    session.pop('completed_qs', None)
    session.pop('consent',None)
    print("Its still in the dict")
    print('consent' in session)
    return redirect('/')
