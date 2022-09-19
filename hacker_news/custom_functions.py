import requests
from datetime import datetime
from . import app, db, scheduler
from .models import *


#function for retriving individual news items given a list of the item ids
def get_news_item(model, ann_list):
    #loop through list of news ids to get the details of each news id and add to database
    news_data= []
    comment_records= []
    for i in ann_list:
        snn_response= requests.get(f'https://hacker-news.firebaseio.com/v0/item/{i}.json')
        snn_item= snn_response.json()
        if snn_item.get('text') == None:
            text= ""
        else:
            text= snn_item.get('text')
        if snn_item.get('url') == None:
            url= ""
        else:
            url= snn_item.get('url')
        if snn_item.get('title') == None:
            title= ""
        else:
            title= snn_item.get('title')
        #convert the unix time to datetime object
        time = datetime.fromtimestamp(snn_item.get('time'))
        #check if type is not job and then retrieve number of comments
        if snn_item.get('type') != 'job' and snn_item.get('kids') != None:
            com_no= len(snn_item.get('kids'))
        else:
            com_no= 0
        #create a record object for the news item
        rec_obj= model(itemid=snn_item.get('id'), ntype=snn_item.get('type'), comment_no=com_no, created=time, title=title, text=text, url=url, written_by=snn_item.get('by'))
        #append it to the news_data list
        news_data.append(rec_obj)

        #if news item possessed comments, comments will be retrieved and added to comment database
        if snn_item.get('kids') != None:
            com_list= snn_item.get('kids')
            #retrieve each comment and create a record object for each of them to append to a list
            for j in com_list:
                level_counter = 0
                comment_response= requests.get(f'https://hacker-news.firebaseio.com/v0/item/{j}.json')
                comment_item = comment_response.json()
                com_time= datetime.fromtimestamp(comment_item.get('time'))
                com_obj= Comments(item_id=comment_item.get('id'), parent_id=comment_item.get('parent'), created=com_time, written_by=comment_item.get('by'), text=comment_item.get('text'), level=level_counter)
                #append to comment list
                comment_records.append(com_obj)
    
    return news_data, comment_records



#this function queries the hacker_news news endpoints and adds them to the database
def retrieve_news(endpoint, model):
    #retrieve and store new news stories in database
    #ann --> all new news; snn --> specific new_news
    ann_response= requests.get(endpoint)
    ann_list2= ann_response.json()
    #get only first 100 news ids from the list
    ann_list = ann_list2[0:100]

    # create record objects for each news item in the list of item ids
    news_data, comment_records= get_news_item(model, ann_list)
                            

    #add all to database session and commit
    db.session.add_all(news_data)
    db.session.commit()
    db.session.add_all(comment_records)
    db.session.commit()


#functions to be called to load news and comment information into the database when the app is initially deployed to the server and run . Commented out for testing purposes
# retrieve_news('https://hacker-news.firebaseio.com/v0/newstories.json', New_news)
# retrieve_news('https://hacker-news.firebaseio.com/v0/jobstories.json', Hacker_jobs)



#this creates the job schedule in order to update the database with new records on a preset interval
@scheduler.task('interval', id='refresh_news_list', minutes=5)
def refresh_news_list():
    #creating updates schedule for new stories
    ann_response= requests.get('https://hacker-news.firebaseio.com/v0/newstories.json')
    ann_list2= ann_response.json()
    #get only first 100 news ids from the list
    ann_list3 = ann_list2[0:100]
    ann_list= []

    #retrieve all current records from the new stories database
    nn_recs2= db.session.query(New_news.itemid).all()
    #convert results from list of tuples to a simple list
    nn_recs= []
    for i in nn_recs2:
        nn_recs.append(i[0])
    
    #loop through list of item ids gotten from endpoint and compared each id with list of item ids gotten from database. If there is no match append id to a new list that will be used to retrieve items to update the database
    for i in ann_list3:
        if i not in nn_recs:
            ann_list.append(i)
    
    #get items from new filtered list and use them to create record objects for each retrieved news item
    news_data1, comment_records1= get_news_item(New_news, ann_list)
                            
    #add all to database session and commit
    db.session.add_all(news_data1)
    db.session.commit()
    db.session.add_all(comment_records1)
    db.session.commit()



    #creating updates schedule for jobs
    jb_response= requests.get('https://hacker-news.firebaseio.com/v0/jobstories.json')
    jb_list2= jb_response.json()
    #get only first 100 news ids from the list
    jb_list3 = jb_list2[0:100]
    jb_list= []

    #retrieve all current records from the new stories database
    jb_recs2= db.session.query(Hacker_jobs.itemid).all()
    #convert results from list of tuples to a simple list
    jb_recs= []
    for i in jb_recs2:
        jb_recs.append(i[0])
    
    #loop through list of item ids gotten from endpoint and compared each id with list of item ids gotten from database. If there is no match append id to a new list that will be used to retrieve items to update the database
    for i in jb_list3:
        if i not in nn_recs:
            jb_list.append(i)
    
    #get items from new filtered list and use them to create record objects for each retrieved news item
    news_data2, comment_records2= get_news_item(Hacker_jobs, jb_list)
                            
    #add all to database session and commit
    db.session.add_all(news_data2)
    db.session.commit()
    db.session.add_all(comment_records2)
    db.session.commit()

    
