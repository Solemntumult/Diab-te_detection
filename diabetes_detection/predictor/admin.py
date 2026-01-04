from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        'nom', 'prenom', 'age', 'prediction',
        'probability', 'get_risk_level', 'date_prediction'
    ]
    list_filter = ['prediction', 'date_prediction']
    search_fields = ['nom', 'prenom']
    readonly_fields = ['prediction', 'probability', 'date_prediction']

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'age')
        }),
        ('Données médicales', {
            'fields': (
                'pregnancies', 'glucose', 'blood_pressure',
                'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree'
            )
        }),
        ('Résultats de la prédiction', {
            'fields': ('prediction', 'probability', 'date_prediction')
        }),
    )

    def get_risk_level(self, obj):
        return obj.get_risk_level()

    get_risk_level.short_description = 'Niveau de risque'