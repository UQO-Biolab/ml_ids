import pandas as pd
import seaborn as sns

# Insert your dataset
df = pd.read_csv('cowrie_sessions_40k_label_correct.csv')

# Convert ip to int
import ipaddress
MAX_IPV4 = 2**32 - 1
df["src_ip_int"] = df["src_ip"].apply(lambda ip: int(ipaddress.IPv4Address(ip)) if pd.notna(ip) else -1)

# Map str(protocol) to 0 or 1
df['protocol'] =  df['protocol'].map({'ssh': 0, 'telnet': 1})

# Insert features in dataframe
X = df[[ 'duration', 'src_ip_int', 'src_port', 'dst_port', 'protocol', 'total_connexion', 'login_success', 'login_failed', 'avg_time_between_failed', 'is_business_hours']]  # entrées
y = df['label']

###################################
# DecisionTreeClassifier training #
###################################
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, classification_report

# Split training & test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create & train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Confusion matrix for our model
confusion_matrix(y_test, y_pred)
sns.heatmap(confusion_matrix(y_test, y_pred), annot = True, fmt='0.0f')

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification:\n", classification_report(y_test, y_pred))

# Extract model with DecisionTreeClassifier
joblib.dump(model, 'model_cowrie.pkl')

###################################
# RandomForestClassifier training #
###################################
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=150)
# Fittin the model
rfc.fit(X_train, y_train)

# Prediction on validation dataset
y_pred = rfc.predict(X_test)

# Prediction on training dataset
y_pred_train = rfc.predict(X_train)

from sklearn import metrics
print("Train ACCURACY OF THE MODEL: ", metrics.accuracy_score(y_train, y_pred_train))
print("ACCURACY OF THE MODEL: ", metrics.accuracy_score(y_test, y_pred))
from sklearn.metrics import confusion_matrix, classification_report
print(classification_report(y_test, y_pred))
confusion_matrix(y_test, y_pred)
sns.heatmap(confusion_matrix(y_test, y_pred), annot = True, fmt='0.0f')

###################################
########## SVC training ###########
###################################
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
# Building a Support Vector Machine on train data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
imputer = SimpleImputer(strategy='mean')  # You can use other strategies like 'median' or 'most_frequent'
svc_pipeline = make_pipeline(imputer, SVC(C=.1, gamma=1, kernel='sigmoid', random_state=42))
svc_pipeline.fit(X_train, y_train)
prediction = svc_pipeline.predict(X_test)

svc_model = SVC(C= .1, gamma= 1, kernel='sigmoid', random_state=42)
#svc_model.fit(X_train, y_train)
#prediction = svc_model .predict(X_test)
# check the accuracy on the training set
print('Accuracy of training data: ', svc_pipeline.score(X_train, y_train))
print('Accuracy of validation data: ',svc_pipeline.score(X_test, y_test))
from sklearn.metrics import confusion_matrix, classification_report
# generating classification report
print(classification_report(y_test, prediction))
confusion_matrix(y_test, prediction)
sns.heatmap(confusion_matrix(y_test, prediction), annot = True, fmt='0.0f')

###################################
### LogisticRegression training ###
###################################
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

# Create an imputer to fill NaN values with the mean
imputer = SimpleImputer(strategy='mean')
# Create a pipeline to apply imputation before fitting the model
lgr_pipeline = make_pipeline(imputer, LogisticRegression(random_state=0))

# Fit the pipeline to the training data
lgr_pipeline.fit(X_train, y_train)

# Predict on the test data
y_pre_test = lgr_pipeline.predict(X_test)
y_pre_train = lgr_pipeline.predict(X_train)
lgr = LogisticRegression(random_state=0)
#lgr.fit(X_train,y_train)
#y_pre_test = lgr.predict(X_test)
#y_pre_train = lgr.predict(X_train)
from sklearn.metrics import accuracy_score
train_accurry = accuracy_score(y_pre_train, y_train)
test_accurry = accuracy_score(y_pre_test, y_test)
print('Accuracy for train dataset for logistic reg : ', train_accurry)
print('Accuracy for test dataset for logistic reg : ', test_accurry)
from sklearn.metrics import confusion_matrix, classification_report
print(classification_report(y_test, y_pre_test ))
confusion_matrix(y_test, y_pre_test )
sns.heatmap(confusion_matrix(y_test,y_pre_test), annot = True, fmt='0.0f')

###################################
###### NaivesBayes training #######
###################################
from sklearn.naive_bayes import GaussianNB, MultinomialNB, CategoricalNB, BernoulliNB, ComplementNB
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

# Bernoullis Navaive bayes classifier
# Create a pipeline with an imputer to handle NaN values
nvb_pipeline = make_pipeline(SimpleImputer(strategy='most_frequent'), BernoulliNB()) # Using 'most_frequent' for categorical features

# Fit the pipeline to the training data
nvb_pipeline.fit(X_train, y_train)

# Predict on the test and train data using the pipeline
y_pre_test = nvb_pipeline.predict(X_test)
y_pre_train = nvb_pipeline.predict(X_train)

from sklearn.metrics import accuracy_score
train_accurry = accuracy_score(y_pre_train, y_train)
test_accurry = accuracy_score(y_pre_test, y_test)
print('Accuracy for train dataset for naive bayes  reg : ', train_accurry)
print('Accuracy for test dataset for naive bayes reg : ', test_accurry)
from sklearn.metrics import confusion_matrix, classification_report
print(classification_report(y_test, y_pre_test ))
confusion_matrix(y_test, y_pre_test)
sns.heatmap(confusion_matrix(y_test, y_pre_test), annot = True, fmt='0.0f')

###################################
###### Manipulation of data #######
###################################
import pandas as pd
import joblib

model = joblib.load('model_cowrie.pkl')
features = [ 'duration', 'src_ip_int', 'src_port', 'dst_port', 'protocol', 'total_connexion', 'login_success', 'login_failed', 'avg_time_between_failed', 'is_business_hours']

# Wrong SSH
#x = pd.DataFrame([[500,3232236033,22,22,0,1,0,1,100,False]], columns=features)

# Legit SSH
x = pd.DataFrame([[12.172734,3232236033,50388,22,0,2,2,0,0,False]], columns=features)

result = model.predict(x)
print("Résultat brut :", result)

if result[0] == 1:
    print("⚠️ Alert !")
else:
    print("✅ Normal")