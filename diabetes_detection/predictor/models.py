from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Patient(models.Model):
    # Informations du patient
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)], verbose_name="Âge")

    # Features pour la prédiction
    pregnancies = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Nombre de grossesses",
        help_text="Nombre de fois enceinte"
    )
    glucose = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        verbose_name="Glucose",
        help_text="Concentration de glucose plasmatique (mg/dL)"
    )
    blood_pressure = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        verbose_name="Pression artérielle",
        help_text="Pression artérielle diastolique (mm Hg)"
    )
    skin_thickness = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Épaisseur de la peau",
        help_text="Épaisseur du pli cutané du triceps (mm)"
    )
    insulin = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(900)],
        verbose_name="Insuline",
        help_text="Insuline sérique à 2 heures (mu U/ml)"
    )
    bmi = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(70)],
        verbose_name="IMC",
        help_text="Indice de masse corporelle (poids en kg/(taille en m)^2)"
    )
    diabetes_pedigree = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        verbose_name="Fonction de pedigree",
        help_text="Fonction de pedigree du diabète"
    )

    # Résultats de la prédiction
    prediction = models.BooleanField(default=False, verbose_name="Prédiction diabète")
    probability = models.FloatField(default=0.0, verbose_name="Probabilité (%)")

    # Métadonnées
    date_prediction = models.DateTimeField(auto_now_add=True, verbose_name="Date de prédiction")

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-date_prediction']

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.date_prediction.strftime('%d/%m/%Y')}"

    def get_risk_level(self):
        """Retourne le niveau de risque basé sur la probabilité"""
        if self.probability < 30:
            return "Faible"
        elif self.probability < 60:
            return "Modéré"
        else:
            return "Élevé"

    def get_risk_color(self):
        """Retourne la couleur associée au risque"""
        if self.probability < 30:
            return "success"
        elif self.probability < 60:
            return "warning"
        else:
            return "danger"