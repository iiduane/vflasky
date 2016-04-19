#!/usr/bin/python
# -*- coding: utf-8 -*-  
import os
from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
## add
#from wtforms import *
# 不能导入 * 又导入包含的类 不然的话，会出现某些方法找不到的问题，可能被重名类覆盖掉了
from wtforms import DateField, DateTimeField, StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://vpush:123@192.168.2.70/plinedb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class BadDeviceForm(Form):
    #id = IntegerField('',)
    #pdate = DateTimeField('Input Date:', validators=[Required()])
    pcb_num = StringField('Bad devices PCB:', validators=[Required()])
    imei_num = StringField('Bad devices IMEI:', validators=[Required()])
    virtual_num = StringField('Virtual Number:', validators=[Required()])
    selfdef_num = StringField('Self define number:', validators=[Required()])
    ## start 6 
    prj_name = StringField('Project name:', validators=[Required()])
    prj_node = StringField('Project node:', validators=[Required()])
    badDevice_source = StringField('Bad device source:', validators=[Required()])
    test_strid = StringField('Test string id:', validators=[Required()])
    plinebuild = StringField('product line build name:', validators=[Required()])
    softversion = StringField('Software version:', validators=[Required()])
    agestress_class = StringField('age stress test class:', validators=[Required()])
    issue_time = DateTimeField('issue happened time')
    bad_present = StringField('Bad device present:', validators=[Required()])
    gongcheng_man = StringField('Bad devices IMEI:', validators=[Required()])
    qa_makesure = StringField('Qa make sure what:', validators=[Required()])
    bug_num = StringField('Bad devices BUG num:', validators=[Required()])

    submit = SubmitField('Submit')

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    formp = BadDeviceForm() 
    ##if form.validate_on_submit(): # and formp.validate_on_submit():
    if formp.validate_on_submit():
        user = User.query.filter_by(username=formp.pcb_num.data).first()
    #    if user is None:
    #        user = User(username=form.name.data)
    #        db.session.add(user)
    #        session['known'] = False
    #    else:
    #        session['known'] = True
    #    session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', formp=formp, name=session.get('name'),
                           known=session.get('known', False))

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    form = NameForm()
    ##if form.validate_on_submit(): # and formp.validate_on_submit():
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('welcome'))
    return render_template('welcome.html', form=form, name=session.get('name'),known=session.get('known', False))

if __name__ == '__main__':
    db.create_all()
    print 'after create tables;'
    manager.run()
