#!/usr/bin/env python3
from flask import Blueprint
from flask_restx import Api, Resource, Namespace

from .shutdown import api as shutdownApi


def addSystemNamespacesToApi(api):
    api.add_namespace(shutdownApi, path="/system/shutdown")
