from email import message
import json
from datetime import datetime, date
from flask import render_template, redirect, flash, request, abort, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from .. import app, db
from ..models import *


#api to get the list of news items. Mandatory filter is 'newstype' and it's value includes 'jobs', 'news', 'askhacker', showhacker'. Optional filters include 'written_by' and 'posted_on' whose values are strings.
# Posted_on filter must be in the format yyyy-mm-dd
# Comments are not retrieved also.
# Can also optionally specify the number of records you want retrieved. If left empty, all records are retrieved. Field to use is 'no' and it's value is a numerical number.
@app.route('/api/v1.0/getnews/')
def get_news():
    #retrieve the data from the request
    if request.is_json:
        requestdatadic= request.get_json()
        ntype= requestdatadic.get('newstype')
        posted= requestdatadic.get('posted_on')
        writer= requestdatadic.get('written_by')
        rec_no= requestdatadic.get('no')
    else:
        ntype= request.args.get('newstype')
        posted= request.args.get('posted_on')
        writer= request.args.get('written_by')
        rec_no= request.args.get('no')
    
    #check if the required fields were passed correctly through the request
    if ntype == None:
        return jsonify(status=0, message="Error. Required fields missing")
    elif ntype != 'jobs' and ntype != 'news' and ntype != 'askhacker' and ntype != 'showhacker':
        return jsonify(status=0, message="Error. Unrecognised arguments for required fields.", data=ntype)
    else:
        titler= None
        if ntype == 'jobs':
            model= Hacker_jobs
        elif ntype == 'news':
            model = New_news
        elif ntype == 'askhacker':
            model= New_news
            titler= 'Ask Hn:%'
        elif ntype == 'showhacker':
            model= New_news
            titler= 'Show HN:%'

        #retrieve models based on the inputted filters
        if titler:
            if posted == None and writer == None:
                recobjs= model.query.filter(model.title.like(titler)).order_by(model.created.desc()).all()
            elif posted == None and writer != None:
                recobjs= model.query.filter(model.title.like(titler), model.written_by == writer).order_by(model.created.desc()).all()
            elif posted != None and writer == None:
                recobjs= model.query.filter(model.title.like(titler), model.created == posted).order_by(model.created.desc()).all()
            elif posted != None and writer != None:
                recobjs= model.query.filter(model.title.like(titler), model.created == posted, model.written_by == writer).order_by(model.created.desc()).all()
        else:
            if posted == None and writer == None:
                recobjs= model.query.order_by(model.created.desc()).all()
            elif posted == None and writer != None:
                recobjs= model.query.filter(model.written_by == writer).order_by(model.created.desc()).all()
            elif posted != None and writer == None:
                recobjs= model.query.filter(model.created == posted).order_by(model.created.desc()).all()
            elif posted != None and writer != None:
                recobjs= model.query.filter(model.created == posted, model.written_by == writer).order_by(model.created.desc()).all()
        
        #returning the records after quering the database
        if recobjs == []:
            return jsonify(status=0, message="No records found that match criteria")
        else:
            data= []
            #checking if the option for number of records was passed 
            if rec_no == None:
                ro= recobjs
            else:
                ro= recobjs[0:int(rec_no)]
            
            #looping through the list of record objects to create an array of json objects which each individually contain the details of a single record
            for i in ro:
                #retrieve comments of specific news item
                comms= []
                if i.comment_no > 0:
                    comobj= Comments.query.filter(Comments.parent_id == i.itemid).all()
                    for j in comobj:
                        tempdata2= {'written_by':j.written_by, 'text':j.text, 'posted':j.created.strftime('%B %d, %Y')}
                        #append each commetn to comm list
                        comms.append(tempdata2)

                #storing records into dictionaory
                tempdata1= {'written_by':i.written_by, 'title':i.title, 'created':i.created.strftime('%B %d, %Y'), 'url':i.url, 'text':i.text, 'comments':comms}
                #append converted data to a 'data' list
                data.append(tempdata1)
            
            return jsonify(data=data, status=1, message="Data retrieved successfully")




