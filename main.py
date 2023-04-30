from flask import Flask, render_template, redirect, make_response, jsonify
from data import users_resource
from data import jobs_resource
from data.db_session import *
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.jobs import JobsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    db_sess = create_session()
    jobs = db_sess.query(Jobs, User)
    jobs = jobs.join(User, Jobs.team_leader == User.id)
    jobs = jobs.all()
    return render_template("index.html", jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Пользователь уже существует")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return make_response(render_template('register.html', title="Регистрация", form=form))


@app.route('/addJobs', methods=['GET', 'POST'])
@login_required
def addJobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = create_session()
        jobs = Jobs(
            team_leader=current_user.id,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data,
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('editJobs.html', title='Добавление работы', heading="Добавление работы", form=form)


@app.route('/editJobs/<int:jobId>', methods=['GET', 'POST'])
@login_required
def editJobs(jobId):
    db_sess = create_session()
    jobs = ()
    if current_user.id != 1:
        jobs = db_sess.query(Jobs).filter(Jobs.id == jobId, Jobs.team_leader == current_user.id).all()
    else:
        jobs = db_sess.query(Jobs).filter(Jobs.id == jobId).all()
    if len(jobs) == 0:
        return redirect('/')
    else:
        jobs = jobs[0]
    form = JobsForm(
        job=jobs.job,
        work_size=jobs.work_size,
        collaborators=jobs.collaborators,
        start_date=jobs.start_date,
        end_date=jobs.end_date,
        is_finished=jobs.is_finished
    )
    if form.validate_on_submit():
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = form.start_date.data
        jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    return render_template('editJobs.html', title='Редактирование работы', heading="Редактирование работы", form=form)


@app.route('/deleteJobs/<int:jobId>', methods=['GET', 'POST'])
@login_required
def deleteJobs(jobId):
    db_sess = create_session()
    jobs = ()
    if current_user.id != 1:
        jobs = db_sess.query(Jobs).filter(Jobs.id == jobId, Jobs.team_leader == current_user.id).all()
    else:
        jobs = db_sess.query(Jobs).filter(Jobs.id == jobId).all()
    if len(jobs) == 0:
        return redirect('/')
    else:
        jobs = jobs[0]
    db_sess.delete(jobs)
    db_sess.commit()
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
