from db_models.models import Log
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import and_
import base64
import  copy
import datetime


def add_log(message):
    try:
        log =Log(message)
        session.add(log)
        session.commit()
        pass
    except Exception as e:
        session.rollback()

        pass
