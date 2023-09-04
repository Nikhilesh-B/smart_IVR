from socketIO_client import SocketIO

def on_connect():
    print('Connected to server')

def on_disconnect():
    print('Disconnected from server')

socketIO = SocketIO('localhost', 3001)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)

# Sample form data to send
form_data = {
    'firstName': 'John',
    'lastName': 'Doe',
    'description': 'Sample data',
    'resolved': True,
    'agentName': 'Agent007'
}

# Emitting 'formSubmit' event to the server with the sample form data
socketIO.emit('formSubmit', form_data)

# Keep the client running for testing purposes
socketIO.wait(seconds=10)
