import datetime
from flask_restful import abort, Resource
from flask import jsonify
from .users import User
from . import db_session
from .users_resource_parsers import put_parser, post_parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email', 'modified_date'))})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        for key in args.keys():
            if key in dir(user) and args[key]:
                setattr(user, key, args[key])
        user.modified_date = datetime.datetime.utcnow()
        try:
            session.commit()
        except Exception as e:
            abort(409, message=f"Что-то пошло не так 0_0")
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        user = User()
        for key in args.keys():
            if key in dir(user) and args[key]:
                setattr(user, key, args[key])
        user.modified_date = datetime.datetime.utcnow()
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            abort(409, message=f"Email {args['email']} уже существует")
        return jsonify({'success': 'OK'})

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users':
                        [user.to_dict(
                            only=('id', 'surname', 'name', 'age', 'position',
                                  'speciality', 'address', 'email', 'modified_date')) for user in users]})
