import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgres://jkvvtzdintehrx:bdfa464550e678373b42fabbb15551d9d2303a5f77bb622da6ceb007e7e05562@ec2-174-129-27-158.compute-1.amazonaws.com:5432/d21urldpnfbqa8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['b05401009@ntu.edu.tw']
    POSTS_PER_PAGE = 3