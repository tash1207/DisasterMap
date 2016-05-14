import pymongo
from datetime import datetime, date, time, timedelta

class Map(object):
	"Map helper class to determine what map the entry should be assigned."

	def __init__(self, db):
		self.db = database
		self.disasters = database.disasters

	# Get existing maps for at most 10 days ago.  
	# If no maps returned, create a new map. 
	# Of the maps returned, check if lat/long within 100 mi range of center lat/long
	# put point with map id into db. 

	def get_map_id(self, current_date, loc):
		drange = current_date - timedelta(days=10)
		# Get nearest disaster map from the last ten days within 10,000 meters.
		map = disasters.find(
			{start_datetime: {"$gte": drange},
			 location: {$near:{$geometry: {type:"Point", coordinates: loc}, $maxDistance: 10000}}}).limit(1).pretty():
		if map:
			return map.id
		else:
			return create_map(current_date, loc)

	def create_map(self, current_date, loc):
		return