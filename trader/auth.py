from dotenv import load_dotenv, dotenv_values
import os

is_live = False
has_prompted = False

def str_to_bool(s):
    if s.lower() in ['true', '1', 't', 'y', 'yes']:
        return True
    elif s.lower() in ['false', '0', 'f', 'n', 'no']:
        return False
    else:
        raise ValueError(f"Cannot convert {s} to boolean, please input a formattable string")

def auth_deets(is_live, type_:str,):
    global has_prompted
    if not has_prompted:
        is_live = str_to_bool(s=input("Would you like to run on your LIVE account? if n then will be DEMO (y/n)"))
        has_prompted = True
    if is_live:
        if type_ == "token":
            access_token=os.getenv("live_token")# you need token here generated from OANDA account for LIVE
            return access_token
        elif type_ == "id":
            accID = os.getenv("live_id") #my account ID here from oanda for LIVE
            return accID
    else:
        if type_ == "token":
            access_token=os.getenv("demo_token") # DEMO TOKEN
            return access_token
        elif type_ == "id":
            accID = os.getenv("demo_id") #my acc ID for the DEMO
            return accID