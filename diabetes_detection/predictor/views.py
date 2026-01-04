from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Patient
from .forms import PatientForm
import joblib
import numpy as np
import os

# Charger le modèle, le scaler et les features au démarrage
try:
    model = joblib.load(settings.MODEL_PATH)
    scaler = joblib.load(settings.SCALER_PATH)
    feature_names = joblib.load(settings.FEATURES_PATH)
    print("Modèle chargé avec succès!")
except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
    model = None
    scaler = None
    feature_names = None


def index(request):
    """Page d'accueil"""
    recent_predictions = Patient.objects.all()[:5]

    # Statistiques
    total_patients = Patient.objects.count()
    diabetic_count = Patient.objects.filter(prediction=True).count()
    non_diabetic_count = Patient.objects.filter(prediction=False).count()

    context = {
        'recent_predictions': recent_predictions,
        'total_patients': total_patients,
        'diabetic_count': diabetic_count,
        'non_diabetic_count': non_diabetic_count,
    }
    return render(request, 'predictor/index.html', context)


def predict(request):
    """Page de prédiction avec formulaire"""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            if model is None:
                messages.error(request, "Erreur: Le modèle n'est pas chargé.")
                return render(request, 'predictor/predict.html', {'form': form})

            # Sauvegarder le patient sans commit
            patient = form.save(commit=False)

            # Préparer les données pour la prédiction
            features = np.array([[
                patient.pregnancies,
                patient.glucose,
                patient.blood_pressure,
                patient.skin_thickness,
                patient.insulin,
                patient.bmi,
                patient.diabetes_pedigree,
                patient.age  # Utilisé à la place de Age dans le dataset
            ]])

            # Standardiser les features
            features_scaled = scaler.transform(features)

            # Faire la prédiction
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0]

            # Sauvegarder les résultats
            patient.prediction = bool(prediction)
            patient.probability = round(probability[1] * 100, 2)
            patient.save()

            messages.success(request, 'Prédiction effectuée avec succès!')
            return redirect('result', patient_id=patient.id)
    else:
        form = PatientForm()

    return render(request, 'predictor/predict.html', {'form': form})


def result(request, patient_id):
    """Page de résultats de prédiction"""
    patient = get_object_or_404(Patient, id=patient_id)

    context = {
        'patient': patient,
    }
    return render(request, 'predictor/result.html', context)


def history(request):
    """Historique de toutes les prédictions"""
    patients = Patient.objects.all()

    context = {
        'patients': patients,
    }
    return render(request, 'predictor/history.html', context)


def delete_patient(request, patient_id):
    """Supprimer un patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    messages.success(request, 'Patient supprimé avec succès!')
    return redirect('history')