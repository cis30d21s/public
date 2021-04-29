# Home Security Dashboard

## Install Python Libraries

On Raspberry Pi, run:

```bash
python3 -m pip install --upgrade flask flask-cors
```

## Test Server-Side Events

```bash
# start `hsd-service`
python3 service/hsd-service.py

# generate messages in another terminal
python3 service/test-ping.py

# listen to messages in another terminal
python3 -m pip install sseclient
python3 service/test-listener.py
```
