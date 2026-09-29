import pandas as pd 
import mysql.connector 
from sklearn.tree import DecisionTreeClassifier

connection=mysql.connector.connect(
    host='mysql-db',
    user='root',
    password='secret-pass',
    database='ml_db'
    )

query="""
    SELECT sepal_length,sepal_width,petal_length,petal_width,species FROM iris_data
    """

df=pd.read_sql(query,connection)

connection.close()

print("Data from MySql:")
print(df)

X=df[['sepal_length','sepal_width','petal_length','petal_width']]
y=df['species']

model=DecisionTreeClassifier()
model.fit(X,y)

sample = [[5.0, 3.4, 1.5, 0.2]]

prediction=model.predict(sample)

print("Prediction:",prediction)