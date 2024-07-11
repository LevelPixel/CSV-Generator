import webbrowser
import subprocess
import time

def run_flask_app():
    subprocess.Popen(['python', 'main.py'])

def open_browser(url):
    webbrowser.open(url)

if __name__ == "__main__":
    run_flask_app()
    time.sleep(2)
    open_browser("http://127.0.0.1:5000/")