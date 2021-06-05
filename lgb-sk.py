import lightgbm as lgb
from lightgbm import LGBMRegressor, LGBMClassifier
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import numpy as np
import joblib
import pandas as pd
import sys

file_path = "./@new.csv"
file = pd.read_csv(file_path, )
file.drop_duplicates()
data_feature = file.iloc[1:, 0:352]
data_label = file.iloc[1:, 352]
# x_train, x_test, y_train, y_test = train_test_split(data_feature, data_label, test_size=0.2)  # 按照8:2划分训练集和测试集
# def mul_train():
#     """
#     多分类任务训练器，采用了相关的参数调优
#     :return: 训练完成的多分类机器学习对象
#     """
#     # Best parameters found by grid search are: {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 100,
#     # 'num_leaves': 40}
#     gbm = LGBMClassifier(boosting_type='gbdt', objective='multiclass', num_class=7, metric='multi_logloss',
#                          learning_rate=0.01, num_leaves=40,
#                          n_estimators=100, max_depth=3,
#                          bagging_fraction=0.7, feature_fraction=0.8, reg_lambda=0.2,
#                          )
#     gbm.fit(data_feature, data_label, eval_set=[(x_test, y_test)], early_stopping_rounds=5)
#     return gbm


# def bin_train():
#     """
#     二分类训练器，采用了调优后的参数
#     :return: 训练完成的二分类机器学习对象
#     """
#     # Best parameters found by grid search are: {'learning_rate': 0.2, 'max_depth': 7, 'n_estimators': 80, 'num_leaves': 40}
#     gbm = LGBMClassifier(boosting_type='gbdt', objective='binary',
#                          num_leaves=40,
#                          learning_rate=0.2,
#                          n_estimators=80, max_depth=7,
#                          bagging_fraction=0.9, feature_fraction=0.9, reg_lambda=0.2,
#                          )
#     gbm.fit(x_train, y_train, eval_set=[(x_test, y_test)], eval_metric='l1', early_stopping_rounds=5)
#     return gbm
### 以上函数用于训练，之后保存pkl文件即可。此处仅做展示说明。

# 模型加载
if sys.argv[1] == '0':
    gbm = joblib.load('./loan_model_binary.pkl')
else:
    gbm = joblib.load('./loan_model_multi.pkl')

# 模型预测
data_pred = gbm.predict(data_feature, num_iteration=gbm.best_iteration_)
print(confusion_matrix(data_label, data_pred, ))
print(classification_report(data_label, data_pred, ))

# 特征重要度
feature = zip(gbm.feature_name_, gbm.feature_importances_)
feature = sorted(feature, key=lambda x: x[1], reverse=True)
cnt = 0
for (k, v) in feature:
    print((k, v))
    cnt += 1
    if cnt > 20:
        break

# print('Feature importances:', list(gbm.feature_name_))
# print('Feature importances:', list(gbm.feature_importances_))
#
# # 网格搜索，参数优化
estimator = LGBMClassifier(boosting_type='gbdt', objective='binary', reg_lambda=0.2, )

param_grid = {
    'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.15, 0.5, 1, 10],
    'n_estimators': [x for x in range(20, 101, 20)],
    'num_leaves': [x for x in range(50, 70, 5)],
    'max_depth': [3, 5, 7, 9, 10],
    'cat_smooth': [1, 10, 15, 20, 35]
}
gbm = GridSearchCV(estimator, param_grid, n_jobs=6)
gbm.fit(x_train, y_train)
print("Best score: %0.3f" % gbm.best_score_)
print('Best parameters found by grid search are:', gbm.best_params_)