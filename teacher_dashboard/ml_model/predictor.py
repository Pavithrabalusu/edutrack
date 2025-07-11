import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edupredict.settings")
django.setup()

from django.conf import settings
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

class StudentPerformancePredictor:
    def __init__(self):
        self.model_path = os.path.join(settings.BASE_DIR, 'teacher_dashboard', 'ml_model', 'performance_model.joblib')
        self.scaler_path = os.path.join(settings.BASE_DIR, 'teacher_dashboard', 'ml_model', 'scaler.joblib')
        self.columns_path = os.path.join(settings.BASE_DIR, 'teacher_dashboard', 'ml_model', 'columns.joblib')
        self.data_path = os.path.join(settings.BASE_DIR, 'teacher_dashboard', 'ml_model', 'student-mat.csv')
        self.all_columns = None
        self.load_model()

    def load_model(self):
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.all_columns = joblib.load(self.columns_path)
        except:
            self.train_model()

    def preprocess_data(self, df, training=True):
        df = df.copy()

        if training:
            # Create performance label from G3
            conditions = [
                (df['G3'] >= 16),
                (df['G3'] >= 12),
                (df['G3'] >= 8),
                (df['G3'] >= 0)
            ]
            choices = ['Excellent', 'Good', 'Average', 'Poor']
            df['performance'] = np.select(conditions, choices, default='Unknown')

        numeric_features = [
            'age', 'Medu', 'Fedu', 'traveltime', 'studytime',
            'failures', 'famrel', 'freetime', 'goout', 'Dalc',
            'Walc', 'health', 'absences', 'G1', 'G2'
        ]

        categorical_cols = [
            'school', 'sex', 'address', 'famsize', 'Pstatus',
            'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup',
            'famsup', 'paid', 'activities', 'nursery', 'higher',
            'internet', 'romantic'
        ]

        # Fill missing categorical cols
        for col in categorical_cols:
            if col not in df.columns:
                df[col] = 'unknown'

        df = pd.get_dummies(df, columns=categorical_cols)

        if training:
            # Save the columns used during training (excluding target)
            self.all_columns = df.drop(columns=['performance']).columns.tolist()
            joblib.dump(self.all_columns, self.columns_path)

            X = df[self.all_columns]
            y = df['performance']
        else:
            # For prediction, ensure all training columns are present
            for col in self.all_columns:
                if col not in df.columns:
                    df[col] = 0  # fill missing cols
            df = df[self.all_columns]
            X = df
            y = None

        return X, y

    def train_model(self):
        df = pd.read_csv(self.data_path, sep=';')
        X, y = self.preprocess_data(df, training=True)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        self.model.fit(X_train_scaled, y_train)

        y_pred = self.model.predict(X_test_scaled)
        print(classification_report(y_test, y_pred))

        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

    def predict_performance(self, student_data):
        try:
            df = pd.DataFrame([student_data])
            X, _ = self.preprocess_data(df, training=False)
            X_scaled = self.scaler.transform(X)
            prediction = self.model.predict(X_scaled)
            return prediction[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Average"  # default fallback

# For standalone testing
if __name__ == "__main__":
    test_data = {
        'age': 17, 'Medu': 2, 'Fedu': 2, 'traveltime': 1, 'studytime': 2,
        'failures': 0, 'famrel': 4, 'freetime': 3, 'goout': 3, 'Dalc': 1,
        'Walc': 1, 'health': 4, 'absences': 4, 'G1': 14, 'G2': 15, 'G3': 15,
        'school': 'GP', 'sex': 'F', 'address': 'U', 'famsize': 'GT3', 'Pstatus': 'T',
        'Mjob': 'teacher', 'Fjob': 'services', 'reason': 'course', 'guardian': 'mother',
        'schoolsup': 'yes', 'famsup': 'no', 'paid': 'yes', 'activities': 'no',
        'nursery': 'yes', 'higher': 'yes', 'internet': 'yes', 'romantic': 'no'
    }

    predictor = StudentPerformancePredictor()
    result = predictor.predict_performance(test_data)
    print("Prediction:", result)
