import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import json
import os
from dataclasses import dataclass


# Create a new client and connect to the server

@dataclass
class EnvironmentVariable:
    uri:str = os.getenv("uri")



# Object of data class
env_var = EnvironmentVariable()

client = MongoClient(env_var.uri, server_api=ServerApi('1'))
