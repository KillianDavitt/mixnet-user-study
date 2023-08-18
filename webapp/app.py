from flask import render_template, session, request, redirect
from flask import Flask, send_file
from flask_session import Session
import random
import sqlite3
import time

num_questions = 14

app = Flask(__name__,static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.secret_key = "dskfsdfds"
SESSION_TYPE = 'filesystem'
secret_key= "fhdsfjd"
app.config.from_object(__name__)
Session(app)
delay_options = [1000,2000,3000,4000,0]

@app.route('/c129ad2439821907f5fd.module.wasm')
def wasm_file():
    return send_file('static/c129ad2439821907f5fd.module.wasm', mimetype = 'application/wasm');


def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

with open('questions.csv') as f:
    data = f.readlines()

question_answers = [x.strip().split(',') for x in data]

def run_survey_page():
    #session['prolific_id'] = -1
    if 'filled' in request.form:
        #print(request.form)
        # get all the survey.html results and record them
        #prolific_id = -1
        try:
                delay = request.form['delay']
                rating = request.form['rating']
                speed_rating = request.form['speed_rating']
                adapted = (request.form['adapted']=='True')
                review = request.form['review']
                start_time = request.form['start_time']
                end_time = int(round(time.time() * 1000000000)) // 1000000

                if 'results' not in session:
                    session['results'] = []
                result = {'delay':delay,
                          'rating':rating,
                          'speed_rating':speed_rating,
                          'adapted':adapted,
                          'review':review,
                          'start_time':start_time,
                          'end_time':end_time
                          }
                session['results'].append(result)
                session['completed_delays'].append(delay)
                session['current_delay'] = None
                
        except Exception as err:
            print(err)
            return str(err)
            #return "There was an error please contact the survey administrators"
        
        return redirect('/')



    # We need to save the automerge binary data in the session,
    # then we can extract it at the end of the survey and commit to the db
    if 'automerge_list' not in session:
        automerge_list = list()
        session['automerge_list'] = automerge_list
    automerge_data = request.form['automerge_data']
    automerge_list = session['automerge_list']
    automerge_list.append(automerge_data)
    session['automerge_list'] = automerge_list
    print(automerge_list)
    
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
    session.pop('current_qs', None)
    
    delay = request.form['delay']
    return render_template('survey.html', delay=delay, debug=app.debug)

@app.route('/register_prolific_id')
def register_prolific_id():
    prolific_id = request.args.get('prolific_id')
    session['prolific_id'] = prolific_id
    return redirect('/')

def run_questions_page():
    if 'prolific_id' not in session:
        return render_template('prolific_id.html')
    
    # Get the list of questions this user has already faced
    qas = []
    try: 
        completed_qs = session['completed_qs'].split(',')
        
    except KeyError:
        completed_qs = []

    try: 
        current_qs = session['current_qs'].split(',')
        for i in range(num_questions):
            qas.append(question_answers[int(current_qs[i])])
        
    except KeyError:
        current_qs = []

    current_task_num = int(len(completed_qs)/num_questions)
        
    # Finished all available questions
    if len(completed_qs) >= len(question_answers):
        # Time to write everything to the DB
        try:
            conn = get_db_connection()
            results = session['results']
            automerge_list = session['automerge_list']
            for i,r in enumerate(results):
                conn.execute('INSERT INTO response (prolific_id, delay, review, rating, speed_rating, adapted, start_time, end_time, education, automerge_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (session['prolific_id'], r['delay'], r['review'], r['rating'], r['speed_rating'],r['adapted'],r['start_time'], r['end_time'], session['education_level'], automerge_list[i]))
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return "There was an error in savings your results to the database. Please contact the survey administrator."
        return render_template('end.html', debug=app.debug)

    for i in range(num_questions):
        if len(current_qs)>=num_questions:
            break
        found_n = False
        while not found_n:
            print("finding questions")
            n = random.randint(0,len(question_answers)-1)
            print(n)
            if not str(n) in completed_qs+current_qs:
                found_n = True
        
        qas.append(question_answers[n])
        current_qs.append(str(n))
        
    session['current_qs'] = ','.join(current_qs)

    # Find a random delay which we haven't already used in this session

    try: 
        completed_delays = session['completed_delays']
        print(completed_delays)
        
    except KeyError:
        completed_delays = []
        session['completed_delays'] = []
        
    try: 
        current_delay = session['current_delay']
        
    except KeyError:
        current_delay = None
    

    found_delay = False
    if current_delay != None:
        found_delay = True
        delay = current_delay
    while not found_delay:
        print("finding delay")
        delay = delay_options[random.randint(0,len(delay_options)-1)]
        if not (str(delay) in completed_delays):
            found_delay=True
            session['current_delay'] = delay
            current_delay = delay
   
    
    return render_template('index.html', delay=delay, qas=qas, debug=app.debug, current_task_num=current_task_num+1)

@app.route('/', methods=['GET', 'POST'])
def index():
    prolific_id = request.args.get('PROLIFIC_PID')
    if prolific_id is not None:
        session['prolific_id']=prolific_id

    app.debug=False
 

    if 'consent' not in session:
        return run_consent_page()
        
    if 'education' not in session:
        return run_education_page()

    if 'first_attention_check' not in session:
        return run_first_attention_page()
    
    if not session['consent']:
        print("Error: bad state")
        session.pop('consent',None)
        return render_template('consent.html', debug=app.debug)

    if not session['education']:
        print("Error: bad state")
        session.pop('education',None)
        return render_template('consent.html', debug=app.debug)

    if not session['first_attention_check']:
        print("Error: bad state")
        session.pop('first_attention',None)
        return render_template('consent.html', debug=app.debug)

    if session['failed_first_attention_check']:
        if 'failed_second_attention_check' in session:
            return render_template('failed.html', debug=app.debug)
        return run_first_attention_page()

    if 'briefed' not in session:
        return run_briefing()
        
    
    if request.method == 'POST':
       
        return run_survey_page()

    return run_questions_page()

@app.route('/delete_cookies', methods=['GET'])
def delete_cookies():
    session.clear()
    return redirect('/')

def run_briefing():
    session['briefed']=True
    return render_template('briefing.html')

def run_first_attention_page():
    if request.method == 'POST':
        d = request.form
        q1 = d.get('q1')
        q2 = d.get('q2')
        second=False
        if 'failed_first_attention_check' in session:
            if session['failed_first_attention_check'] == True:
                second = True
        if q1 != '2' and q2 != '6':
            if second:
                session['failed_second_attention_check'] = True
            else:
                session['failed_first_attention_check'] = True
        else:
            if second:
                    session['failed_second_attention_check'] = False
            else:
                session['failed_first_attention_check'] = False

        session['first_attention_check'] = True
        return redirect('/')
    return render_template('attention.html', debug=app.debug)


def run_education_page():
    if request.method == 'POST':
        d = request.form
        education = d.get('education_level')
        #need to save edutation here...
        session['education_level'] = education
        print(education)
        print('dklskdnsdkfnldf')
        session['education'] = True
        return redirect('/')
    return render_template('education.html', debug=app.debug)


def run_consent_page():
    if request.method == 'POST':
        d = request.form
        print(d)
        print(d.get('1'))
        consent = d.get('1') and d.get('2') and d.get('3')
        consent = consent and d.get('4') and d.get('5') and d.get('6')
        print(consent)
        session['consent'] = consent
        return redirect('/')
        
    return render_template('consent.html', debug=app.debug)
