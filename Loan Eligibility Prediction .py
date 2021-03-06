#!/usr/bin/env python
# coding: utf-8

# # LOAN ELIGIBILITY PREDICTION 
# The aim of this work is towards helping the banks accurately determine, through an automation process, whether a customer can obtain a loan or not depending on the details provided by the customer while making the application. 

# In[1]:


#import the required modules

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import *
style.use("ggplot")
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import plot_confusion_matrix, f1_score, matthews_corrcoef

#The PolynomialFeatures will be used for feature creation to explore the nonlinear pattern of the numerical data.
from sklearn.preprocessing import PolynomialFeatures
#The Pipeline is used to package the feature creator and the classifier.
from sklearn.pipeline import Pipeline


# For feature creation
# Degree 2 is used here but one can set the degree to be a hyperparameter to further explore the accuracy of the model
poly = PolynomialFeatures(degree = 2)

#importing the classifiers
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron

#for combining multiple models into one 
from sklearn.ensemble import StackingClassifier


# In[2]:


#read the dataset 
#the data was saved on my computer, so you can edit the file path to suit you
#this could be a url

loan_train = pd.read_csv("/Users/apple/Documents/OPEN_UNIVERSITY/Data_for_DataScience/Loan-Eligibility-Prediction-Project/train.csv")
loan_test = pd.read_csv("/Users/apple/Documents/OPEN_UNIVERSITY/Data_for_DataScience/Loan-Eligibility-Prediction-Project/test.csv")


# In[3]:


#set what the datasets look like
print(loan_train.shape)
loan_train.head()


# In[4]:


print(loan_test.shape)
loan_test.head()


# In[5]:


# info about the datasets
print(loan_train.info())
print(loan_train.isnull().sum())


# In[6]:


print(loan_test.info())
print(loan_test.isnull().sum())


# #One would notice that the test.csv data does not contain the loan status column. The implication of this is that one would not be able to evaluate the accuracy of the models from the data. Hence, only the train.csv data would be used for this project.

# # Data Analysis 

# In[7]:


#Some analysis of the data is done to check the dependence of the feature variables to the label variable
plt.rcParams['figure.figsize'] = (10.0, 5.0)
fig, ax = plt.subplots(nrows = 1, ncols = 3)
sns.countplot(ax = ax[0], x = loan_train["Loan_Status"])
ax[0].set_title("Loan Status count")
sns.countplot(ax = ax[1], x = loan_train["Gender"])
ax[1].set_title("Gender count")
sns.countplot(ax = ax[2], x = loan_train["Self_Employed"])
ax[2].set_title("Self-employed count")


# In[8]:


#checking dependencies
plt.rcParams['figure.figsize'] = (15.0, 10.0)
fig, ax = plt.subplots(nrows = 2, ncols = 3)
sns.countplot(ax = ax[0,0], x = "Loan_Status", hue = "Married", data = loan_train)
#for minor ticks
ax[0,0].yaxis.set_minor_locator(MultipleLocator(10))
sns.countplot(ax = ax[0,1], x = "Loan_Status", hue = "Gender", data = loan_train)
ax[0,1].yaxis.set_minor_locator(MultipleLocator(10))
sns.countplot(ax = ax[0,2], x = "Loan_Status", hue = "Education", data = loan_train)
ax[0,2].yaxis.set_minor_locator(MultipleLocator(10))
sns.countplot(ax = ax[1,0], x = "Loan_Status", hue = "Property_Area", data = loan_train)
ax[1,0].yaxis.set_minor_locator(MultipleLocator(5))
sns.countplot(ax = ax[1,1], x = "Loan_Status", hue = "Dependents", data = loan_train)
ax[1,1].yaxis.set_minor_locator(MultipleLocator(10))
sns.countplot(ax = ax[1,2], x = "Loan_Status", hue = "Credit_History", data = loan_train)
ax[1,2].yaxis.set_minor_locator(MultipleLocator(10))
plt.show()


