from datetime import datetime
import requests
from flask import render_template, redirect, flash, request, abort
from flask_sqlalchemy import Pagination
from .. import app, db, scheduler
from ..models import *



@app.route('/test/')
def test_route():
    nn_obj= requests.get('https://hacker-news.firebaseio.com/v0/item/269883.json')
    nn= nn_obj.json()

    return f"{nn}"


@app.route('/')
def home():
    return redirect('/news/all/')


@app.route('/news/<string:filtera>/')
def latest_news(filtera):
    pageno= request.args.get('page', 1)
    if filtera == 'all':
        lnpageobj= New_news.query.order_by(New_news.created.desc()).paginate(int(pageno), per_page=15)
        lname= 'news/all'
    elif filtera == 'askhacker':
        lnpageobj= New_news.query.filter(New_news.title.like('Ask Hn:%')).order_by(New_news.created.desc()).paginate(int(pageno), per_page=15)
        lname= 'news/askhacker'
    elif filtera == 'showhacker':
        lnpageobj= New_news.query.filter(New_news.title.like('Show Hn:%')).order_by(New_news.created.desc()).paginate(int(pageno), per_page=15)
        lname= 'news/showhacker'


    return render_template('latest.html', npo=lnpageobj, lname=lname, mname="New_news", stype='news')


@app.route('/jobs/')
def jobs():
    pageno= request.args.get('page', 1)
    jbpageobj= Hacker_jobs.query.order_by(Hacker_jobs.created.desc()).paginate(int(pageno), per_page=15)

    return render_template('latest.html', npo=jbpageobj, lname='jobs', mname="Hacker_jobs", stype='jobs')


@app.route('/item/<string:model>/<int:nid>/<int:itemid>/')
def display_news(model, nid, itemid):
    try:
        cname= eval(model)
    except:
        abort(404)
    #retrieve the specific news item
    nitem= cname.query.get(nid)

    #retrieve the comments of the news item
    comm= Comments.query.filter(Comments.parent_id == itemid).all()

    return render_template('display_news.html', nitem=nitem, comm=comm)


@app.route('/search/')
def search():
    #retrieve search parameters
    stext= request.args.get('sitem')
    stype= request.args.get('stype')
    page= request.args.get('page', 1)

    #choose model to use based on search type
    if stype == 'news':
        model= New_news
        modelname= "New_news"
    elif stype == 'jobs':
        model= Hacker_jobs
        modelname= "Hacker_jobs"
    
    #splitting the inputted search text into individual words
    stextlist= stext.split(' ')

    #getting records based on exact search sentence
    senrecs= model.query.filter((model.title == stext) | (model.text == stext)).all()
    #getting records based on the words in the search parameter
    textrecs= []
    for i in stextlist:
        temptr= model.query.filter((model.title.like('%'+i+'%')) | (model.text.like('%'+i+'%'))).all()
        textrecs.extend(temptr)

    #merging all results into a single list of records
    tempres= []
    tempres.extend(senrecs)
    tempres.extend(textrecs)
    resrec= []
    for i in tempres:
        if i not in resrec:
            resrec.append(i)
    

    #paginate the result
    #first determine the start and end indexes for each page
    start= (int(page) - 1) * 15
    end= start + 15
    #use index to pick the result needed per page
    resrecpg= resrec[start:end]
    result= Pagination(query=None, page=int(page), per_page=15, total=len(resrec), items=resrecpg)
    sp= 1
    
    return render_template('search.html', npo=result, lname='search', sitem=stext, stype=stype, sp=sp, mname=modelname)