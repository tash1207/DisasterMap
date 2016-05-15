import pymongo
from datetime import datetime, date, time, timedelta
from bson.son import SON
import sys

class Map():
	"Map helper class to determine what map the entry should be assigned."

	def __init__(self, db):
		self.db = db

	# Get existing maps for at most 10 days ago.  
	# If no maps returned, create a new map. 
	# Of the maps returned, check if lat/long within 100 mi range of center lat/long
	# put point with map id into db. 

	def get_map_id(self, current_date, location):
		disasters = self.db.disasters
		drange = current_date - timedelta(days=10)
		# Get nearest disaster map from the last ten days within 10,000 meters.
		# result_map = disasters.find_one({"start_datetime": {"$gte": drange}, "loc": SON([("$near", location), ("$maxDistance", 10)])})
		result_map = disasters.find_one({'loc':{'$near':{'$geometry':{'type': "Point", 'coordinates': location},'$maxDistance': 10}}})
		if result_map:
			print "START"
			print result_map["_id"]
			print result_map
			print "END"
			return result_map["_id"]
			
		else:
			print "OH NOSE"
			return self.create_map(current_date, location)

	def create_map(self, current_date, location):
		disasters = self.db.disasters
		# Insert the new disaster map and other data in the disaster db
		disasters.create_index([("loc", pymongo.GEOSPHERE), ("name", pymongo.ASCENDING), ("start_datetime", pymongo.DESCENDING)])
		try:
			response = disasters.insert_one({'loc': { 'type': "Point", 'coordinates': location }, "name": "red", "start_datetime": datetime.now()})
			#response = disasters.insert_one({'loc': {'type': 'Point', 'coordinates': location}, "name": "blue", "start_datetime": datetime.now()})
			print response.inserted_id
			print response
			return response.inserted_id
		except:
			print "Unexpected error:", sys.exc_info()	
		return	