# From the charts above, 
# 
#   - about 59% of the unmarried people are not eligible to get a loan while only about 42% of the married people are eligible. Hence, one is more likely to get a loan if the person is married.
#   
#   - about 43% of the female gender was rejected loan while about 44% of the male gender was rejected loan. Hence, one can say that the loan eligibility does not necessarily depend on the person's gender.   
#   
#   - about 63% of the non-graduates are not eligible to get a loan while only about 41% of the graduates are eligible. Hence, a non-graduate is less likely to be eligible for a loan.
#   
#   - one is more likely to get a loan if the property is in a semiurban area giving that about 39%, 34% and 23% of the people whose properties are in the rural, urban and semiurban areas respectively are not eligible for a loan,
#   
#   - the number of people with or without dependent that are not eligible for a loan are as follows:  0: 45%, 1:35%, 2:26%, and 3+: 40%. Hence, one can say that a person is more likely to be eligible for a loan if he/she has 1 or 2 dependents. 
#  
#   - one is less likely to be eligible for a loan if they do not completely the requirements for the loan eligibility

# In[9]:


#The distribution of the applicant's income
plt.rcParams['figure.figsize'] = (15.0, 10.0)
figs, ax = plt.subplots(nrows = 2, ncols = 3)
loan_train['ApplicantIncome'].plot.hist(ax = ax[0,0], title = 'Applicant Income')
ax[0,0].yaxis.set_minor_locator(MultipleLocator(20))
ax[0,0].xaxis.set_minor_locator(MultipleLocator(5000))

loan_train['CoapplicantIncome'].plot.hist(ax = ax[0,1], title = 'Co-applicant Income')
ax[0,1].yaxis.set_minor_locator(MultipleLocator(20))
ax[0,1].xaxis.set_minor_locator(MultipleLocator(5000))


loan_train['LoanAmount'].plot.hist(ax = ax[0,2], title = 'Loan Amount')
ax[0,2].yaxis.set_minor_locator(MultipleLocator(10))
ax[0,2].xaxis.set_minor_locator(MultipleLocator(20))

loan_train['Loan_Amount_Term'].plot.hist(ax = ax[1,0], title = 'Loan Amount Term')
ax[1,0].yaxis.set_minor_locator(MultipleLocator(20))
ax[1,0].xaxis.set_minor_locator(MultipleLocator(20))

ax[1,1].scatter(loan_train['ApplicantIncome'], loan_train['Loan_Status'])
ax[1,1].set_title('Applicant Income')
ax[1,1].xaxis.set_minor_locator(MultipleLocator(2000))

ax[1,2].scatter( x = loan_train['CoapplicantIncome'], y = loan_train['Loan_Status'])
ax[1,2].set_title('Co-applicant Income')
ax[1,2].xaxis.set_minor_locator(MultipleLocator(2000))

plt.show()
print("   ")
print('Mean Applicant Income  = ', np.mean(loan_train['ApplicantIncome']))
print('Mean Co-applicant Income  = ', np.mean(loan_train['CoapplicantIncome']))
print('Mean Loan Amount  = ', np.mean(loan_train['LoanAmount']))
print('Mean Loan Amount Term  = ', np.mean(loan_train['Loan_Amount_Term']))


# # Data Wrangling

# In[10]:


#get rid of all the null values in the data

   #first the heat map for the null values
plt.rcParams['figure.figsize'] = (10.0, 10.0)
sns.heatmap(loan_train.isnull(), cmap="viridis")


# In[11]:


#now remove all the null values
loan_train.dropna(inplace = True)

#check the heatmap again
sns.heatmap(loan_train.isnull(), cmap="viridis", cbar = False)


# In[12]:


#or you can print out the isnull count
print(loan_train.isnull().sum())
print(loan_train.shape)


# # Data Preprocessing

# In[13]:


#the Loan_ID column is not needed, so it is dropped
loan_train.drop("Loan_ID", axis = 1, inplace = True)


# In[14]:


#encode the string values in the necessary column
encoder  = LabelEncoder()

#THE GENDER COLUMN: Female = 0, Male  = 1
loan_train["Gender"] = encoder.fit_transform(loan_train["Gender"])
loan_train = loan_train.rename(columns = {"Gender":"Male_Gender"})
loan_train["Male_Gender"].value_counts()


# In[15]:


