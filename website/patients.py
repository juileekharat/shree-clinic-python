from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_login import current_user
from .models import Patient
from datetime import datetime
from . import db 
import json

patients = Blueprint('patients', __name__)

@patients.route('/patients', methods=['POST', 'GET'])
def display_patients(): 
    patients = Patient.query.all()
    return render_template("patients/patients.html", user=current_user, data=patients)

@patients.route('/add_patient_redirect')
def add_patient_redirect():
    return render_template("patients/add_patients.html", user=current_user)

@patients.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == "POST":
        name = request.form.get('name')
        age = request.form.get('age')
        bloodGroup = request.form.get('bloodGroup')
        treatment = request.form.get('treatment')
        patientSince = request.form.get('patientSince')
        history = request.form.get('history')

        patientSinceDate = None
        if patientSince:
            patientSinceDate = datetime.strptime(patientSince, '%Y-%m-%d').date()

        if len(name) == 0:
            flash('Please enter Name', category='error')
        elif not age.isnumeric():
            flash("Age must be a number", category='error')
        elif len(treatment) == 0:
            flash("Please enter Treatment", category='error')
        else:
            new_patient = Patient(name=name, age=age, blood_group=bloodGroup, treatment=treatment, patient_since=patientSinceDate, history=history)
            db.session.add(new_patient)
            db.session.commit()
            flash('Patient Added', category='success')
            return redirect(url_for('patients.display_patients'))
    return render_template("patients/patients.html", user=current_user)
    
@patients.route('/fetch_patient', methods=['GET'])
def fetch_patient():
    patientId = request.args.get('id')
    patient = Patient.query.get(patientId)
    #patient = Patient.query.filter_by(id=patientId).all()
    return render_template("patients/edit_patients.html", user=current_user, data=patient)
 
@patients.route('/get-patient', methods=['POST', 'GET'])
def get_patient():
    patient = ""
    args = []
    id = request.form.get('id')
    args.append(Patient.id.like('%%%s%%' % id))
    patient = Patient.query.filter(*args).all()
    if patient:
        pass
    else:
        flash('Patient does not exist', category='error')     
    return render_template("patients/patients.html", user=current_user, data=patient)

@patients.route('/edit_patient', methods=['POST'])
def edit_patient():
    if request.method == 'POST':
        id = request.form.get('id')
        patient = Patient.query.filter_by(id=id).first()
        if patient:
            name = request.form.get('name')
            age = request.form.get('age')
            bloodGroup = request.form.get('bloodGroup')
            treatment = request.form.get('treatment')
            patientSince = request.form.get('patientSince')
            history = request.form.get('history')

            patientSinceDate = None
            if patientSince:
                patientSinceDate = datetime.strptime(patientSince, '%Y-%m-%d').date()

            if len(name) == 0:
                flash('Please enter Name', category='error')
            elif not age.isnumeric():
                flash("Age must be a number", category='error')
            elif len(treatment) == 0:
                flash("Please enter Treatment", category='error')
            else:
                patient.name = name
                patient.age = age
                patient.blood_group = bloodGroup
                patient.treatment = treatment
                patient.patient_since = patientSinceDate
                patient.history = history
                db.session.commit()

                flash('Patient Modified', category='success')
                return redirect(url_for('patients.display_patients'))

    return render_template("patients/patients.html", user=current_user)

@patients.route('/delete_Patient', methods=['POST'])
def delete_Patient():
    data = json.loads(request.data)
    patientId = data['patientId']
    patient = Patient.query.get(patientId)
    if patient:
            db.session.delete(patient)
            db.session.commit()
            flash('Patient Deleted', category='success')
    return jsonify({})

# @patients.route('/fetch_patient', methods=['POST'])
# def fetch_patient():
#     try:
#         data = json.loads(request.data)
#         print(data)
#         patientId = data['patientId']
#         patient = Patient.query.get(patientId)
#         #patient = Patient.query.filter_by(id=patientId).all()
#         data = {'id': patient.id,
#                 'name': patient.name,
#                 'age': patient.age,
#                 'bloodGroup': patient.blood_group,
#                 'treatment': patient.treatment,
#                 'patientSince': patient.patient_since,
#                 'history': patient.history }
#         return jsonify(data), 200 , ({'ContentType':'application/json'}) 
#     except Exception as e:
#             print(e)  
#             # Now you can see what the real issue is...
#             return json.dumps({'success':True}), 200, ({'ContentType':'application/json'})







