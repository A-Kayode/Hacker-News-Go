from sqlalchemy import func
from . import db

class New_news(db.Model):
    nid= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    itemid= db.Column(db.Integer(), nullable=True)
    ntype= db.Column(db.String(50), nullable=False)
    written_by= db.Column(db.String(255), nullable=False, default="")
    comment_no= db.Column(db.Integer(), default=0)
    created= db.Column(db.DateTime(), nullable=False, default=func.now())
    title= db.Column(db.String(255), nullable=False)
    text= db.Column(db.Text(), nullable=False, default="")
    url= db.Column(db.String(255), nullable=False, default="")
    password= db.Column(db.String(255), nullable=False, default="")
    updated= db.Column(db.Date(), nullable=True)

    def __repr__(self):
        return f"latest news: {self.title}"


class Hacker_jobs(db.Model):
    nid= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    itemid= db.Column(db.Integer(), nullable=True)
    ntype= db.Column(db.String(50), nullable=False)
    written_by= db.Column(db.String(255), nullable=False, default="")
    created= db.Column(db.DateTime(), nullable=False, default=func.now())
    title= db.Column(db.String(255), nullable=False)
    url= db.Column(db.String(255), nullable=False, default="")
    text= db.Column(db.Text(), nullable=False, default="")
    comment_no= db.Column(db.Integer(), default=0)
    password= db.Column(db.String(255), nullable=False, default="")
    updated= db.Column(db.Date(), nullable=True)


class Comments(db.Model):
    com_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    item_id= db.Column(db.Integer(), nullable=False)
    parent_id= db.Column(db.Integer(), nullable=False)
    written_by= db.Column(db.String(255), nullable=False, default="")
    text= db.Column(db.Text(), nullable=False, default="")
    created= db.Column(db.DateTime(), nullable=False)
    level= db.Column(db.Integer(), nullable=False)