#THE MARRIED COLUMN: Yes = 1, No = 0
loan_train["Married"] = encoder.fit_transform(loan_train["Married"])
loan_train["Married"].value_counts()


# In[16]:


#THE EDUCATION COLUMN: Graduate = 0, Not Graduate  = 1
loan_train["Education"] = encoder.fit_transform(loan_train["Education"])
loan_train = loan_train.rename(columns = {"Education":"Not_Graduate"})
loan_train["Not_Graduate"].value_counts()


# In[17]:


#THE SELF-ENPMPLOYED COLUMN: No = 1, Yes = 0
loan_train["Self_Employed"] = encoder.fit_transform(loan_train["Self_Employed"])
loan_train["Self_Employed"].value_counts()


# In[18]:


#THE SELF-ENPMPLOYED COLUMN: No = 0, Yes = 1
loan_train["Loan_Status"] = encoder.fit_transform(loan_train["Loan_Status"])
loan_train["Loan_Status"].value_counts()


# In[19]:


#THE PROPERTY AREA COLUMN
#This column has a multivalued. So, one can either use get_dummies or one-hot-encoder

property_area = pd.get_dummies(loan_train["Property_Area"], drop_first = True)
print(property_area.head())


# In[20]:


#THE DEPENDENT COLUMN: This is also multivalued
dependents_ = pd.get_dummies(loan_train["Dependents"])
print(dependents_.head())


# In[21]:


#one can then concatenate this with the main data
loan_train = pd.concat([loan_train, property_area, dependents_], axis = 1)

#drop the previous property area, dependents and the 3+ columns
loan_train.drop(["Property_Area", "Dependents", "3+" ], axis = 1, inplace = True)
loan_train = loan_train.rename(columns = {"0":"0_dependent", "1":"1_dependent", "2":"2_dependents"})
loan_train.head()


# # Data Splitting

# In[22]:


#split the data into features and labels
x = loan_train.drop(["Loan_Status"], axis = 1)
y = loan_train["Loan_Status"]

#split the data into training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(x,y, test_size = 0.25, random_state = 20)


# In[23]:


#scale the data due to large range of of the distribution
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# # Building the models

# In[24]:


#Keep all the classifiers in a list so that the testing and training can be done once and for all
#then one can choose the one with the best accuracy
classifiers_ = [
    ("AdaBoost", AdaBoostClassifier()),
    ("Decision Tree", DecisionTreeClassifier(max_depth=3)),
    ("Gaussian Process", GaussianProcessClassifier(1.0 * RBF(1.0))),
    ("Linear SVM", SVC(kernel="linear", C=1,probability=True)),
    ("Naive Bayes",GaussianNB()),
    ("Nearest Neighbors",KNeighborsClassifier(2)),
    ("Neural Net",MLPClassifier(alpha=1)),
    ("QDA", QuadraticDiscriminantAnalysis()),
    ("Random Forest",RandomForestClassifier(n_jobs=2, random_state=1)),
    ("RBF SVM",SVC(gamma=2, C=1,probability=True)),
    ("SGDClassifier", SGDClassifier(max_iter=1000, tol=10e-3,penalty='elasticnet')),
    ("LogisticRegression", LogisticRegression()), 
    ("Perceptron", Perceptron(tol=1e-3, random_state=0)), 
    ("BaggingClassifier", BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=0))
    ] 


# In[25]:


for n,clf in classifiers_:
    print("n = ",n, " and clf = ", clf)


# In[26]:


plt.rcParams['figure.figsize'] = (3.0, 3.0)
#use each Classifier to take its training results.
clf_names = []
train_accuracy_score = []
test_accuracy_score = []
predict_sums = []
test_f1score = []
train_f1score = []
test_matthews = []
train_matthews = []
i = 0

