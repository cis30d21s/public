# Home Security Dashboard

## Install Python Libraries

Additional libraries are needed to run the HSD service.

On Raspberry Pi, run:

```bash
python3 -m pip install --upgrade flask flask-cors
```

## Test Server-Side Events

Test programs can be used to test server-side events without UI.

On Raspberry Pi, run:

```bash
# start `hsd-service`
python3 service/hsd-service.py

# generate messages in another terminal
python3 service/test-ping.py

# listen to messages in another terminal
python3 -m pip install sseclient
python3 service/test-listener.py
```
