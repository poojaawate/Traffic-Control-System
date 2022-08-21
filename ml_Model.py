# importing libraries  
import numpy as nm  
import matplotlib.pyplot as mtp  
import pandas as pd  
  
#importing datasets 
print("Loading the Dataset...." ) 
data_set= pd.read_csv('dataset.csv')  
#print(data_set)  

#Extracting Independent and dependent Variable  
y= data_set.iloc[:, [0]].values  
x= data_set.iloc[:, [1]].values

#print(x)
#print(y)
 
# Splitting the dataset into training and test set. 
print("Splitting Dataset: Training Set = 75% , Test Set = 25%") 
from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.25, random_state=0) 

'''  
#feature Scaling  
from sklearn.preprocessing import StandardScaler    
st_x= StandardScaler()    
x_train= st_x.fit_transform(x_train)    
x_test= st_x.transform(x_test)  
'''

#Fitting K-NN classifier to the training set  
from sklearn.neighbors import KNeighborsClassifier  
classifier= KNeighborsClassifier(n_neighbors=2)  
classifier.fit(x_train, y_train)  

#Predicting the test set result  
y_pred= classifier.predict(x_train) 

#Creating the Confusion matrix  
from sklearn.metrics import confusion_matrix, accuracy_score  
cm= confusion_matrix(y_train, y_pred) 
acc = accuracy_score(y_train, y_pred) 

print(cm)
print("Accuracy of Model = ",acc*100,"%")
