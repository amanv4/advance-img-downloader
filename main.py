# Importing the necessary  libraries
import re
import uuid
from flask import Flask, render_template, request, send_file
from flask_cors import cross_origin

from Scheduler import ScheduleJob
from Logger import Logging

# Configuring the logger
logger_ins = Logging('Advance Image Extractor')  # Creating an instance of custom logger
logger_ins.initialize_logger()  # Instantiating the logger instance

ade = Flask(__name__)  # Initializing the Flask App with the name 'ade'


# Home Page Route
@ade.route('/', methods=['GET'])
@cross_origin()
def index_home():
    
    # This Function is responsible for showing the home page

    try:
        if request.method == 'GET':
            logger_ins.print_log('Inside the index_home function', 'info')
            logger_ins.print_log('Rendering the home.html page', 'info')
            return render_template('home.html')
        else:
            logger_ins.print_log('(main.py) - Something went wrong Method not allowed', 'exception')
            return render_template('error.html', msg='Method not allowed')
    except Exception as e:
        logger_ins.print_log('(main.py) - Something went wrong ' + str(e), 'exception')
        return render_template('error.html', msg=str(e))


#  Submitted Page Route
@ade.route('/job_submitted', methods=['POST'])
@cross_origin()
def job_submitted():
    
    # This function is responsible for performing the various things after the job is submitted by the user

    try:
        if request.method == 'POST':
            logger_ins.print_log('Inside the job_submitted function', 'info')

            # Handling the user input
            search_query = request.form['search-query'].lower()
            date = request.form['date']
            time = request.form['time']
            email = request.form['email'].lower()
            no_images = request.form['images']

            is_valid, error = validate_inputs(search_query, date, time, email, no_images)

            if is_valid:
                # Creating the unique ID for the request generated
                req_id = uuid.uuid4()

                # Creating a object for th e scheduler
                schedule_job = ScheduleJob()

                # Adding the job in the scheduler
                schedule_job.insert_request(search_query, date, time, int(no_images), email, req_id)

                logger_ins.print_log('Schedule is added for adding the job in queue', 'info')

                # Rendering the Job Submitted template
                logger_ins.print_log('Rendering the job_submitted.html template', 'info')
                return render_template('job_submitted.html')
            else:
                logger_ins.print_log('(main.py) - Something went wrong ' + error, 'exception')
                return render_template('error.html', msg=error)

        else:
            logger_ins.print_log('(main.py) - Something went wrong Method is not allowed', 'exception')
            return render_template('error.html', msg='Method not allowed')

    except ValueError:
        logger_ins.print_log('(main.py) - Something went wrong. No of images must be a number', 'exception')
        return render_template('error.html', msg='No of images must be a number')

    except Exception as e:
        logger_ins.print_log('(main.py) - Something went wrong ' + str(e), 'exception')
        return render_template('error.html', msg=str(e))


# Downloading the images route
@ade.route('/download/<search_term>/<uuid:req_id>', methods=['GET'])
@cross_origin()
def download(search_term, req_id):

  # This Function is responsible for sending the zip file to the requested user

    try:
        logger_ins.print_log('Inside the download route', 'info')
        str_req_id = str(req_id)

        # Sending the downloadable file to the user
        return send_file(str_req_id + '_zipfile.zip', as_attachment=True, attachment_filename=search_term + '.zip')

    except Exception as e:
        logger_ins.print_log('(main.py) - Something went wrong ' + str(e), 'exception')
        return render_template('error.html', msg='This link has expired')


def validate_inputs(search_query, date, time, email, no_images):
   

    # This Function is responsible for validating the inputs given by the user
  
    try:
        # Checking if the queries passed are empty
        if search_query != '' and date != '' and time != '' and email != '' and no_images != '':

            no_images = int(no_images)  # Converting into integer for further processing
            # Number of images should be in between 1 and 500
            if 1 <= no_images <= 500:
                # Validating the email address
                if re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                    return True, None
                else:
                    logger_ins.print_log('(main.py (validate_inputs)) - Something went wrong. Email address is invalid',
                                         'exception')
                    return False, 'Invalid email address'
            else:
                logger_ins.print_log('(main.py (validate_inputs)) - Something went wrong. No of images must be in '
                                     'between 1 and 500',
                                     'exception')
                return False, 'No of images must be in between 1 and 500'
        else:
            logger_ins.print_log('(main.py (validate_inputs)) - Something went wrong. One of the inputs is empty',
                                 'exception')
            return False, 'One of inputs is empty'

    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    ade.debug = True
    ade.run()
