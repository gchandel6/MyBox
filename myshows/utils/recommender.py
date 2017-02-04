import pandas as p
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import scale
from .cts import build_training_set
import os 
from random import shuffle

file_dir=os.path.dirname(__file__)

training_df=build_training_set()
training_df=training_df.iloc[:,1:]

x_training=scale(training_df.iloc[:,5:])

y_training=training_df.iloc[:,3]

x_training_labels=training_df.iloc[:,0]


testing_df=p.read_csv(os.path.join(file_dir,"data.csv"))
testing_df=p.DataFrame(testing_df)
testing_df=testing_df.append(testing_df)
testing_df=testing_df.append(testing_df)
testing_df=testing_df.drop_duplicates("SeriesName")


x_testing=testing_df.iloc[:,5:]

x_testing_labels=testing_df.iloc[:,0]


def get_recommendations():

	classifier=RandomForestClassifier()
	classifier.fit(x_training,y_training)

	results=classifier.predict(x_testing)

	newdf=p.DataFrame()
	newdf['series_name']=testing_df.iloc[:,0]
	newdf['tvdbID']=testing_df.iloc[:,1]
	newdf['predicted_rating']=results
	newdf['indicator']=(training_df.iloc[:,4] * training_df.iloc[:,3])*newdf['predicted_rating']

	newdf=newdf.sort(['indicator'],ascending=False)

	return list(newdf.iloc[:4,1])


