
import glob
from pathlib import Path
import os

from flask import Flask, current_app as currentApp, send_file as sendFile
from flask_restx import Api, Resource, Namespace

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, NotFound, NotImplemented
from werkzeug.utils import secure_filename as secureFilename

api = Namespace(
    "System Shutdown",
    description="Actions related to shutting down the API host server") 

def shutdownWindows(minutes=0, cancel=False):
    if cancel:
        return os.system("shutdown /a")
    else:
        return os.system("shutdown /f /s /t {}".format(minutes * 60))

def shutdownLinux(minutes=0, cancel=False):
    if cancel:
        return os.system("shutdown -c")
    else:
        return os.system("shutdown -h +{}".format(minutes))

@api.route("/schedule/<minutesLater>")
class ScheduleShutdown(Resource):
    @api.doc(responses={200: "Shutdown scheduled",
                        400: "Invalid parameters",
                        501: "Unsupported operating system"})
    def get(self, minutesLater: str):
        """Shutdown the server in minutesLater
        
        Parameters
        ----------
        @param minutesLater: int
            Number of minutes later to schedule the shutdown, from 0
            to 60 inclusive.
        """
        try:
            minutesLater = int(minutesLater)
        except ValueError:
            raise BadRequest("Please enter a valid time")

        if not ( 0 < minutesLater < 60 ):
            raise BadRequest("Please enter a time between 0 and 60 inclusive")
            
        if os.name == "posix":
            shutdownLinux(minutesLater)
        elif os.name == "nt":
            shutdownWindows(minutesLater)
        else:
            raise NotImplemented("This operation is not supported")

@api.route("/cancel")
class CancelShutdown(Resource):
    @api.doc(responses={200: "Shutdown cancelled",
                        403: "Forbidden",
                        501: "Unsupported operating system"})
    def get(self):
        if os.name == "posix":
            shutdownLinux(cancel=True)
        elif os.name == "nt":
            shutdownWindows(cancel=True)
        else:
            raise NotImplemented("This operation is not supported")
