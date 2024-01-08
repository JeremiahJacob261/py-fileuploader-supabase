import os
from supabase import create_client, Client
import random
import string
import json
import tkinter as tk
from tkinter import filedialog
import requests
import re
root = tk.Tk()
root.withdraw()
global auth


def generate_random_string(length):
   letters_and_digits = string.ascii_letters + string.digits
   result_str = ''.join(random.choice(letters_and_digits) for i in range(length))
   return result_str

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
url = "https://hnefhmxnthlskxmggirm.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhuZWZobXhudGhsc2t4bWdnaXJtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMjgzMzkwMiwiZXhwIjoyMDE4NDA5OTAyfQ.kY_PoT1S6Yr8S3IbFnFfiw-M-v4fA9zy4rJaFJejskg"
supabase: Client = create_client(url, key)

def getfie():
    try:
        filepath = filedialog.askopenfilename()
        print(filepath)
    except Exception as e:
        print(e)
    return filepath

def active(auth):
    action = input("1. Upload Files \n 2. Download or List Files \n 3.Exit this program \n")
    if (int(action) == 1):
        print("Getting file location")
        try:
            def sanitize_filename(filename):
                return re.sub(r'\W+', '_', filename)

            with open(getfie(), 'rb') as f:
                print(f)
                filename = sanitize_filename(os.path.basename(getfie()))
                supabase.storage.from_("pystore").upload(file=f, path=filename,
                                                         file_options={"content-type": "*"})
                print("Uploading file")
                res = supabase.storage.from_('pystore').get_public_url('filename')
                data, count = supabase.table('pydata').insert({"token": auth,"filename":filename,"fileurl":res}).execute()
                print("File Uploaded")
        except Exception as e:
            print(e)
    elif (int(action) == 2):
        data, count = supabase.table('pydata').select('*').eq('token', auth).execute()
        listed = data[1]
        # for l in listed:
        #     print(list[list.index(l)] + ". " +l['filename'])
        for i, item in enumerate(listed, start=1):
            print(f"{i}. {item['filename']}")
            selection = int(input("Choose a file by entering its number: "))

            selected_file = listed[selection - 1]
            file_url = selected_file['fileurl']
            cwd = os.getcwd()
            print(f"The URL of the selected file is: {file_url}")
            print("Downloading ...")
            response = requests.get(file_url)

            local_file_path = os.path.join(cwd, item['filename'])

            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            print("Downloaded")
            active(auth)
    elif (int(action) == 3):
        print("Thanks for using this program, Please, Don't forget to give a STAR")
    else:
        print("Invalid input")
        active(auth)
def start():
    print("Welcome to Python File Uploader: built by Jerrydev")
    print("We will required you to create an account or login to save your files: ")
    user = input("Login/Signup (l / s) : ")
    if(user == "l"):
        auth = input("Please input your token : ")
        print("please wait ...")
        data, count = supabase.table('pyusers').select('token').eq('token', auth).execute()
        if(data[1][0]['token']):
            print("welcome, great one")
            active(data[1][0]['token'])
        else:
            print("Wrong Token, please create an account or input the right token! ")
    elif(user == 's'):
        print("Please wait while we generate a token for you : ")
        tokenizer = generate_random_string(20);
        print("this is your token, it will be used for logins : " + tokenizer)
        ath = {"token": tokenizer}
        with open('auth.json', 'w') as fp:
            json.dump(ath, fp)
        data, count = supabase.table('pyusers').insert({"token": tokenizer}).execute()
    else:
        print("Invalid Input")


start()
# root.mainloop()