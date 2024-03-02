import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns


def predict_trading_signals(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    def add_technical_indicators(df):
        df['VIX']=df['VIX']
        df['fedrate']=df['fedrate']
        df['VIX_short']= df['VIX'].rolling(window=5).mean()
        df['VIX_long']= df['VIX'].rolling(window=15).mean() 
        df['close_short'] = df['Close'].rolling(window=5).mean()
        df['close_long'] = df['Close'].rolling(window=15).mean()
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal_line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        return df

    def label_data(df):
        df['Label'] = 0
        df.loc[df['close_short'] > df['close_long'], 'Label'] = 1
        return df

    df = add_technical_indicators(df)
    df = label_data(df)

    train_df = df.loc['2015-01-01':'2019-12-31']
    test_df = df.loc['2020-01-01':'2024-02-29']

    features = ['close_short','fedrate','VIX','VIX_short','VIX_long','close_long', 'RSI', 'MACD', 'Signal_line']
    train_df.dropna(subset=features + ['Label'], inplace=True)
    X_train = train_df[features]
    y_train = train_df['Label']
    X_test = test_df[features].dropna()
    y_test = test_df.loc[X_test.index, 'Label']  # Ensure y_test is defined for accuracy calculation

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['auto','sqrt']
    }

    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    predictions = best_model.predict(X_test)
    test_df.loc[X_test.index, 'Predictions'] = predictions

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy}")
    print(f"Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

    feature_importances = best_model.feature_importances_
    importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances}).sort_values(by='Importance', ascending=False)
    print("Feature Importances:")
    print(importance_df)

     # After calculating accuracy, precision, recall, f1
    current_directory = os.getcwd()

    cm = confusion_matrix(y_test, predictions)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig(current_directory+'/static/images/confusion_matrix.png')
    plt.close()

    def add_signals_and_prices(df):
        df['Buy_Signal'] = 0
        df['Sell_Signal'] = 0
        df['pricebuy'] = np.nan
        df['pricesell'] = np.nan

        last_signal = None

        for i in range(1, len(df)):
            current_signal = None
            
            if df.iloc[i]['Predictions'] == 1 and df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
                current_signal = 'buy'
            elif df.iloc[i]['Predictions'] == 0 and df.iloc[i]['Close'] < df.iloc[i-1]['Close'] * 0.99:
                current_signal = 'sell'
            
            if current_signal and current_signal != last_signal:
                if current_signal == 'buy':
                    df.at[df.index[i], 'pricebuy'] = df.iloc[i]['Close']
                    last_signal = 'buy'
                elif current_signal == 'sell':
                    df.at[df.index[i], 'pricesell'] = df.iloc[i]['Close']
                    last_signal = 'sell'

        df['Buy_Signal'] = df['pricebuy'].notnull().astype(int)
        df['Sell_Signal'] = df['pricesell'].notnull().astype(int)

        return df

    # Apply signals and prices to the test DataFrame
    test_df = add_signals_and_prices(test_df)
    test_df.reset_index(inplace=True)  # Reset index to make 'Date' a column again


    return test_df, accuracy, precision, recall, f1, feature_importances, importance_df

