import socket
import json
import time
import sys
import os

# --------------------- A L L   C O N S T A N T S --------------------------

FORMAT = "utf-8"
DISCONNECTED_MSG = "! DISCONNECTED"
SIZE = 1024
TEMP_DATABASE = {}
CMDL_ARGS = sys.argv

# PORT AND IP 
PORT = 19725
IP =  "4.tcp.ngrok.io"
ADDR = (IP,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# ----------------------- F U N C T I O N S -------------------------------
def get():
    PROTOCALL = "GET"
    client.send(PROTOCALL.encode(FORMAT))
    string_of_json = client.recv(SIZE).decode(FORMAT)
    TEMP_DATABASE = json.loads(string_of_json)
    return TEMP_DATABASE
def post(msg):
    PROTOCALL = "POST"
    client.send(PROTOCALL.encode(FORMAT))

    response1 = client.recv(SIZE).decode(FORMAT)
    if (response1 == "300"):
        client.send(msg.encode(FORMAT))
        response2 = client.recv(SIZE).decode(FORMAT)
        return (response2 == "201")
    else:
        return 0
def clear():
    PROTOCALL = "CLEAR"
    client.send(PROTOCALL.encode(FORMAT))
    response = client.recv(SIZE).decode(FORMAT)
    return (response == "202")

def disconnect():
    client.send(DISCONNECTED_MSG.encode(FORMAT))

def help():
    msg  = '''
# COMMANADS :

* FORMAT -
note [-OPTIONS-] [-OPTIONS-]

* OPTIONS -
1. [String]             : Any String Within Double Quotes, that will be inserted into NOTEPAD
2. -r -a                : Remove All the notes from the "ONLINE NOTEPAD"
3. -r -no.              : Remove the perticular Note from NOTEPAD with given index
4. -s -a                : Show All the Notes present in the NOTEPAD
5. -s                   : Show 10 recent note (By Default)
6. -s -no.              : Show recent notes of given number
7. -up -filename.txt    : Upload the notes as a file.(*)
8. -help                : How to use the commnads

* EXTRA'S -
(*) - Coming Soon (Bulid In Progress)
'''
    print(msg)

def getNotesArray(num=0):
    json_notes_obj = get()
    if json_notes_obj:
        notes_arr = json_notes_obj["notes"]
        notes_arr.reverse()
        notes_arr_len = len(notes_arr)

        if (num !=0):
            return notes_arr[:num]
        else:
            return notes_arr
    else:
        print("\n:: Notepad- Error In Retriving The Data !\n")
        return []

# ---------------- S T A R T P O I N T ---------------
def main():

    # If No argument passed 
    if (len(CMDL_ARGS) == 1):
        help()
        disconnect()

    # Showing the notes
    elif ((len(CMDL_ARGS) >= 2) and (CMDL_ARGS[1]) == "-s" ):

        # Show All Notes
        notes_arr = []

        if (len(CMDL_ARGS) == 2):
            notes_arr = getNotesArray(10)
        elif (CMDL_ARGS[2] == "-a"):
            notes_arr = getNotesArray()
        elif (CMDL_ARGS[2].isnumeric()):
            num = int(CMDL_ARGS[2])
            notes_arr = getNotesArray(num)
        else :
            print("\n:: Notepad - Please Enter The Commands Correctly !\n")
            return

        notes_arr_len = len(notes_arr)
        print("\n* Your Notes :\n")
        for i in range(notes_arr_len):
            print(str(i+1) + ") " + notes_arr[i])
        disconnect()

    # Removing the notes
    elif ((len(CMDL_ARGS) >= 2) and (CMDL_ARGS[1]) == "-r" ):
        if (len(CMDL_ARGS) == 2):
            print("\n:: Notepad - Please Enter The Commands Correctly !\n")
        elif (CMDL_ARGS[2] == "-a"):
            clear()
            print("\n:: Notepad - All Notes Deleted Successfully ! \n")
        else:
            print("\n:: Notepad - Please Enter The Commands Correctly !\n")
        disconnect()

    # Providing The HELP for user
    elif (CMDL_ARGS[1] == "-h"):
        help()
        disconnect()

    # Adding the Note into Notepad 
    elif ((len(CMDL_ARGS) == 2)):
        response = post(CMDL_ARGS[1])
        if response:
            print("\n:: Notepad - Note Added Successfully in NOTEBOOK.\n")
        else:
            print("\n:: Notepad - Internal Problem | Please Try Again \n")
        disconnect()

    # Giving Error Message 
    else:
        print("\n:: Notepad - Please Enter The Commands Correctly !\n")
        disconnect()

main()
