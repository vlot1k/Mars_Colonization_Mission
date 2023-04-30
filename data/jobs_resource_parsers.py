from flask_restful import reqparse
from datetime import datetime

put_parser = reqparse.RequestParser()
put_parser.add_argument('team_leader',   required=False, type=int)
put_parser.add_argument('job',           required=False, type=str)
put_parser.add_argument('work_size',     required=False, type=int)
put_parser.add_argument('collaborators', required=False, type=str)
put_parser.add_argument('start_date',    required=False, type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
put_parser.add_argument('end_date',      required=False, type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
put_parser.add_argument('is_finished',   required=False, type=bool)

post_parser = reqparse.RequestParser()
post_parser.add_argument('team_leader',   required=True, type=int)
post_parser.add_argument('job',           required=True, type=str)
post_parser.add_argument('work_size',     required=True, type=int)
post_parser.add_argument('collaborators', required=True, type=str)
post_parser.add_argument('start_date',    required=True, type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
post_parser.add_argument('end_date',      required=True, type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
post_parser.add_argument('is_finished',   required=True, type=bool)
