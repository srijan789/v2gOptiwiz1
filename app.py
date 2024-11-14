from flask import Flask, render_template, request
import datetime
import pickle
import pandas as pd

# create a simple flask app

app = Flask(__name__, template_folder='templates')



model = pickle.load(open('model.pkl', 'rb'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    
    elif request.method == 'POST':
        
        # get the data from the POST request
        timestamp = request.form['date']
        powerLevelStart = request.form['powerLevelStart']
        batteryCapacity = request.form['batteryCapacity']
        chargerType = request.form['chargerType']
        chargingPower = request.form['chargingPower']
        temerature = request.form['temperature']
        
        # parse the timestamp to get day of week and hour of day
        timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M')
        day_of_week = timestamp.weekday()
        hour_of_day = timestamp.hour

        # determine if the day is a workday
        is_workday = 1 if day_of_week < 5 else 0

        # create the dataframe row
        data = pd.DataFrame({
            'day_of_week': [day_of_week],
            'hour_of_day': [hour_of_day],
            'battery_level_start': [float(powerLevelStart)],
            'battery_capacity': [float(batteryCapacity)],
            'charging_power': [float(chargingPower)],
            'is_workday': [is_workday],
            'temperature': [float(temerature)],
            'parking_type_Airport': [1 if chargerType == 'Airport' else 0],
            'parking_type_city parking lot': [1 if chargerType == 'city parking lot' else 0],
            'parking_type_mini charging station': [1 if chargerType == 'mini charging station' else 0],
            'parking_type_office space': [1 if chargerType == 'office space' else 0]
        })
        
        
        
        
        
        
        # make a prediction
        prediction = model.predict(data)
        
        # get the output
        output = prediction[0]
        
        
        # convert output to a string with 2 decimal places
        output = '{:.2f}'.format(output)
        
        return render_template('result.html', output=output)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')