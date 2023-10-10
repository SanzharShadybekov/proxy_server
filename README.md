## Proxy_server
#### Python technical task, proxy server for Hacker News website with micro text modification: original - 'Hello Ivelum', modified 'Hello Ivelum™'.

## Start service locally

* **You need clone project**
```commandline
git clone https://github.com/SanzharShadybekov/tz_proxy_server.git
```
* **Create virtual environment and activate**
```commandline
python3 -m venv venv
. venv/bin/acivate
```
* **Install packages**
```commandline
pip install -r requirements
```
* **Start server, proxy will be available at localhost:8000**
```commandline
python3 proxy.py
```
* **Start test for modifying text**
```commandline
python3 tests.py
```






