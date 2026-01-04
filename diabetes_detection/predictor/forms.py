from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'nom', 'prenom', 'age',
            'pregnancies', 'glucose', 'blood_pressure',
            'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Âge du patient',
                'min': '1',
                'max': '120'
            }),
            'pregnancies': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2',
                'min': '0',
                'max': '20',
                'step': '1'
            }),
            'glucose': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 120 mg/dL',
                'min': '0',
                'max': '300',
                'step': '0.1'
            }),
            'blood_pressure': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 80 mm Hg',
                'min': '0',
                'max': '200',
                'step': '0.1'
            }),
            'skin_thickness': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 20 mm',
                'min': '0',
                'max': '100',
                'step': '0.1'
            }),
            'insulin': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 80 mu U/ml',
                'min': '0',
                'max': '900',
                'step': '0.1'
            }),
            'bmi': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 25.5',
                'min': '0',
                'max': '70',
                'step': '0.1'
            }),
            'diabetes_pedigree': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 0.5',
                'min': '0',
                'max': '3',
                'step': '0.001'
            }),
        }