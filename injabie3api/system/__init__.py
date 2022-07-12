#!/usr/bin/env python3
from flask import Blueprint
from flask_restx import Api, Resource, Namespace

from .shutdown import api as shutdownApi

bp = Blueprint("system", __name__)
api = Api(bp, description="System-related operations")
api.add_namespace(shutdownApi, path="/shutdown")
