# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/19 11:12
# @IDE:         PyCharm

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %matplotlib inline

# 读取文件
data = pd.read_csv("creditcard.csv")
# print(data.head())

# 查看样本分布
count_classes = pd.value_counts(data['Class'], sort = True).sort_index()
count_classes.plot(kind = 'bar')
plt.title("Fraud class histogram")
plt.xlabel("Class")
plt.ylabel("Frequency")
# plt.show()

from sklearn.preprocessing import StandardScaler

# 样本转换
data['normAmount'] = StandardScaler().fit_transform(data['Amount'].values.reshape(-1, 1))
data = data.drop(['Time','Amount'],axis=1)
# print(data.head())

# 下采样策略
X = data.iloc[:, data.columns != 'Class']
y = data.iloc[:, data.columns == 'Class']

# Number of data points in the minority class
# 取出class=1的index
number_records_fraud = len(data[data.Class == 1])
fraud_indices = np.array(data[data.Class == 1].index)

# Picking the indices of the normal classes
# 取出class=0的index
normal_indices = data[data.Class == 0].index

# Out of the indices we picked, randomly select "x" number (number_records_fraud)
# 随机选择样本
random_normal_indices = np.random.choice(normal_indices, number_records_fraud, replace = False)
random_normal_indices = np.array(random_normal_indices)

# Appending the 2 indices
# 拼接样本数据
under_sample_indices = np.concatenate([fraud_indices,random_normal_indices])

# Under sample dataset
# 展示结果
under_sample_data = data.iloc[under_sample_indices,:]

X_undersample = under_sample_data.iloc[:, under_sample_data.columns != 'Class']
y_undersample = under_sample_data.iloc[:, under_sample_data.columns == 'Class']

# Showing ratio
# print("Percentage of normal transactions: ", len(under_sample_data[under_sample_data.Class == 0])/len(under_sample_data))
# print("Percentage of fraud transactions: ", len(under_sample_data[under_sample_data.Class == 1])/len(under_sample_data))
# print("Total number of transactions in resampled data: ", len(under_sample_data))

from sklearn.model_selection import train_test_split

# Whole dataset
# 交叉验证
# 随机切分
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state = 0)
# 切分结果
# print("Number transactions train dataset: ", len(X_train))
# print("Number transactions test dataset: ", len(X_test))
# print("Total number of transactions: ", len(X_train)+len(X_test))

# Undersampled dataset
# 下采样策略
# 随机切分
X_train_undersample, X_test_undersample, y_train_undersample, y_test_undersample = train_test_split(X_undersample
                                                                                                   ,y_undersample
                                                                                                   ,test_size = 0.3
                                                                                                   ,random_state = 0)
# 切分结果
# print("")
# print("Number transactions train dataset: ", len(X_train_undersample))
# print("Number transactions test dataset: ", len(X_test_undersample))
# print("Total number of transactions: ", len(X_train_undersample)+len(X_test_undersample))

#Recall = TP/(TP+FN)    模型评估方法
# 逻辑回归
from sklearn.linear_model import LogisticRegression
# cross_validation替换成model_selection
# KFold=几倍的交叉验证
# cross_val_score=交叉验证评估结果
from sklearn.model_selection import KFold, cross_val_score
# confusion_matrix=混淆矩阵
from sklearn.metrics import confusion_matrix,recall_score,classification_report


def printing_Kfold_scores(x_train_data, y_train_data):
    # print(len(y_train_data))
    fold = KFold(5, shuffle=False)

    # Different C parameters 惩罚力度
    c_param_range = [0.01, 0.1, 1, 10, 100]

    results_table = pd.DataFrame(index=range(len(c_param_range), 2), columns=['C_parameter', 'Mean recall score'])
    results_table['C_parameter'] = c_param_range

    # the k-fold will give 2 lists: train_indices = indices[0], test_indices = indices[1]
    j = 0
    # 选择每个C参数
    for c_param in c_param_range:
        print('-------------------------------------------')
        print('C parameter: ', c_param)
        print('-------------------------------------------')
        print('')

        recall_accs = []
        # 选择交叉验证的组
        for iteration, indices in enumerate(fold.split(x_train_data)):
            # Call the logistic regression model with a certain C parameter
            # 逻辑回归，实例化模型
            # 新版本需指定solver参数值，并将max_iter调大
            lr = LogisticRegression(C=c_param, penalty='l1',solver='liblinear',max_iter = 10000)

            # Use the training data to fit the model. In this case, we use the portion of the fold to train the model
            # with indices[0]. We then predict on the portion assigned as the 'test cross validation' with indices[1]
            # 模型训练.fit
            lr.fit(x_train_data.iloc[indices[0], :], y_train_data.iloc[indices[0], :].values.ravel())

            # Predict values using the test indices in the training data
            # 进行预测.predict
            y_pred_undersample = lr.predict(x_train_data.iloc[indices[1], :].values)

            # Calculate the recall score and append it to a list for recall scores representing the current c_parameter
            # 交叉验证
            recall_acc = recall_score(y_train_data.iloc[indices[1], :].values, y_pred_undersample)
            recall_accs.append(recall_acc)
            print('Iteration ', iteration, ': recall score = ', recall_acc)

        # The mean value of those recall scores is the metric we want to save and get hold of.
        results_table.loc[j, 'Mean recall score'] = np.mean(recall_accs)
        j += 1
        print('')
        print('Mean recall score ', np.mean(recall_accs))
        print('')
    # print(results_table['Mean recall score'].dtype)
    # 新版本ix改用iloc，且idxmaix前要加astype
    best_c = results_table.loc[results_table['Mean recall score'].astype(float).idxmax()]['C_parameter']

    # Finally, we can check which C parameter is the best amongst the chosen.
    print('*********************************************************************************')
    print('Best model to choose from cross validation is with C parameter = ', best_c)
    print('*********************************************************************************')

    return best_c

best_c = printing_Kfold_scores(X_train_undersample,y_train_undersample)

def plot_confusion_matrix(cm, classes,
                          title='Confusion matrix',
                          cmap=plt.cm.get_cmap("Blues")):
    """
    This function prints and plots the confusion matrix.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

import itertools
lr = LogisticRegression(C = best_c, penalty = 'l1',solver='liblinear')
lr.fit(X_train_undersample,y_train_undersample.values.ravel())
y_pred_undersample = lr.predict(X_test_undersample.values)

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test_undersample,y_pred_undersample)
np.set_printoptions(precision=2)

print("Recall metric in the testing dataset: ", cnf_matrix[1,1]/(cnf_matrix[1,0]+cnf_matrix[1,1]))

# Plot non-normalized confusion matrix
class_names = [0,1]
plt.figure()
plot_confusion_matrix(cnf_matrix
                      , classes=class_names
                      , title='Confusion matrix')
plt.show()