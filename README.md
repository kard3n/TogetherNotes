 
# DoTogether

## Installation and Startup
For the app to be able to start `redis` must be installed and running.
Under Arch Linux this could be done using the following commands:
```bash
yay -S redis-server
sudo systemctl start redis
```

With a python environment set up and running, the dependencies can be installed as follows:
```bash
pip install -r requirements.txt
```

The app can then be launched with `python app.py`. After, a server should be availbale at `http://127.0.0.1:5000`
