from iottalkpy import dan
import socket, threading, sys, json
from flask import Flask
from config import IoTtalk_URL, device_model, device_name, device_addr, username

''' Initialize Flask '''
app = Flask(__name__)

''' TCP/IP Socket '''
processing_connection = None

''' Percentage temporary buffer '''
Result = None

''' on_data to Processing '''
def cmd2processing(msg):
    global processing_connection
    if(processing_connection):
        print("[processing] send msg ", msg)
        processing_connection.send(msg.encode('utf-8'))

''' IoTtalk data handler '''
def on_data(odf_name, data):
    global Result

    print("[da] [data] ", odf_name, data)
    Result = json.loads(data[0])['percentage']

    Percentage = ' '.join(str(elem) for elem in Result)
    cmd2processing("p," + Percentage + ";")

def on_signal(signal, df_list):
    print('[cmd]', signal, df_list)

def on_register():
    dan.log.info('[da] register successfully')

def on_deregister():
    dan.log.info('[da] register fail')

''' IoTtalk registration '''
#device_addr = "{:012X}".format(getnode())
odf_list = [
    ['Result-O', ['string']]
]
context = dan.register(
    IoTtalk_URL,
    on_signal=on_signal,
    on_data=on_data,
    odf_list=odf_list,
    accept_protos=['mqtt'],
    name=device_name,
    id_=device_addr,
    profile={
        'model': device_model,
        'u_name': username
    },
    on_register=on_register,
    on_deregister=on_deregister
)

def toProcessing():
    global  processing_connection
    ''' build socket with Processing '''
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8888))
        server.listen(1)
        #server.settimeout(10)
        print('[sys] Waiting for processing connection')
        (processing_connection, processing_address) = server.accept()
        print('Connection successed! Client (Processing) info: ', processing_connection, processing_address)
    except:
        print('[sys] Create socket failed')
        sys.exit(1)

@app.route('/')
def index():
    return str(Result)

if __name__ == "__main__":
    ''' Build Thread to connect Processing '''
    t = threading.Thread(target=toProcessing, daemon=True)
    t.start()

    app.run()
