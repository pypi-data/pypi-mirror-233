#!/usr/bin/env python
# coding: utf-8
"""  Create multilabel intent recognition model from a dataset of labeled messages/utterances.

Datasets are stored in mathtext/data/ as CSVs.
To train a model your application, run the following:

from mathtext.models.multilabel_intent_recognition import run_multilabel_model_development_process
run_multilabel_model_development_process()
"""
from mathtext.models.encoders import BERTEncoder
from mathtext.constants import DATA_DIR
import pandas as pd

ANNOTATED_QUESTION_ANSWERS = DATA_DIR / 'annotated_data - wholeset_annotated.csv'

df = pd.read_csv(ANNOTATED_QUESTION_ANSWERS)
