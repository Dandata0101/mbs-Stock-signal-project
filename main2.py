from flask import Flask, request, Response
import os
from waitress import serve
import subprocess
from dotenv import load_dotenv
import requests
from flask import Flask, request, render_template, jsonify, session, url_for, flash, redirect,send_file

# Set matplotlib to use 'Agg' backend before any other matplotlib imports
import matplotlib
matplotlib.use('Agg')

# Load environment variables
load_dotenv()

app = Flask(__name__)

def start_tensorboard(logdir, port=6006):
    """
    Start TensorBoard in a subprocess, making it accessible over the network.
    :param logdir: Directory where TensorBoard will read logs.
    :param port: Port on which TensorBoard will run.
    """
    command = ['tensorboard', '--logdir', logdir, '--port', str(port), '--bind_all']
    subprocess.Popen(command)

@app.route('/')
def show_tensorboard():
    # Dynamically generate the TensorBoard URL based on its port
    tensorboard_port = 6006  # Ensure this matches the port used in start_tensorboard
    tensorboard_url = f'http://localhost:6006'
    return render_template('tensor.html', tensorboard_url=tensorboard_url)

if __name__ == '__main__':
    # Initialize and start TensorBoard
    logdir = 'logs/fit'
    tensorboard_port = 6006  # This can be any port that's free on your system
    start_tensorboard(logdir, tensorboard_port)

    # Configure the Flask app's debug mode based on the FLASK_DEBUG environment variable
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']

    # Get the port number from the PORT environment variable for the Flask app
    port = int(os.getenv('PORT', 8000))

    # Serve the Flask app with Waitress on the specified host and port
    serve(app, host="0.0.0.0", port=port)