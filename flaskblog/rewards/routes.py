# -*- coding: utf-8 -*-

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Reward, User, Post
from flaskblog.rewards.forms import RewardForm, DashboardForm, SearchAssociateForm

rewards = Blueprint('rewards', __name__ )

from sqlalchemy import desc

 
@rewards.route('/reward/new' , methods =['GET', 'POST'])
@login_required
def new_reward():   
    form = RewardForm()
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file )
    if form.validate_on_submit():
        reward = Reward(associate_id=form.associate_id.data, category=form.category.data, reward_points=form.reward_points.data, giver=current_user)
        db.session.add(reward)
        current_user.balance = current_user.balance - form.reward_points.data
        associate = User.query.filter_by(email=form.associate_id.data).first()
        associate.earned = associate.earned + form.reward_points.data
        title='@'+str(associate.username)+' has been awarded '+ str(form.reward_points.data)+ ' points'
        content ='Category: '+str(form.category.data)+'\n' + form.reward_comments.data
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your reward has been shared successfully!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        user_email = request.args.get('user_email', None)
        print(user_email)
        form.associate_id.data = user_email
        user = User.query.filter_by(email=user_email).first()
        form.associate_name.data = user.username
        form.balance.data = current_user.balance
        image_file = url_for('static', filename='profile_pics/'+ user.image_file )
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('create_reward.html', title='New Reward', form=form,
                           legend='New Reward', image_file=image_file, counts=counts)

@rewards.route('/reward/search' , methods =['GET', 'POST'])
@login_required
def search_associate():   
    form = SearchAssociateForm()
    if form.validate_on_submit():
        associate = User.query.filter_by(email=form.associate_id.data).first()
        print(associate)    
        return redirect(url_for('rewards.new_reward', user_email = associate.email))
    counts = User.query.order_by(desc(User.earned)).limit(5)
    print(counts)
    return render_template('search_associate.html', title='New Reward', form=form, 
                           legend='Search Associate', counts=counts)


@rewards.route('/dashboard' , methods =['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardForm()
    if request.method == 'GET':
        form.earned.data = current_user.earned
        form.balance.data = current_user.balance
    elif form.validate_on_submit():
        print("2:"+str(form.submit2.data))
        print("1:"+str(form.submit.data))
        if(form.submit.data):
            return "Feature will be added soon"
        elif(form.submit2.data):
            return redirect(url_for('rewards.search_associate'))
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('dashboard.html', title='Dashboard', form=form, 
                           legend='Redeem Points', legend2='Share Points', counts=counts)