for n,clf in classifiers_:
    clf_names.append(n)
    
    # Model training
    clf.fit(X_train, y_train)
    print(i, ":",  n+" training done! \n ")
    
    # The prediction for both training and testing 
    clf.predict(X_test)
    clf.predict(X_train)
    predict_sums.append(clf.predict(X_test).sum()) 
        #you can print the classification report and confusion matrix if you like
    print(classification_report(y_test, clf.predict(X_test)))
    print(confusion_matrix(y_test, clf.predict(X_test)))
    
    #you can also plot the confussion matrix if you like
    disp1 = plot_confusion_matrix(clf, X_train, y_train,
                              display_labels=['YES','NO'],
                              cmap=plt.cm.Blues,
                              normalize=None)
    disp1.ax_.set_title('Confusion matrix')
    plt.show()
    
    disp = plot_confusion_matrix(clf, X_test, y_test,
                              display_labels=['YES','NO'],
                              cmap=plt.cm.Blues,
                              normalize=None)
    disp.ax_.set_title('Confusion matrix')
    plt.show()
    
    # Measure training accuracy and score
    train_accuracy_score.append(round(accuracy_score(y_train, clf.predict(X_train)), 3))
    train_matthews.append(round(matthews_corrcoef(y_train, clf.predict(X_train)),3))
    train_f1score.append(round(f1_score(y_train, clf.predict(X_train)),3))
    print("The Training Accuracy Score: ", accuracy_score(y_train, clf.predict(X_train)) )
    print("The Training F1 Score: ", f1_score(y_train, clf.predict(X_train)) )
    print("The Training Matthews coefficient: ", matthews_corrcoef(y_train, clf.predict(X_train)))
    print(n+" training score done!")
    
    # Measure test accuracy and score
    test_accuracy_score.append(round(accuracy_score(y_test, clf.predict(X_test)), 3))
    test_f1score.append(round(f1_score(y_test, clf.predict(X_test)),3))
    test_matthews.append(round(matthews_corrcoef(y_test, clf.predict(X_test)),3))
    print("The Accuracy Score: ", accuracy_score(y_test, clf.predict(X_test)))
    print("Test F1 Score: ",f1_score(y_test,clf.predict(X_test)))
    print("The Testing Matthews coefficient: ", matthews_corrcoef(y_test, clf.predict(X_test)))
    print(n+" testing score done!")
    print("-------------------------------------------------------")
    print("  ")
    i = i+1
print("Names: ", clf_names)
print("Train Accuracy Scores: ", train_accuracy_score)
print("Test Accuracy Scores: ", test_accuracy_score)
print("Train F1 Scores: ", train_f1score)
print("Test F1 Scores: ", test_f1score)
print("Train Matthews Coefficients", train_matthews)
print("Test Matthews Coefficients", test_matthews)


# In[27]:


plt.rcParams['figure.figsize'] = (40.0, 30.0)
figs, ax = plt.subplots(2,3)

ax[0,0].scatter(x =  train_accuracy_score,y = clf_names)
ax[0,0].set_title("Train Accuracy")
ax[0,0].grid(True, color = 'g')

ax[0,1].scatter(x =  train_f1score,y = clf_names)
ax[0,1].set_title("Train Accuracy")
ax[0,1].grid(True, color = 'g')

ax[0,2].scatter(x =  train_matthews,y = clf_names)
ax[0,2].set_title("Train Matthews Coefficients")
ax[0,2].grid(True, color = 'g')


ax[1,0].scatter(test_accuracy_score,clf_names)
ax[1,0].set_title("Test Accuracy")
ax[1,0].grid(True, color = 'g')


ax[1,1].scatter(test_f1score,clf_names)
ax[1,1].set_title("Test F1 Score")
ax[1,1].grid(True, color = 'g')

ax[1,2].scatter(test_matthews,clf_names)
ax[1,2].set_title("Test Matthews Coefficients")
ax[1,2].grid(True, color = 'g')

plt.show()


# From the graphs above, one would notice overfitting on the Random Forest classifier. The Linear SVM showed the best test accuracy. This is followed by the Stochastic Gradient Descent (SGD) Classifier, Decision Tree, Naive Bayes  and Logistic Regression. 

# # Polynomial Features

# The PolynomialFeatures will be used for feature creation to explore the nonlinear pattern of the numerical data.

# In[28]:


plt.rcParams['figure.figsize'] = (3.0, 3.0)
#use each Classifier to take its training results.
clf_names = []
train_accuracy_score = []
test_accuracy_score = []
predict_sums = []
test_f1score = []
train_f1score = []
test_matthews = []
train_matthews = []
i = 0

