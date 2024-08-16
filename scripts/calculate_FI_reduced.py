import os
import pandas as pd 
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV

# Initialize lists for results
features_weight = []
features_gain   = []

# Select the file to process
for file in sorted(os.listdir('final_datasets_reduced/')):
    
    print(f"\n\nProcessing {file}")    
    
    # Set the name for the columns and read file
    cols = ['Year','nodeID','SDcen','SClCoef','SClCen','DBcen','DG','DI','DClCoef','DClcen','DKatz','Target']
    data = pd.read_csv(f"final_datasets_reduced/{file}",sep=' ',names=cols)

    # Sort by ID
    sorted_data = data.sort_values(by=['nodeID','Year'])

    # Create Features to study and target values.
    features = ['nodeID','Year','SDcen','SClCoef','SClCen','DBcen','DG','DI','DClCoef','DClcen','DKatz']

    X = sorted_data[features]
    y = sorted_data['Target']

    # Split the dataset into training and testing based on the 'Year' column
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define XGB model
    model = xgb.XGBRegressor(objective='reg:squarederror',n_estimators=100, learning_rate=0.1, max_depth=6)

    # Training Phase
    model.fit(X_train, y_train, verbose=True) # Change verbose to True if you want to see it train
    print("\nInitial Model Trained")
    
    print("Weight")
    print(model.get_booster().get_score(importance_type='weight'))
    
    print("Gain")
    print(model.get_booster().get_score(importance_type='gain'))
    
    # Store the result data into the lists that we've previously created
    features_weight.append(model.get_booster().get_score(importance_type='weight'))
    features_gain.append(  model.get_booster().get_score(importance_type='gain'))
    

# Convert the list of dicts onto a dataframe
features_weight_df = pd.DataFrame(features_weight)
features_gain_df = pd.DataFrame(features_gain)

# Store each dataframe as a csv file
features_weight_df.to_csv(f"results/reduced/FI_w_r", sep=',', index=False, encoding='utf-8')
features_gain_df.to_csv(f"results/reduced/FI_g_r", sep=',', index=False, encoding='utf-8')
