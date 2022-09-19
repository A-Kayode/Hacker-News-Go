class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@localhost/hacker_news_go"

    SCHEDULER_API_ENABLED=True