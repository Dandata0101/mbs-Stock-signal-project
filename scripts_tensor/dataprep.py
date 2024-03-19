from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
def prepare_and_split_data_grouped(df, target_column_name, identifier_columns, group_column, test_size=0.2, random_state=42):
   
    print('Separate features, target, and identifiers, ensuring group column is included in identifiers')
    if group_column not in identifier_columns:
        identifier_columns.append(group_column)
    
    # Separating out features, target, and identifiers
    X = df.drop(columns=[target_column_name] + identifier_columns)
    feature_names = X.columns.tolist()   
    y = df[target_column_name]
    identifiers = df[identifier_columns]
    groups = df[group_column]

    print('Performing group-based train-test split')
    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(gss.split(X, y, groups))
    
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    identifiers_train, identifiers_test = identifiers.iloc[train_idx], identifiers.iloc[test_idx]

    print('Normalizing data (scaling)')
    scaler = StandardScaler()
    # Filter for numeric columns only for scaling
    numeric_columns = X_train.select_dtypes(include=['number']).columns
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train[numeric_columns]), columns=numeric_columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test[numeric_columns]), columns=numeric_columns, index=X_test.index)

    print('Ensure the non-numeric data is concatenated back after scaling')
    non_numeric_columns = X_train.select_dtypes(exclude=['number']).columns
    if len(non_numeric_columns) > 0: # Check if there are non-numeric columns to concatenate
        X_train_scaled = pd.concat([X_train_scaled, X_train[non_numeric_columns]], axis=1)
        X_test_scaled = pd.concat([X_test_scaled, X_test[non_numeric_columns]], axis=1)
    
    feature_names = X.columns.tolist()    

    print('Transformation complete')

    # Updating return statement to include X_train_scaled and X_test_scaled
    return X,X_train,X_test, X_train_scaled, X_test_scaled, y_train, y_test, identifiers_train, identifiers_test,feature_names
