import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def fit_and_plot_logistic_regression(X_train, X_test, y_train, y_test, feature_names, max_iter=1000, top_features=20, solver='saga', penalty='l2', tol=0.01):
    """
    Fits a Logistic Regression model on the numeric training data and plots the top N features based on their importance.
    Now includes performance optimizations, retains numeric column selection within the function, and enhances visual output.
    
    Parameters:
    - X_train: Training feature DataFrame.
    - X_test: Test feature DataFrame.
    - y_train: Training labels.
    - y_test: Test labels.
    - feature_names: Names of the features in the original dataset.
    - max_iter: Maximum number of iterations for Logistic Regression.
    - top_features: Number of top features to display.
    - solver: Solver to use for Logistic Regression, 'saga' recommended for large datasets.
    - penalty: Penalty (regularization term) to use, 'l2' or 'none'.
    - tol: Tolerance for stopping criteria, consider increasing for faster convergence.
    """
    print('Select numeric columns only')
    numeric_columns = X_train.select_dtypes(include=['number']).columns
    X_train_numeric = X_train[numeric_columns]
    X_test_numeric = X_test[numeric_columns]

    print('Ensure feature_names only includes names of numeric columns')
    feature_names_numeric = [name for name in feature_names if name in numeric_columns]

    print('Initialize and fit the Logistic Regression model')
    log_reg = LogisticRegression(max_iter=max_iter, solver=solver, penalty=penalty, tol=tol, n_jobs=-1)
    log_reg.fit(X_train_numeric, y_train)

    print('Extract the coefficients of the model')
    coefficients = np.abs(log_reg.coef_[0])

    print('Sort the features by the absolute value of their coefficients')
    sorted_indices = np.argsort(coefficients)[::-1]

    print('Plot the top N features based on their importance')
    plt.figure(figsize=(15, 8))  # Larger figure size for better readability
    top_indices = sorted_indices[:top_features]
    colors = plt.cm.viridis(coefficients[top_indices] / coefficients[top_indices].max())  # Apply color mapping for visual appeal
    bars = plt.bar(range(top_features), coefficients[top_indices], align='center', color=colors)
    
    plt.xticks(range(top_features), labels=np.array(feature_names_numeric)[top_indices], rotation=45, fontsize=12)  # Improve label readability
    plt.yticks(fontsize=12)
    plt.xlabel('Feature', fontsize=14)
    plt.ylabel('Absolute Coefficient Value', fontsize=14)
    plt.title(f'Top {top_features} Logistic Regression Coefficients for Numeric Features', fontsize=16)
    
    # Annotate bars with their exact coefficient values for clarity
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()  # Ensure everything fits without overlap
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add gridlines for easier interpretation of bar heights
    plt.show()
