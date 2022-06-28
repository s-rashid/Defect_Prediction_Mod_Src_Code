import argparse
import numpy as np
import csv as csv
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn import decomposition, datasets
from sklearn import tree
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True, type=str, help="Project name")
args = parser.parse_args()
project_name = args.name

max_depths = [2,4,6,8,12,20,30,50,80,100]

for max_depth in max_depths:

    count = 0
    tp_total = 0
    fp_total = 0
    fn_total = 0

    while(count < 6):
        dir_num = str(count)
        input_file_training = project_name + "/" + dir_num + "/train.csv"
        input_file_test = project_name + "/" + dir_num + "/test.csv"

        # load the training data as a matrix
        dataset = pd.read_csv(input_file_training, header=0)

        # separate the data from the target attributes
        train_data = dataset.drop('500_Buggy?', axis=1)

        # remove unnecessary features
        train_data = train_data.drop(['change_id', '411_commit_time', '412_full_path'], axis=1)

        # the lables of training data. `label` is the title of the  last column in your CSV files
        train_target = dataset[dataset.columns[-1]]

        # load the testing data
        dataset2 = pd.read_csv(input_file_test, header=0)

        # separate the data from the target attributes
        test_data = dataset2.drop('500_Buggy?', axis=1)

        # remove unnecessary features
        test_data = test_data.drop(['change_id', '411_commit_time', '412_full_path'], axis=1)

        # the lables of test data
        test_target = dataset2[dataset2.columns[-1]]

        decision_t = DecisionTreeClassifier(criterion = 'entropy', max_depth = max_depth)
        test_pred = decision_t.fit(train_data, train_target).predict(test_data)

        tn, fp, fn, tp = confusion_matrix(test_target, test_pred).ravel()
    
        tp_total = tp_total + tp
        fp_total = fp_total + fp
        fn_total = fn_total + fn
        count = count + 1


    precision = tp_total / (tp_total + fp_total)
    recall = tp_total / (tp_total + fn_total)
    f1 = (2 * precision * recall) / (precision + recall)
    print("f1-score for project " + project_name + " with max_depth: " + str(max_depth) + " is: " + str(f1))
