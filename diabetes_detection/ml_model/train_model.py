import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le dataset (Pima Indians Diabetes Database)
# Téléchargez depuis: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
df = pd.read_csv('ml_model/diabetes.csv')

print("=== APERÇU DES DONNÉES ===")
print(df.head())
print(f"\nNombre de patients: {len(df)}")
print(f"\nDistribution des classes:\n{df['Outcome'].value_counts()}")

# Analyse des données
print("\n=== STATISTIQUES DESCRIPTIVES ===")
print(df.describe())

# Vérifier les valeurs manquantes
print(f"\nValeurs manquantes:\n{df.isnull().sum()}")

# Remplacer les zéros par NaN pour certaines colonnes (car biologiquement impossibles)
cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)

# Imputation par la médiane
for col in cols_with_zeros:
    df[col].fillna(df[col].median(), inplace=True)

# Séparer les features et la target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Standardisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entraînement du modèle Random Forest
print("\n=== ENTRAÎNEMENT DU MODÈLE ===")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train_scaled, y_train)

# Prédictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

# Évaluation
print("\n=== MÉTRIQUES DE PERFORMANCE ===")
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print(f"\nMatrice de confusion:\n{cm}")

# Importance des features
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print(f"\n=== IMPORTANCE DES FEATURES ===\n{feature_importance}")

# Visualisation de la matrice de confusion
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Matrice de Confusion')
plt.ylabel('Vraie Classe')
plt.xlabel('Classe Prédite')
plt.savefig('confusion_matrix.png')
print("\nMatrice de confusion sauvegardée: confusion_matrix.png")

# Visualisation de l'importance des features
plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance, x='importance', y='feature')
plt.title('Importance des Features')
plt.tight_layout()
plt.savefig('feature_importance.png')
print("Importance des features sauvegardée: feature_importance.png")

# Sauvegarder le modèle et le scaler
joblib.dump(model, 'diabetes_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("\n=== MODÈLE SAUVEGARDÉ ===")
print("Fichiers créés: diabetes_model.pkl, scaler.pkl")

# Sauvegarder les noms des features
feature_names = X.columns.tolist()
joblib.dump(feature_names, 'feature_names.pkl')
print("Noms des features sauvegardés: feature_names.pkl")