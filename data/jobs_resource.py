from flask_restful import abort, Resource
from flask import jsonify
from .jobs import Jobs
from . import db_session
from .jobs_resource_parsers import put_parser, post_parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size',
                  'collaborators', 'start_date', 'end_date', 'is_finished'))})

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        for key in args.keys():
            if key in dir(job) and args[key]:
                setattr(job, key, args[key])
        try:
            session.commit()
        except Exception as e:
            abort(409, message=f"Что-то пошло не так 0_0")
        return jsonify({'success': 'OK'})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        job = Jobs()
        for key in args.keys():
            if key in dir(job) and args[key]:
                setattr(job, key, args[key])
        try:
            session.add(job)
            session.commit()
        except Exception as e:
            abort(409, message=f"Что-то пошло не так 0_0")
        return jsonify({'success': 'OK'})

    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs':
            [job.to_dict(
                only=('id', 'team_leader', 'job', 'work_size',
                      'collaborators', 'start_date', 'end_date', 'is_finished')) for job in jobs]})