for n,clf in classifiers_:
    clf_names.append(n)
    
    # Model declaration with pipeline
    clf = Pipeline([('POLY', poly),('CLF',clf)])
    
    # Model training
    clf.fit(X_train, y_train)
    print(i, ":",  n+" training done! \n ")
    
    # The prediction for both training and testing 
    clf.predict(X_test)
    clf.predict(X_train)
    predict_sums.append(clf.predict(X_test).sum()) 
        #you can print the classification report and confusion matrix if you like
    print(classification_report(y_test, clf.predict(X_test)))
    print(confusion_matrix(y_test, clf.predict(X_test)))
    
    #you can also plot the confussion matrix if you like
    disp1 = plot_confusion_matrix(clf, X_train, y_train,
                              display_labels=['YES','NO'],
                              cmap=plt.cm.Blues,
                              normalize=None)
    disp1.ax_.set_title('Confusion matrix')
    plt.show()
    
    disp = plot_confusion_matrix(clf, X_test, y_test,
                              display_labels=['YES','NO'],
                              cmap=plt.cm.Blues,
                              normalize=None)
    disp.ax_.set_title('Confusion matrix')
    plt.show()
    
    # Measure training accuracy
    train_accuracy_score.append(round(accuracy_score(y_train, clf.predict(X_train)), 3))
    train_matthews.append(round(matthews_corrcoef(y_train, clf.predict(X_train)),3))
    train_f1score.append(round(f1_score(y_train, clf.predict(X_train)),3))
    print("The Training Accuracy Score: ", accuracy_score(y_train, clf.predict(X_train)) )
    print("The Training F1 Score: ", f1_score(y_train, clf.predict(X_train)) )
    print("The Training Matthews coefficient: ", matthews_corrcoef(y_train, clf.predict(X_train)))
    print(n+" training score done!")
    
    # Measure test accuracy 
    test_accuracy_score.append(round(accuracy_score(y_test, clf.predict(X_test)), 3))
    test_f1score.append(round(f1_score(y_test, clf.predict(X_test)),3))
    test_matthews.append(round(matthews_corrcoef(y_test, clf.predict(X_test)),3))
    print("The Accuracy Score: ", accuracy_score(y_test, clf.predict(X_test)))
    print("Test F1 Score: ",f1_score(y_test,clf.predict(X_test)))
    print("The Testing Matthews coefficient: ", matthews_corrcoef(y_test, clf.predict(X_test)))
    print(n+" testing score done!")
    print("-------------------------------------------------------")
    print("  ")
    i = i+1
print("Names: ", clf_names)
print("Train Accuracy Scores: ", train_accuracy_score)
print("Test Accuracy Scores: ", test_accuracy_score)
print("Train F1 Scores: ", train_f1score)
print("Test F1 Scores: ", test_f1score)
print("Train Matthews Coefficients", train_matthews)
print("Test Matthews Coefficients", test_matthews)


# In[29]:


plt.rcParams['figure.figsize'] = (30.0, 25.0)
figs, ax = plt.subplots(2,3)

ax[0,0].scatter(x =  train_accuracy_score,y = clf_names)
ax[0,0].set_title("Train Accuracy")
ax[0,0].grid(True, color = 'g')

ax[0,1].scatter(x =  train_f1score,y = clf_names)
ax[0,1].set_title("Train Accuracy")
ax[0,1].grid(True, color = 'g')

ax[0,2].scatter(x =  train_matthews,y = clf_names)
ax[0,2].set_title("Train Matthews Coefficients")
ax[0,2].grid(True, color = 'g')


ax[1,0].scatter(test_accuracy_score,clf_names)
ax[1,0].set_title("Test Accuracy")
ax[1,0].grid(True, color = 'g')


ax[1,1].scatter(test_f1score,clf_names)
ax[1,1].set_title("Test F1 Score")
ax[1,1].grid(True, color = 'g')

ax[1,2].scatter(test_matthews,clf_names)
ax[1,2].set_title("Test Matthews Coefficients")
ax[1,2].grid(True, color = 'g')

plt.show()


