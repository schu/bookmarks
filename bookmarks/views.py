# -*- coding: utf-8 -*-

from bookmarks import app, db
from bookmarks.forms import BookmarkForm, DummyForm, LoginForm, TagForm
from bookmarks.models import Bookmark, Tag, User
from flask import abort, flash, redirect, render_template, request, url_for
from flask.ext.login import (current_user, login_required, login_user,
                             logout_user)
from sqlalchemy.exc import IntegrityError


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'%s - %s' % (
                getattr(form, field).label.text, error), 'error')


@app.route('/')
def index():
    if request.args.get('tag'):
        tag = Tag.query.filter_by(name=request.args['tag']).first()
        if not tag:
            flash('Tag "%s" does not exist.' % request.args['tag'], 'error')
            return redirect(url_for('index'))
        if not tag.bookmarks:
            flash('No Bookmarks for "%s".' % request.args['tag'], 'error')
            return redirect(url_for('index'))
        return render_template('index.html', bookmarks=tag.bookmarks)
    return render_template('index.html',
            bookmarks=Bookmark.query.order_by(Bookmark.url).all())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = app.auth_handler(form.mail.data, form.password.data)
        if not user:
            flash('Invalid login.', 'error')
            return render_template('login-form.html', form=form)
        login_user(user, remember=True)
        user.set_last_login()
        def next_url(url):
            try: return url_for(url)
            except: return url
        goto = next_url(request.args.get('next')) or url_for('index')
        return redirect(goto)
    flash_errors(form)
    return render_template('login-form.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/<int:id>')
def bookmark_show(id):
    bookmark = Bookmark.query.filter_by(id=id).first()
    if not bookmark:
        return abort(404)
    return render_template('bookmark.html', bookmark=bookmark)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def bookmark_new():
    form = BookmarkForm(request.form)
    if form.validate_on_submit():
        try:
            bookmark = Bookmark(form.url.data,
                        form.title.data,
                        description=form.description.data,
                        tags=form.tags.data,
                        public=form.public.data)
            db.session.add(bookmark)
            db.session.commit()
        except IntegrityError:
            flash(u'Boomark for "%s" exists already.' % form.url.data,
                    'error')
            return render_template('bookmark-form.html', form=form)
        flash(u'Done!')
        return redirect('%d' % bookmark.id)
    flash_errors(form)
    return render_template('bookmark-form.html', form=form)


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def bookmark_edit(id):
    bookmark = Bookmark.query.filter_by(id=id).first()
    if not bookmark:
        return abort(404)
    form = BookmarkForm(request.form, obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.add(bookmark)
        db.session.commit()
        flash(u'Done!')
        return redirect('%d' % bookmark.id)
    flash_errors(form)
    return render_template('bookmark-form.html', form=form)


@app.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def bookmark_delete(id):
    bookmark = Bookmark.query.filter_by(id=id).first()
    if not bookmark:
        return abort(404)
    form = DummyForm()
    if form.validate_on_submit():
        db.session.delete(bookmark)
        db.session.commit()
        flash(u'Deleted.')
        return redirect(url_for('index'))
    flash_errors(form)
    return render_template('bookmark-delete.html', bookmark=bookmark, form=form)


@app.route('/tags')
@login_required
def tags():
    return render_template('tags.html', tags=Tag.query.all())


@app.route('/tag/new', methods=['GET', 'POST'])
@login_required
def tag_new():
    form = TagForm(request.form)
    if form.validate_on_submit():
        try:
            tag = Tag(form.name.data)
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            flash(u'Tag "%s" exists already.' % form.name.data,
                    'error')
            return render_template('tag-form.html', form=form)
        flash(u'Done!')
        return redirect(url_for('tags'))
    flash_errors(form)
    return render_template('tag-form.html', form=form)


@app.route('/tag/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def tag_edit(id):
    tag = Tag.query.filter_by(id=id).first()
    if not tag:
        return abort(404)
    form = TagForm(request.form, obj=tag)
    if form.validate_on_submit():
        form.populate_obj(tag)
        db.session.add(tag)
        db.session.commit()
        flash(u'Done!')
        return redirect(url_for('tags'))
    flash_errors(form)
    return render_template('tag-form.html', form=form)


@app.route('/tag/<int:id>/delete')
@login_required
def tag_delete(id):
    tag = Tag.query.filter_by(id=id).first()
    if not tag:
        return abort(404)
    if tag.bookmarks:
        flash('Cannot delete tag "%s".' % tag.name, 'error')
        return redirect(url_for('tags'))
    db.session.delete(tag)
    db.session.commit()
    flash(u'Deleted.')
    return redirect(url_for('tags'))


@app.route('/apidoc')
@login_required
def apidoc():
    return render_template('apidoc.html')

@app.errorhandler(404)
def http404(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def http403(e):
    return render_template('403.html'), 403
