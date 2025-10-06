import pandas as pd
import joblib
import os
df = pd.read_csv('src/data/simulated_transactions.csv')
print(df.head())
print(df['label'].value_counts())

#Preprocessing imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Separate features and target
X = df.drop('label', axis=1)
y = df['label']

# Define column types
numeric_features = ['amount', 'customer_age', 'account_age_days', 'num_prev_flags']
categorical_features = ['origin_country', 'destination_country', 'transaction_type', 'time_of_day']
binary_features = ['is_high_risk_country']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features),
        ('bin', 'passthrough', binary_features)
    ]
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline

# Define models to test
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Gradient Boosting': GradientBoostingClassifier(),
    'SVM': SVC(probability=True),
    'MLP': MLPClassifier(max_iter=500),
    'Dummy': DummyClassifier(strategy='most_frequent')
}

# Train and evaluate each model
results = []

for name, model in models.items():
    clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1] if hasattr(clf.named_steps['classifier'], 'predict_proba') else None

    result = {
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1 Score': f1_score(y_test, y_pred),
        'ROC AUC': roc_auc_score(y_test, y_proba) if y_proba is not None else 'N/A'
    }
    results.append(result)

# Display results
results_df = pd.DataFrame(results).sort_values(by='F1 Score', ascending=False)
print(results_df)

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Select best model by F1 Score
best_model_name = results_df.iloc[0]["Model"]
best_model = models[best_model_name]

# Rebuild pipeline with best model
best_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", best_model)])

# Fit on full training data
best_pipeline.fit(X_train, y_train)

# Save to models/best_model.pkl
joblib.dump(best_pipeline, "models/best_model.pkl")
print(f"✅ Saved best model: {best_model_name} to models/best_model.pkl")