# From the graphs above, most of the models performed better with polynomial input features. In fact the Bagging classifier (with accuracy score = 0.911) did better than the Linear SVM (with accuracy score = 0.903) when the linear input features are used. This is followed by the QDA, Decision Tree, Gaussian Process and Nearest Neighbours. So, from here on, I will stick with using the polynomial input features. 
# 
# One can combine the few best multiple models into a single model to obtain a hopefully better accuracy. The models are combined using the Stacking Classifier. That is, combining the prediction probabilities from multiple machine learning models on the same dataset. 
# 

# # Combining the models

# In[30]:


#THE STACKING CLASSIFIER
#Let's use the combination of the prediction probability of the best five classifiers

bestclassifiers = [("BaggingClassifier", BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=0)), 
    ("QDA", QuadraticDiscriminantAnalysis()),
    ("Decision Tree", DecisionTreeClassifier(max_depth=10)),
    ("Gaussian Process", GaussianProcessClassifier(1.0 * RBF(1.0))),
    ("Nearest Neighbors",KNeighborsClassifier(2))
                  ] 

#Build the stack model
stack_model = StackingClassifier(estimators = bestclassifiers, final_estimator = BaggingClassifier(base_estimator=SVC(), n_estimators=10, random_state=0) )
#I used the best estimator as my final estimator to optimise the result.

# Model declaration with pipeline
stack_model = Pipeline([('POLY', poly),('CLF',stack_model)])

#train the stack model
stack_model.fit(X_train, y_train)



# The prediction for both training and testing 
stack_model.predict(X_test)
stack_model.predict(X_train)

# Measure training accuracy

print("The Training Accuracy Score: ", accuracy_score(y_train, stack_model.predict(X_train)) )
print("The Training F1 Score: ", f1_score(y_train, stack_model.predict(X_train)) )
print("The Training Matthews coefficient: ", matthews_corrcoef(y_train, stack_model.predict(X_train)))

    
# Measure test accuracy 

print("Test Accuracy Score: ", accuracy_score(y_test, stack_model.predict(X_test)))
print("Test F1 Score: ",f1_score(y_test,stack_model.predict(X_test)))
print("The Testing Matthews coefficient: ", matthews_corrcoef(y_test, stack_model.predict(X_test)))


# Although the stack_model (with accuracy score = 0.858, f1 score = 0.903 and Matthews coefficient = 0.663) performed way better than most of the models used, it is still not as accurate as the Bagging Classifier (with accuracy Score = 0.875 , f1 score = 0.911 and Matthews coefficient = 0.704). So, I would rather stick with the single model when deploying.  

# We can also get the most importance features for determing the result of the loan eligibility. This can basically be included when deploying the models but it is done here for clarity purpose. This is not straight-forward since we are using the pipepline. 

# # Most important feature

# In[38]:


#to obtain the feature importance, 

theclassifiers = classifiers_ = [
    ("AdaBoost", AdaBoostClassifier()),
    ("Decision Tree", DecisionTreeClassifier(max_depth=3)),
    ("Random Forest",RandomForestClassifier(n_jobs=2, random_state=1))
    ] 
#NB: these classifiers are considered because they are only once amongst the classfiers considered that run with the 
# "feature_importances_" code line

for n,clif in theclassifiers:
    clif = Pipeline([('POLY', poly),('CLF',clif)])
    clif.fit(X_train, y_train)
    feature_names = clif.named_steps["POLY"].get_feature_names()
#put the name of the column heads in a list
    column_head = loan_train.drop(["Loan_Status"], axis = 1).columns

#obtain the coefficients of the features
    coefs = clif.named_steps["CLF"].feature_importances_.flatten()

# Zip coefficients and names together and make a DataFrame
    zipped = zip(feature_names, coefs)
    df = pd.DataFrame(zipped, columns=["feature", "value"])

#since we need the names of the column heads as the tick labels
    for i in range(len(column_head)):
        df["feature"][i] = column_head[i]
    
#Make a bar chart of the coefficients
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    sns.barplot(x=df["feature"][0:len(column_head)],
                y=df["value"][0:len(column_head)])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=20)
    ax.set_title(n, fontsize=25)
    ax.set_ylabel("Coefficients", fontsize=22)
    ax.set_xlabel("Feature Name", fontsize=22)
    ax.grid(True, color = "g")
    plt.show()


