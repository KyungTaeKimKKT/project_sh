import datetime

def get_Now() -> str:
    return datetime.datetime.now().strftime('%Y-%m-d %H:%M:%S')

def log_print(msg:str, length:int=400) -> None:
    print (f"{get_Now()} - {msg[:length]}")