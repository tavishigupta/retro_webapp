"""
Routes and views for the flask application.
"""

from retro_webapp import app
from flask import request, render_template
from decimal import Decimal
import urllib2
import json
import os

# removes all new lines for correct input to trained model
def cleanAgenda(agenda):
    return agenda.replace('\n', ' ')

# return homepage for user input
@app.route("/")
def main():
    return render_template('homepage.html')

# return result page with prediction
@app.route('/prediction', methods=['POST','GET'])
def get_prediction():
    if request.method == 'POST':
        # instantiate all venue and audience inputs
        offices = stores = schools = premises = otherv = 0
        under5 = six = twelve = eighteen = over23 = industry = educators = government = othera = 0

        # extract all values from result
        result = request.form
        date = result['date']
        agenda = cleanAgenda(result['agenda'])
        length = result['length']

        # extract list of all venues and audiences
        venue = request.form.getlist('venue')
        audience = request.form.getlist('audience')

        # validate correct format of each value
        print(result)
        print(date)
        print(agenda)
        print(length)
        print(venue)
        print(audience)

        # true value for selcted venue on homepage
        if 'offices' in venue:
            offices = 1
        if 'stores' in venue:
            stores = 1
        if 'schools' in venue:
            schools = 1
        if 'premises' in venue:
            premises = 1
        if 'other' in venue:
            otherv = 1

        # true value for selcted audience on homepage
        if 'under5' in audience:
            under5 = 1
        if '6to11' in audience:
            six = 1
        if '12to17' in audience:
            twelve = 1
        if '18to22' in audience:
            eighteen = 1
        if '23Over' in audience:
            over23 = 1
        if 'industry' in audience:
            industry = 1
        if 'educators' in audience:
            educators = 1
        if 'government' in audience:
            government = 1
        if 'other' in audience:
            othera = 1

        # validate correct value for venue and audience input
        print(offices)
        print(stores)
        print(schools)
        print(premises)
        print(otherv)
        print(under5)
        print(six)
        print(twelve)
        print(eighteen)
        print(over23)
        print(industry)
        print(educators)
        print(government)
        print(othera)

        # input data in the correct JSON format
        data = {
            "Inputs": {
                "Input": {
                    "ColumnNames": ["Event Date", "Event Agenda", "Event Venue: Microsoft Office(s)", 
                                    "Event Venue: Microsoft Store(s)", "Event Venue: Partner Premises", 
                                    "Event Venue: School(s)", "Event Venue: Other", "Audience (Age): Under 5", 
                                    "Audience (Age): 6-11", "Audience (Age): 12-17", "Audience (Age): 18-22", 
                                    "Audience (Age): 23+", "Audience: Industry Representatives", "Audience: Educators", 
                                    "Audience: Government Representatives", "Audience: Other", "Event Length"],
                    "Values": [ [date, agenda, offices, stores, premises, schools, otherv, under5, six, twelve, 
                                eighteen, over23, industry, educators, government, othera, length ], ]
                },        
            }
        }

        # prepare values for request
        body = str.encode(json.dumps(data)) # JSON encoded string
        url = 'https://ussouthcentral.services.azureml.net/workspaces/9b6da4f58f7440efb562c248970511c5/services/e1218058ea3749b49a8513d858a06e69/execute?api-version=2.0&details=true'
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ os.environ['api_key'])}

        try:
            # get a response from request URL
            req = urllib2.Request(url, body, headers) 
            response = urllib2.urlopen(req)

            # convert the response to string format
            JSONprediction = json.loads(response.read())

            # extract the prediction value
            prediction = Decimal(JSONprediction['Results']['output']['value']['Values'][0][0])
            prediction = "{0:.0f}".format(prediction)
   
            return render_template('result.html', prediction = prediction)
        except urllib2.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read()))

            return render_template('result.html', prediction = 'error loading prediction')