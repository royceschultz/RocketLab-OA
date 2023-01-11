import sys
sys.path.append('..')

from modules import db

if __name__ == '__main__':
    db = db.connect_mongo()
    collection = db['measurements']
    collection.create_index([('measurement', 1), ('time', -1)], unique=True)
