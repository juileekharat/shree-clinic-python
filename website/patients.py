from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, Response
from flask_login import current_user
from .models import Patient, Documents
from datetime import datetime
from flask_sqlalchemy import pagination
from werkzeug.utils import secure_filename
from . import db 
import json
import os

patients = Blueprint('patients', __name__)

@patients.route('/patients', methods=['POST', 'GET'])
def display_patients(): 
    page = request.args.get('page', 1, type=int)
    patients = Patient.query.filter_by().paginate(page=page, per_page=10)
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

    action = request.args.get('action')
    if action == 'edit':
        return render_template("patients/edit_patients.html", user=current_user, data=patient)
    
    return render_template("patients/upload_documents.html", user=current_user, data=patient) 
 
@patients.route('/get-patient', methods=['POST', 'GET'])
def get_patient():
    page = request.args.get('page', 1, type=int)
    args = []
    id = request.form.get('id')
    args.append(Patient.id.like('%%%s%%' % id))
    patient = Patient.query.filter(*args).paginate(page=page, per_page=10)
    print(patient)
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
            #db.session.delete(patient)
            db.session.commit()
            flash('Patient Deleted', category='success')
    return jsonify({})

@patients.route('/upload_documents', methods=['POST'])
def upload_documents():
    id = request.form.get('id')
    documentFile = request.files['documentFile']
    displayDocument = "false"

    if not documentFile:
        flash('No file selected', category='error')
    else:
        fileName = secure_filename(documentFile.filename)
        mimeType = documentFile.mimetype
        documentCount = Documents.query.filter_by(document_name=fileName).count()
        if documentCount > 1:
            flash('Document already exists.', category='error')
        else:
            #Get File Size in KB
            blob = documentFile.read()
            documentSize = len(blob)/1000

            if documentSize > 500:
                flash('File size must be 500KB.', category='error')
            else:
                displayDocument = "true"
                document = Documents(image_buffer=documentFile.read(), mimetype=mimeType, document_name=fileName, patient_id=id)
                db.session.add(document)
                db.session.commit()
                flash('Document has been uploaded', category='success')
        
    patient = Patient.query.filter_by(id=id).first()

    return render_template("patients/upload_documents.html", user=current_user, data=patient, displayDocument=displayDocument)

@patients.route('/upload_documents/<int:id>', methods=['POST','GET'])
def view_document(id):
    document = Documents.query.filter_by(id=id).first()
    print(document)
    if not document:
        flash('Document does not exist', category='error')

    return Response(document.image_buffer, mimetype=document.mimetype)

