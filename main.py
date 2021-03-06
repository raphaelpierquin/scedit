#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Dependencies (on a Ubuntu computer, on other systems you will need to find other ways of finding these) :
  Flask

Loaded remotely:
  ace   (javascript editor from ace.ajax.org)
  jquery

 NB/TODO:
 - security issues in the handling of filenames (both file select and save)
"""

from __future__ import unicode_literals
import io                   # Better alternative for unicode files.
import glob
import string
import datetime
import os
import random

from flask import Flask, request, session, render_template, flash, redirect, url_for
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

import yggdrasil

ENCODING="UTF-8"
JSDIR = os.environ['SRCDIR']

def get_file_content(fname):
    try:
        return io.open(fname, "r", encoding=ENCODING).read()
    except:
        return ""

def logged_in_player():
    if 'yggdrasil' in session:
        return yggdrasil.player_name(session['yggdrasil'])
    else:
        return None

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('username', validators=[DataRequired()])

app = Flask(__name__)
app.wtf_csrf_enabled = False
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return redirect(url_for('edit')) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        response = yggdrasil.authenticate(form.username.data, 
                                          form.password.data)
        if response is not None:
            session['yggdrasil'] = response
            flash('Logged in to Minecraft')
        else:
            flash('Could not log in to Minecraft')

        return redirect(url_for('edit'))

    return render_template(
        'login.html',
        form=form
    )

@app.route('/logout')
def logout():
    if 'yggdrasil' in session and yggdrasil.invalidate(session['yggdrasil']):
        session.pop('yggdrasil', None)
        flash('Logged out')
    return redirect(url_for('edit'))

@app.route("/edit/")
def edit():
    "lists files we might want to edit"

    directories = glob.glob("%s/*/" % (JSDIR,))
    dnames = [ d[len(JSDIR):] for d in directories]
    fnames = {}
    for dn in dnames:
        files = glob.glob("%s%s*.js" % (JSDIR,dn))
        files.sort()
        fnames[dn]= [ f[len(JSDIR):] for f in files]
    return render_template(
        'edit.html',
        filesByDirectory = fnames
    )

@app.route("/edit/file")
def editfile():
    "edit the content of a file"

    fname = request.args.get("file")

    return render_template(
        'editfile_ace.html',
        fname = fname,
        player_name = logged_in_player(),
        content = get_file_content("%s/%s" % (JSDIR, fname))
    )

@app.route('/edit/sfile', methods = ['POST'])
def editfile_submit():
<<<<<<< HEAD
    "Handles save file'"
    if logged_in_player() is None:
        return "", 403
    fname = request.form['fname']
    txt   = request.form['text']
    print "Submitting file %s" % fname
    file = io.open("%s/%s" %(JSDIR, fname), "wt", encoding=ENCODING)
    file.write(unicode(txt))
    file.close()
=======
    "Handles 'save file'"
    print "Submitting new file"
    fname = request.forms['fname']
    txt   = request.forms['text']
    print "  fname", fname, "len", len(txt)

    # create a backup
    tnow = datetime.datetime.now()
    try:
        oldtxt = io.open("%s/%s" %(JSDIR, fname), "r", encoding=ENCODING).read()
        io.open("%s/%s-pre-%s" %(BKDIR, fname.replace('/', '-'), tnow.isoformat()), "w", encoding=ENCODING).write(oldtxt)
    except:
        pass
    # Now overwrite the file we want to save
    io.open("%s/%s" %(JSDIR, fname), "w", encoding=ENCODING).write(unicode(txt,encoding = ENCODING))
>>>>>>> a9e72
    return ""

@app.route("/logfile")
def logfile():
    return render_template(
        'logfile.html',
        content = get_file_content("mcserver.log")
    )


# ------------------------------------------------------------
#
#  Mainstuff
#

<<<<<<< HEAD
if __name__ == "__main__":
    app.run(debug=True)
=======
# Get cork and bottle to cooperate
session_opts = {
    'session.type': 'cookie',
    'session.validate_key': True,
}

app = bottle.default_app()
app = SessionMiddleware(app, session_opts)

# With reloader: automatically reloads the bottle server when the python modules have been updated.
#bottle.run(app=app, reloader=True, host="localhost", port=8090)
bottle.run(app=app, reloader=True, host="0.0.0.0", port=8095)  # listens to all hosts

>>>>>>> a9e72
