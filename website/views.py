from flask import Blueprint, redirect, render_template, request, flash, jsonify, session, url_for
import json, random, requests

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET','POST'])
def bank():
    if request.method == 'POST':
        s = request.form.get('state')
        if(len(s) <= 0):
            flash("Invalid State", category='error')
        else:
            return redirect(url_for("views.park", state=s))
    return render_template("welcome.html")

@views.route('/park/<state>', methods = ['GET', 'POST'])
def park(state):
    if(len(state) <= 0):
        flash("Invalid State",category='error')
        return redirect(url_for('views.bank'))

    api_url = "https://developer.nps.gov/api/v1/parks?stateCode="+state.upper()+"&api_key=uYogFAGOYuOtyghqxcH7VfJi8dam7OLUieLOJTkI"
    response = requests.get(api_url)
    data = response.json()
    if request.method == 'POST':
        code = request.form.get('id')
        return redirect(url_for('views.currentPark', code))
    if (int(data['total'])>0 and len(state)==2):
        return render_template("park.html", s = state, data = data, total = int(data['total']))
    else:
        flash("Invalid State",category='error')
        return redirect(url_for('views.bank'))
        
@views.route('/parkCode/<code>', methods = ['GET', 'POST'])
def currentPark(code):
    api_url = "https://developer.nps.gov/api/v1/parks?parkCode="+code+"&api_key=uYogFAGOYuOtyghqxcH7VfJi8dam7OLUieLOJTkI"
    api_url_things = "https://developer.nps.gov/api/v1/thingstodo?parkCode="+code+"&api_key=uYogFAGOYuOtyghqxcH7VfJi8dam7OLUieLOJTkI"
    response = requests.get(api_url)
    response2 = requests.get(api_url_things)
    thingstodo = response2.json()
    data = response.json()
    totalImage = data['data'][0]['images']
    operatinglength = len(data['data'][0]['operatingHours'][0]['description'])
    weatherlength = len(data['data'][0]['weatherInfo'].split())
    activities = data['data'][0]['activities']
    return render_template("currentPark.html", code = code, data = data, totalImage = len(totalImage), thingstodo=thingstodo, operatinglength=operatinglength, activities=activities,weatherlength=weatherlength)
 