# TYou have to specify a news type in the 'newstype' field. The values can only be 'news' and 'jobs'
# You must also include a password for the post, as that will authorize you to update or delete the post. The field is 'password' and the value is the password to be used
# The posters name must be sent in the 'writer' field. Required
# Title must be added in the 'title' field. Required
# Either text or/and url must also be added in the 'text' and 'url' fields respectively
@app.route('/api/v1.0/postnews/', methods=['POST'])
def post_news():
    if request.is_json:
        requestdatadic= request.get_json()
        ntype= requestdatadic.get('newstype')
        unhashpass= requestdatadic.get('password')
        writer= requestdatadic.get('writer')
        title= requestdatadic.get('title')
        text= requestdatadic.get('text')
        url= requestdatadic.get('url')
    else:
        ntype= request.form.get('newstype')
        unhashpass= request.form.get('password')
        writer= request.form.get('writer')
        title= request.form.get('title')
        text= request.form.get('text')
        url= request.form.get('url')

    #conditions to check for valid data
    if ntype == None or unhashpass == None or writer == None or title == None:
        return jsonify(status=0, message="Error. Required fields missing. Please fill all required fields")
    
    if len(unhashpass) < 8:
        return jsonify(status=0, message="Error. Password must be at least 8 characters long")
    
    if text == None and url == None:
        return jsonify(status=0, message="Error. You must fill one or both of the 'text' and 'url' fields")
    elif text == "" and url == "":
        return jsonify(status=0, message="Error. You must fill one or both of the 'text' and 'url' fields")
    
    if ntype != 'jobs' and ntype != 'news':
        return jsonify(status=0, message="Error. You must fill valid data for the news type")
    
    #setting the models to use based on newstype
    if ntype == 'jobs':
        model= Hacker_jobs
        nt= "job"
    elif ntype == 'news':
        model= New_news
        nt= "story"
    
    #changing text or url to empty strings if they are none
    if text == None:
        text= ""
    if url == None:
        url = ""
    
    #hashing the password used to make the post
    hashpass= generate_password_hash(unhashpass)

    #adding the resulting post to database
    postobj= model(written_by=writer, title=title, text=text, url=url, password=hashpass, ntype=nt)
    db.session.add(postobj)
    db.session.commit()

    return jsonify(status=1, message="Success. Post has been added successfully.", post_id=postobj.nid)




# To update a post, you need to provide the passwork used in creating the post and the post id returned to you. These are required. The password in 'password' field and post id in 'post_id'
# The news type must also be specified. Field is 'newstype' and values are 'jobs' or 'news'
# To change title, use 'title' field, to change text, use 'text' field, to change 'url', use 'url' field. All these fields are optional.
@app.route('/api/v1.0/updatepost/', methods=['PUT'])
def update_post():
    requestdatadic= request.get_json()
    ntype= requestdatadic.get('newstype')
    pid= requestdatadic.get('post_id')
    unhashpass= requestdatadic.get('password')
    title= requestdatadic.get('title')
    text= requestdatadic.get('text')
    url= requestdatadic.get('url')

    #data validation
    if pid == None or unhashpass == None or ntype == None:
        return jsonify(status=0, message="All required fields must be filled")
    
    if ntype != 'jobs' and ntype != 'news':
        return jsonify(status=0, message="Error. Please input valid data")
    
    if ntype == 'jobs':
        model= Hacker_jobs
    elif ntype == 'news':
        model= New_news
    
    if pid.isnumeric():
        pass
    else:
        return jsonify(status=0, message="Error. Please input valid data")
    
    #after checks, retrive the record
    recobj= model.query.get(int(pid))
    if recobj == None:
        return jsonify(status=0, message="Error. This post has been deleted or does not exist")
    else:
        #check the password hash whether the password matches. If it does, update the record
        if check_password_hash(recobj.password, unhashpass):
            if title != None:
                recobj.title= title
            if text != None:
                recobj.text= text
            if url != None:
                recobj.url= url
            recobj.updated= date.today()

            db.session.commit()
            return jsonify(status=1, message="Post updated successfully.")
        else:
            return jsonify(status=0, message="Error. Authorization failed.")




#To delete, the post id 'post_id', news type 'newstype'  and password 'password' fields are requeire
@app.route('/api/v1.0/deletepost/', methods=['DELETE'])
def delete_post():
    requestdatadic= request.get_json()
    pid= requestdatadic.get('post_id')
    ntype= requestdatadic.get('newstype')
    unhashpass= requestdatadic.get('password')

    #validation checks
    if pid == None or unhashpass == None or ntype == None:
        return jsonify(status=0, message="Error. Fill in all the required fields")
    
    if pid.isnumeric():
        pass
    else:
        return jsonify(status=0, message="Error. Please input valid data")
    
    if ntype != 'jobs' and ntype != 'news':
        return jsonify(status=0, message="Error. Please input valid data")
    
    if ntype == 'jobs':
        model= Hacker_jobs
    elif ntype == 'news':
        model= New_news

    #retrive the record object
    recobj= model.query.get(int(pid))
    if recobj == None:
        return jsonify(status=0, message="Error. This post has been deleted or does not exist")
    else:
        if check_password_hash(recobj.password, unhashpass):
            db.session.delete(recobj)
            db.session.commit()
            return jsonify(status=1, message="Post successfully deleted.")
        else:
            return jsonify(status=0, message="Authentication Failed")
        
