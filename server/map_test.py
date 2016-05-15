import unittest
from map import Map
from pymongo import MongoClient, GEO2D
from datetime import datetime, date, time, timedelta

class TestMap(unittest.TestCase):
	def test_existing_map(self):
		db = MongoClient().geo_example
		db.disasters.create_index([("loc", GEO2D)])
		result = db.disasters.insert_many([{"loc": [12, 15], "name": "blah1.44", "start_datetime": datetime.now()}, {"loc": [30, 5], "name": "blah2.222", "start_datetime": datetime.now()}, {"loc": [1, 2], "name": "blah3111", "start_datetime": datetime.now()}, {"loc": [40, 40], "name": "blah4333", "start_datetime": datetime.now()}]) 
		print result.inserted_ids
		m = Map(db)
		m.get_map_id(datetime.now(), [0, 0])

	def test_new_map(self):
		db = MongoClient().geo_example
		m = Map(db)
		m.create_map(datetime.now(), [10, 10])

if __name__ == '__main__':
    unittest.main()