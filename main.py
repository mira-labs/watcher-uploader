import os
import sys
import time
from datetime import datetime

import pysftp
from dotenv import load_dotenv
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

# Takes environment variables from .env
# Code of the application, which uses environment variables
# (e.g. from `os.environ` or `os.getenv`) as if they came from the actual environment.
load_dotenv()
CWD = os.getcwd()


def current_time():
    """Takes current time and returns formatted output for logging purposes"""
    cur_time = datetime.now()
    return "[" + cur_time.strftime('%Y-%m-%d %H:%M:%S') + "]: "


def upload(file: str):
    """Uploads a file through SFTP
    Parameters
        ----------
        file : str
            The name of the file
            """
    print(current_time() + 'Uploading file: ' + file)
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        sftp_client = pysftp.Connection(host=os.getenv('HOST'), port=int(os.getenv('PORT')), username=os.getenv('USER'),
                                        password=os.getenv('PASSWORD'), cnopts=cnopts)
        try:
            sftp_client.cwd(os.getenv('REMOTE_PATH'))
            sftp_client.put(file, preserve_mtime=True)
            print(current_time() + 'File: ' + file + ' uploaded successfully')
        except:
            ex = sys.exc_info()
            print(current_time() + 'FAILED: ' + file + "{0}".format(ex))
    except:
        e = sys.exc_info()
        print("Exception: {0}".format(e))


def on_created(event):
    print(f"{event.src_path} has been created")


def on_deleted(event):
    print(f"{event.src_path} delete!")


def on_modified(event):
    print(f"{event.src_path} has been modified")
    upload(event.src_path)


def on_moved(event):
    print(f"{event.src_path} has been moved")
    upload(event.src_path)


if __name__ == "__main__":

    my_event_handler = PatternMatchingEventHandler(os.getenv('PATTERNS'), os.getenv('IGNORE_PATTERNS'),
                                                   os.getenv('IGNORE_DIRECTORIES'), os.getenv('CASE_SENSITIVE'))
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, os.getenv('PATH'), recursive=go_recursively)
    my_observer.start()
    print('Observer started')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
