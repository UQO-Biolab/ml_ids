import pandas as pd
import seaborn as sns

# Insert your dataset
df = pd.read_csv('test_dataset.csv')

# 2. Convert to datetime
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Extract hours data
df['start_hour'] = df['start_time'].dt.hour
df['start_weekday'] = df['start_time'].dt.weekday
df['start_month'] = df['start_time'].dt.month

df['end_hour'] = df['end_time'].dt.hour
df['end_weekday'] = df['end_time'].dt.weekday
df['end_month'] = df['end_time'].dt.month

# Add duration feature
df['duration_sec'] = (df['end_time'] - df['start_time']).dt.total_seconds()

df = df.drop(columns=['@timestamp', 'start_time', 'end_time'])

# Convert ip to int
import ipaddress
MAX_IPV4 = 2**32 - 1
df['ip_norm'] = df['remote_ip'].apply(lambda x: int(ipaddress.IPv4Address(x)) / MAX_IPV4)
print(df['ip_norm'])

# 6. Convert hashes to float
MAX_MD5 = 2**128 - 1
MAX_SHA512 = 2**512 - 1

def hash_to_float(h, max_val):
    try:
        return int(h, 16) / max_val
    except:
        return 0.0

df['md5_feature'] = df['payload/md5_hash'].apply(lambda x: hash_to_float(x, MAX_MD5))
df['sha512_feature'] = df['payload/sha512_hash'].apply(lambda x: hash_to_float(x, MAX_SHA512))

# Insert features in dataframe
X = df[['duration_sec', 'ip_norm', 'remote_port', 'local_port', 'md5_feature', 'sha512_feature', 'payload/length', 'operation_mode', 'download_count', 'download_tries']]  # entrées
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

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
print("\nClassification :\n", classification_report(y_test, y_pred))

# Extract model with DecisionTreeClassifier
joblib.dump(model, 'model_honeytrap.pkl')

###################################
# RandomForestClassifier training #
###################################
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100)
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
# Building a Support Vector Machine on train data
svc_model = SVC(C= .1, gamma= 1, kernel='sigmoid', random_state=42)
svc_model.fit(X_train, y_train)
prediction = svc_model .predict(X_test)
# check the accuracy on the training set
print('Accuracy of training data: ', svc_model.score(X_train, y_train))
print('Accuracy of validation data: ',svc_model.score(X_test, y_test))
from sklearn.metrics import confusion_matrix, classification_report
# generating classification report
print(classification_report(y_test, prediction))
confusion_matrix(y_test, prediction)
sns.heatmap(confusion_matrix(y_test, prediction), annot = True, fmt='0.0f')

###################################
### LogisticRegression training ###
###################################
from sklearn.linear_model import LogisticRegression
lgr = LogisticRegression(random_state=0)
lgr.fit(X_train,y_train)
y_pre_test = lgr.predict(X_test)
y_pre_train = lgr.predict(X_train)
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
# Bernoullis Navaive bayes classifier
nvb = BernoulliNB()
nvb.fit(X_train,y_train)
y_pre_test = nvb.predict(X_test)
y_pre_train = nvb.predict(X_train)
from sklearn.metrics import accuracy_score
train_accurry = accuracy_score(y_pre_train, y_train)
test_accurry = accuracy_score(y_pre_test, y_test)
print('Accuracy for train dataset for naive bayes  reg : ', train_accurry)
print('Accuracy for test dataset for naive bayes reg : ', test_accurry)
from sklearn.metrics import confusion_matrix, classification_report
print(classification_report(y_test, y_pre_test ))
confusion_matrix(y_test, y_pre_test)
sns.heatmap(confusion_matrix(y_test, y_pre_test), annot = True, fmt='0.0f')