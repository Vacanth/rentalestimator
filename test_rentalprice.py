import numpy as np
import pandas as pd
import requests
import json


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OrdinalEncoder,PolynomialFeatures,OneHotEncoder,LabelEncoder
from sklearn.compose import ColumnTransformer


numerical_features = ['accommodates',
                      'bathrooms',
                      'bedrooms',
                      'beds',
                      'cleaning_fee',
                      'guests_included','extra_people',
                      'minimum_nights',#'maximun_nights',
                      'availability_30', 
                      'availability_60', 
                      'availability_90',
                      'availability_365', 
                      'number_of_reviews',
                      'review_scores_rating', 
                      'review_scores_accuracy', 
                      'review_scores_cleanliness',
                      'review_scores_checkin',
                      'review_scores_communication',
                      'review_scores_location',
                      'review_scores_value'
                    ]

categorical_features = ["neighbourhood_cleansed",
                        "city",
                        "state",#"zipcode",
                        "property_type",
                        "room_type", 
                        "bed_type", 
                        "cancellation_policy",
                        "instant_bookable","host_is_superhost","tv","cable_tv","internet",
                        "wireless_internet","kitchen","breakfast","pets_allowed",
                        "air_conditioning","heating","bathtub","pool","smoking_allowed",
                        "hot_tub","washer","dryer","family/kid_friendly",
                        "wheelchair_accessible", "indoor_fireplace","self_check-in","lockbox",
                        "free_parking_on_premises","gym","smoke_detector",
                        "carbon_monoxide_detector","first_aid_kit", "fire_extinguisher",
                        "essentials","shampoo","24-hour_check-in", "review_score"]


# Perform numerical features transformation
numeric_transformer = Pipeline(steps=[('polynomial',PolynomialFeatures(degree=2)),
                                      ('scaler', StandardScaler())])

# Perform categorical features transformation
categorical_transformer = Pipeline([('ordinal_encoder', OrdinalEncoder())])

# Apply separate transformer for numerical and categorical features
preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numerical_features),
                                                ('cat', categorical_transformer, categorical_features)],
                                 remainder='passthrough')

# Features for processing
df_feature_set = listings[['id'] + numerical_features + categorical_features + ['price']].copy()

# LabelEncode object feilds
le_cols=['neighbourhood_cleansed','city','state',
         'property_type','room_type','bed_type',
         'cancellation_policy','review_scores_value','review_score']
df_feature_set[le_cols] = df_feature_set[le_cols].apply(LabelEncoder().fit_transform).astype(int)

# Features
X = df_feature_set.drop('price', axis = 1)
X.fillna(0, inplace=True)

#Target
y = df_feature_set['price']

# Load data
listings= pd.read_csv("SF_airbnb-listings.csv",dtype={"State": "string","Zipcode":"string"})

# Features
X = df_feature_set.drop('price', axis = 1)

#Target
y = df_feature_set['price']
# Test/Train split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Serialize the data into json and send the request to the model
payload = {'data': json.dumps(X_test.tolist())}
y_predict = requests.post('http://127.0.0.1:5000/listprice', data=payload).json()

# Make array from the list
y_predict = np.array(y_predict)
print(y_predict)