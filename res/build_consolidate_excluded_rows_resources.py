from db_models.models import ConsolidateMarkData,ConsolidateExcludeTransactionsDocuments,Projects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import json
import subprocess
from settings import ENGINE_PATH


class BuildConsolidateExcludedRowsDocumentsListResource(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            project_id = json_data['project_id']
            project = session.query(Projects).filter(Projects.id==project_id).first()

            if (not project):
                return abort(400,error='Project not found')

            user_id = project.user_id
            consolidate_marks = session.query(ConsolidateMarkData).filter(ConsolidateMarkData.project_id==project_id).first()

            consolidate_marks_data = json.loads(consolidate_marks.data)
            for member in consolidate_marks_data['members']:
                name = member['name']

                balance_header = member['balance_data']['headers']
                balance_data = member['balance_data']['data']

                opiu_header = member['opiu_data']['headers']
                opiu_data = member['opiu_data']['data']

                odds_header = member['odds_data']['headers']
                odds_data = member['odds_data']['data']


                model = {
                    'name':name,
                    'balance_header':balance_header,
                    'balance_data': balance_data,
                    'opiu_header': opiu_header,
                    'opiu_data': opiu_data,
                    'odds_header': odds_header,
                    'odds_data': odds_data,
                }

                data = json.dumps(model)

                transaction_document = ConsolidateExcludeTransactionsDocuments(project_id,user_id,name,data)
                session.add(transaction_document)
                session.commit()



            t=0

            return None, 201
        except Exception as e:
            abort(400, message="Error while adding record Consolidate Mark")
