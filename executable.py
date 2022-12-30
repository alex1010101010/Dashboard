import time
from selenium import webdriver
import subprocess
import threading as thr
import os 

# Kill the server if a dash app is already running
def kill_server():
    subprocess.run("lsof -t -i tcp:8080 | xargs kill -9", shell=True)

#start dash app executable in different thread
def start_dash_app_frozen():
    os.system('test')


# Start the driver
# def start_driver():
#     driver = webdriver.Chrome()
#     time.sleep(5) # give dash app time to start running
#     driver.get("http://localhost:8080/") # go to the local server
    

def exe():
    kill_server() # in case app is already running stop it
    thread = thr.Thread(target=start_dash_app_frozen) 
    thread.start() # start dash app on port
    # start_driver() # open browser window and go to url of dash app
    
    
if __name__ == '__exe__':
    exe()