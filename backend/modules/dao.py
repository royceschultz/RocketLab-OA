from .db import connect_mongo
from datetime import datetime
import pymongo # For DuplicateKeyError
from bson.objectid import ObjectId

# Consider using a real ORM like MongoEngine or Mongoose.
# But this is a simple example.

def parse_time_string(time_str):
    try:
        return datetime.fromisoformat(time_str)
    except:
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        return datetime.strptime(time_str, time_format)

class Measurement:
    def __init__(self):
        self.db = connect_mongo()

    def create(self, data):
        # Checking required fields wouldn't be necessary if using SQL
        # But this is for MongoDB.
        # NOTE: Allows all extra non-required fields.
        required_fields = ['measurement', 'time', 'value', 'apid']
        for field in required_fields:
            if field not in data:
                raise Exception(f'Missing required field: {field}')
        # Validate fields
        data['time'] = parse_time_string(data['time'])
        try:
            data['value'] = float(data['value'])
        except:
            pass  # Allow non-numeric value types
        try:
            data['apid'] = int(data['apid'])
        except:
            pass  # Allow non-numeric apid types
        # Write data
        try:
            self.db.measurements.insert_one(data)
            data['_id'] = str(data['_id'])
        except pymongo.errors.DuplicateKeyError as e:
            # Index enforces unique (measurement, time)
            duplicate_keys = e.details['keyValue']
            existing_obj = self.db.measurements.find_one(duplicate_keys)
            error_msg = '\n'.join([
                f'Duplicate keys: {duplicate_keys}',
                'Existing ObjectId: ' + str(existing_obj['_id']),
                'Existing value: ' + str(existing_obj['value']),
                'Attempted insert: ' + str(data['value']),
            ])
            raise Exception(error_msg)

    def read(self, _id):
        obj = self.db.measurements.find_one({'_id': ObjectId(_id)})
        if obj is None:
            raise Exception(f'No Measurement with _id {_id}')
        obj['_id'] = str(obj['_id'])
        return {
            'success': True,
            'result': obj,
        }

    def lookup(self, measurement=None, start_time=None, end_time=None, page=1, page_size=10):
        # Build query
        query = {}
        if measurement is not None:
            query['measurement'] = {
                '$regex': measurement,
            }
        if start_time is not None:
            start_time = parse_time_string(start_time)
            query['time'] = {'$gte': start_time}
        if end_time is not None:
            end_time = parse_time_string(end_time)
            if 'time' not in query:
                query['time'] = {}
            query['time']['$lte'] = end_time
        # Execute query
        offset = (page-1) * page_size
        results = self.db.measurements.find(query).skip(offset)
        if page_size > 0:
            results = results.limit(page_size)
        results = list(results)
        for result in results:  # Fix ObjectID is not JSON serializable
            result['_id'] = str(result['_id'])
        return results

    def delete(self, _id):
        res = self.db.measurements.delete_one({'_id': ObjectId(_id)})
        if res.deleted_count == 0:
            raise Exception(f'No Measurement with _id {_id}')
        return {
            'success': True,
        }
