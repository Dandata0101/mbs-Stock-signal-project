import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import interact
import mplcursors

sns.set_theme(style="whitegrid")  # Apply Seaborn theme

def plot_model_loss(loss_history, val_loss_history=None, title='Model Loss', xlabel='Epoch', ylabel='Loss'):
    plt.figure(figsize=(10, 6))
    plt.plot(loss_history, label='Train Loss', marker='o')
    if val_loss_history is not None:
        plt.plot(val_loss_history, label='Validation Loss', marker='s')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()

    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"Epoch: {sel.target.index + 1}\nLoss: {sel.target[1]:.4f}"))
    plt.show()

# Function to plot confusion matrix
def plot_confusion_matrix(y_true, y_pred, classes=['Actual 0', 'Actual 1'], title='Confusion Matrix'):
    conf_matrix = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Predicted 0', 'Predicted 1'], yticklabels=classes)
    plt.title(title)
    plt.show()

# Function to make confusion matrix plotting interactive
def interactive_confusion_matrix(y_test, y_pred):
    def wrapper(classes, title):
        # Splitting the classes string into a list for the confusion matrix
        class_list = classes.split(',')
        plot_confusion_matrix(y_test, y_pred, classes=class_list, title=title)
    
    interact(wrapper,
             classes=widgets.Text(value='Actual 0, Actual 1', description='Classes:', continuous_update=False),
             title=widgets.Text(value='Confusion Matrix', description='Title:', continuous_update=False))