# The scores suggest that the important features, which are features with non-zero coefficients, are dependent on the model deployed. However, the three plots above show that the property being in the Semi-Urban area appears to be generally "the most" important feature. Basically, all other features with a zero coefficient are essentially removed them from the model.

# # DEPLOYING THE MODEL

# Since we have found out that the best model is the BaggingClassifier. This model is typically deployed by exporting the model and binding it with an application API. Here, I will just try to take the details of the from the customers to prediction the customers eligibility for the loan. 

# In[32]:


#GENDER
gender = input("State your gender [Male(m) or Female (f)]:\n ").lower()
if gender in ["male", "m"]:
    Male_Gender = 1
elif gender in ["female", "f"]:
    Male_Gender = 0
else:
    print("ERROR: Invalid Input!!!")
    
#MARITAL STATUS
married = input("Are you married? (y/n) \n ").lower()
if married in ["yes", "y"]:
    Married = 1
elif married in ["no", "n"]:
    Married = 0
else:
    print("ERROR: Invalid Input!!!")

#GRADUATE
graduate = input("Are you a graduate? (y/n) \n ").lower()
if graduate in ["yes", "y"]:
    Not_Graduate = 0
elif graduate in ["no", "n"]:
    Not_Graduate = 1
else:
    print("ERROR: Invalid Input!!!")
    
#SELF-EMPLOYED
Self_Employed = input("Are you self-employed? (y/n) \n ").lower()
if Self_Employed in ["yes", "y"]:
    Self_Employed = 1
elif Self_Employed in ["no", "n"]:
    Self_Employed = 0
else:
    print("ERROR: Invalid Input!!!")
    
#Applicant's Income
ApplicantIncome = input("What the applicant's income? (Enter figures only) \n ")
ApplicantIncome = float(ApplicantIncome)

#Co-Applicant's Income
CoapplicantIncome = input("What the co-applicant's income? (Enter figures only) \n ")
CoapplicantIncome = float(CoapplicantIncome)

#LOAN AMOUNT
LoanAmount  = input("How much do you want to loan? (Enter figures only) \n")
LoanAmount = float(LoanAmount)

#LOAN AMOUNT TERM
Loan_Amount_Term = input("How long (in months) is the loan for? (Enter figures only) \n")
Loan_Amount_Term = float(Loan_Amount_Term)

#CREDIT HISTORY
Credit_History = input("Does your credit history completely meet the requirements? (y/n) \n")
if Credit_History in ["yes", "y"]:
    Credit_History = 1
elif Credit_History in ["no", "n"]:
    Credit_History = 0
else:
    print("ERROR: Invalid Input!!!")
    
#Dependents
dependents_0 = 0
dependents_1 = 0
dependents_2 = 0

Dependents = input("How many dependents do you have? (Enter figures only) \n")
Dependents = abs(int(Dependents))
if Dependents==0:
    dependents_0 = 1
elif Dependents==1:
    dependents_1 = 1
elif Dependents==2:
    dependents_2 = 1
    
#PROPERTY AREA
urban = 0
semi_urban = 0
Property_Area = input("Where is the property situated? [Urban (u) or Semi-urban (s) or Rural (r)] \n").lower()
if Property_Area in ["urban", "u"]:
    urban=1
elif Property_Area in ["semi-urban", "s"]:
    semi_urban = 1

    
#The prediction based on the details
print("\n\n THE LOAN ELGIBILTY: ")
Xnew = [[Male_Gender, Married, Not_Graduate, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History,semi_urban, urban, dependents_0, dependents_1, dependents_2]]
Xnew = sc.transform(Xnew)

AdaBoostCF =  AdaBoostClassifier()
AdaBoostCF = Pipeline([('POLY', poly),('CLF',AdaBoostCF)])
AdaBoostCF.fit(X_train, y_train)

ynew = AdaBoostCF.predict(Xnew)
if ynew[0]==0: 
    print("Sorry, you are not eligible for a loan.")
elif ynew[0]==1:
    print("Congratulations, you are eligible for a loan")

    

