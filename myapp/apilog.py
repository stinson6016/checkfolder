from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime

from . import db
from .models import Changelog, Computers

class AddChangeLog(Resource):
     def post(self):
          if request.is_json:
               computer = request.json['computer']
               computer_check = Computers.query.filter_by(name=computer).first()
               if not computer_check:
                    new_computer = Computers(name=computer,code=0)
                    db.session.add(new_computer)
                    db.session.commit()
                    computerid = new_computer.id
               else:
                    computerid = computer_check.id
               log = Changelog(type=request.json['type'], 
                               name=request.json['name'],
                               date=datetime.strptime(request.json['date'], '%m/%d/%Y'),
                               time=request.json['time'],
                               computer=computerid)
               db.session.add(log)
               db.session.commit()
               return make_response(jsonify({'id':log.id}), 201)
          else:
               return {'error': 'request must be json'}, 400
