# install sseclient
import sseclient

messages = sseclient.SSEClient('http://localhost:5000/listen')

for message in messages:
    if message.event != 'test':
        continue
    print(f'{message.event}: {message.data}')
