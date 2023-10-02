import numpy as np
import pandas as pd

from mathtext.models.digital_ocean_storage import upload_to_object_storage
from mathtext.models.encoders import BERTEncoder
from mathtext.constants import DATA_DIR

from sklearn.svm import SVC

np.random.seed(42)
# ANNOTATED_QUESTION_ANSWERS = DATA_DIR / "annotated_data - wholeset_annotated - modified.csv"
ANNOTATED_QUESTION_ANSWERS = DATA_DIR / "annotated_data - wholeset_annotated.csv"


df = pd.read_csv(ANNOTATED_QUESTION_ANSWERS)

feature_columns = "question expected_answer text".split()

enc = BERTEncoder()

y = df["actual_type"]
X_question = enc.transform(df[feature_columns[0]])
X_expected_answer = enc.transform(df[feature_columns[1]])
X_text = enc.transform(df[feature_columns[2]])

X = np.concatenate([X_question, X_text, X_expected_answer], axis=1)
is_test = np.random.rand(len(y)) > 0.9
is_train = ~is_test
X_train = X[is_train]
X_test = X[is_test]
y_test = y[is_test]
y_train = y[is_train]

svc = SVC(class_weight="balanced", probability=True)
svc.fit(X_train, y_train)
print(svc.score(X_test, y_test))
print(svc.score(X_train, y_train))
svc.predict_proba(X)
svc.predict(X)

results = pd.DataFrame()
results["is_testset_example"] = is_test
results["nlu_prediction"] = svc.predict(X)
results[["predict_answer_confidence", "predict_intent_confidence"]] = svc.predict_proba(
    X
)
print(results.head().T)


results.to_csv("results_predict_answer_or_intent.csv")
