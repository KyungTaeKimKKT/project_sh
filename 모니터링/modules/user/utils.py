# def get_IP_Netifaces(ifname):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
import socket, datetime, json, sys, os
import random

TCP_LIVE_START = 50000
TCP_lIVE_END = 65533
TCP_START = 40000
TCP_END   = 49999


def log_print(msg:str, length:int=250) -> None:
    now =  datetime.datetime.now().strftime('%Y-%m-d %H:%M:%S')
    print (f"{now} - {msg[:length]}")


def get_pid_wrte_infojson(pid=str):
    with open('./_info.json', 'r') as f:
        info_contents = json.load(f)

    pid_json = {pid:os.getpid()}

    info_contents.update(pid_json)

    with open('./_info.json', 'w') as f:
        json.dump(info_contents, f, ensure_ascii=False)

def get_IP_Hostname() ->tuple[str|None, str|None, bool]:
    try: 
        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.10.249", 80))
        return ( s.getsockname()[0] , hostname , True)
    except Exception as e:
        print ('Network Error : ', e)
        return ( None, None, False)
        # return (ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'], 'hostname')
   

def get_Now():
    return datetime.datetime.now()

def get_data_from_jsonfile(path):
    with open(path, encoding='utf-8') as file:
        data = json.load(file)    
    return data

def pprint(msg=None):
    strNow = get_Now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{strNow} Line No: {sys._getframe().f_back.f_lineno}: {msg if msg is not None else ''}\n")
          
def print_Traceback(tr, exc_info, msg) :
    print (get_Now().strftime("%Y-%m-%d %H:%M:%S") )
    print ( tr )
    print ( exc_info )
    print ( msg )


def get_TCP_LIVE_Port(start=TCP_LIVE_START, end=TCP_lIVE_END ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    while True:
        tcp_port = random.choice(range(start, end, 2))
        result = sock.connect_ex(('127.0.0.1',tcp_port))
        if result : 
            sock.close()
            return tcp_port

def get_TCP_Port(start=TCP_START, end=TCP_END ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    while True:
        tcp_port = random.choice(range(start, end))
        result = sock.connect_ex(('127.0.0.1',tcp_port))
        if result : 
            sock.close()
            return tcp_port