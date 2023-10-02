import numpy as np
import pandas as pd

from mathtext.models.digital_ocean_storage import upload_to_object_storage
from mathtext.models.encoders import BERTEncoder
from mathtext.constants import DATA_DIR

from sklearn.svm import SVC

np.random.seed(42)

enc = BERTEncoder()
svc_is_correct = SVC(class_weight="balanced", probability=True)

df = pd.read_csv(DATA_DIR / "annotated_data - answer_correct - modified.csv")
feature_columns = "question expected_answer student_answer".split()

Xs = [enc.transform(df[c]) for c in feature_columns]
y = df["human_judgement"]

# X = np.concatenate(Xs)
X = np.concatenate(Xs, axis=1)

is_test = np.random.rand(len(y)) > 0.9
is_train = ~is_test
X_train = X[is_train]
X_test = X[is_test]
y_test = y[is_test]
y_train = y[is_train]

# svc_is_correct.fit(X, y)
# svc_is_correct.score(X, y)
svc_is_correct.fit(X_train, y_train)
print(svc_is_correct.score(X_test, y_test))
print(svc_is_correct.score(X_train, y_train))
svc_is_correct.predict_proba(X)
svc_is_correct.predict(X)


results_answer_is_correct = pd.DataFrame()
results_answer_is_correct["nlu_prediction"] = svc_is_correct.predict(X)
results_answer_is_correct[
    [
        "predict_student_ans_incorrect_confidence",
        "predict_student_ans_correct_confidence",
    ]
] = svc_is_correct.predict_proba(X)
results_answer_is_correct
print(results_answer_is_correct.head().T)

results_answer_is_correct.to_csv("results_predict_correctness.csv")
