# -*- coding: utf-8 -*-
from flask import render_template, request, Blueprint
from flaskblog.models import Post, User
from flask_login import login_required

main = Blueprint('main', __name__ )

from sqlalchemy import desc

@main.route('/')
@main.route('/home')
def home():
   page = request.args.get('page', 1, type=int)
   posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
   counts = User.query.order_by(desc(User.earned)).limit(5)
   return render_template('home.html', posts=posts, counts=counts)

