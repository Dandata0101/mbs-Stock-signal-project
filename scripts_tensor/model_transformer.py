import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
import datetime
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
from io import BytesIO

def log_confusion_matrix(y_true, y_pred, class_names, logdir, step):
    cm = confusion_matrix(y_true, y_pred)
    # Adjust figsize to have the same aspect ratio as the TensorBoard card for Beta.
    # The values 12 and 4 are examples; you may need to tweak them to fit your specific TensorBoard layout.
    figure = plt.figure(figsize=(10, 4), dpi=300)
    sns.heatmap(cm, annot=True, fmt="d", cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)  # bbox_inches='tight' may help with fitting
    plt.close(figure)
    buf.seek(0)
    
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    image = tf.expand_dims(image, 0)
    
    # Use a descriptive tag for the image summary
    with tf.summary.create_file_writer(logdir).as_default():
        tf.summary.image("Confusion Matrix/Confusion Matrix", image, step=step)

def log_feature_importance_to_tensorboard(feature_names, importances, logdir, step, top_features=20):
    """
    Logs the top N feature importances as a bar chart to TensorBoard, including gridlines and value labels.
    """
    # Ensure the number of top features does not exceed the total number of features
    top_features = min(top_features, len(importances))

    # Sort features by importance and select the top N
    sorted_indices = np.argsort(importances)[-top_features:]
    sorted_features = np.array(feature_names)[sorted_indices]
    sorted_importances = np.array(importances)[sorted_indices]

    # Color mapping for visual appeal
    colors = cm.viridis(sorted_importances / sorted_importances.max())

    plt.figure(figsize=(8, 4))  # Adjust the figure size as needed for TensorBoard
    bars = plt.bar(range(top_features), sorted_importances, color=colors)

    plt.xticks(range(top_features), labels=sorted_features, rotation=45, ha="right", fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlabel('Feature', fontsize=10)
    plt.ylabel('Importance', fontsize=10)
    plt.title('Top Feature Importances', fontsize=11)

    # Adding gridlines and value labels
    plt.grid(True, which='major', linestyle='--', linewidth='0.5', color='grey')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center', fontsize=8)

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)  # Adjust DPI to manage the trade-off between size and clarity
    plt.close()
    buf.seek(0)

    # Convert PNG buffer to TF image
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    image = tf.expand_dims(image, 0)

    # Log the image to TensorBoard
    with tf.summary.create_file_writer(logdir).as_default():
        tf.summary.image("Feature Importances", image, step=step)

def create_model_with_transformer_and_train(X_train, y_train, X_test, y_test):
    # Define categorical columns
    categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns

    # Preprocess the data
    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ], remainder='passthrough')
    X_train_encoded = preprocessor.fit_transform(X_train).astype('float32')
    X_test_encoded = preprocessor.transform(X_test).astype('float32')

    # Scale the data
    scaler = StandardScaler(with_mean=False)
    X_train_scaled = scaler.fit_transform(X_train_encoded)
    X_test_scaled = scaler.transform(X_test_encoded)

    # Reshape data for the model
    X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], 1, X_train_scaled.shape[1]))
    X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))

    # Define the model
    input_shape = (X_train_reshaped.shape[1], X_train_reshaped.shape[2])
    inputs = layers.Input(shape=input_shape)
    transformer_layer = layers.MultiHeadAttention(num_heads=2, key_dim=2)(inputs, inputs)
    transformer_layer = layers.Dropout(0.1)(transformer_layer)
    transformer_layer = layers.LayerNormalization(epsilon=1e-6)(transformer_layer)
    transformer_output = layers.Flatten()(transformer_layer)
    x = layers.Dense(32, activation='relu')(transformer_output)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    model = models.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Configure callbacks
    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, write_graph=True)
    early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Train the model
    history = model.fit(X_train_reshaped, y_train, epochs=5, batch_size=128, validation_split=0.2, callbacks=[early_stopping, tensorboard_callback])

    # Evaluate the model
    y_pred_prob = model.predict(X_test_reshaped)
    y_pred = (y_pred_prob > 0.5).astype(int).flatten()
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f'\nTest Accuracy: {test_accuracy}')

    # Log the confusion matrix
    class_names = ["Class 0", "Class 1"]
    log_confusion_matrix(y_test, y_pred, class_names, log_dir, step=0)

    importances = np.random.rand(len(X_train.columns))  # This is a placeholder
    log_feature_importance_to_tensorboard(X_train.columns, importances, log_dir, step=0,top_features=20)

    # Return model and evaluation metrics
    return model, history, test_accuracy, y_test, y_pred, X_train_reshaped, X_test_reshaped
