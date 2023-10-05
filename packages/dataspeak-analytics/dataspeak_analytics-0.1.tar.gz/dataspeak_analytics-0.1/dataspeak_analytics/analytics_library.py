import mixpanel
from pymongo import MongoClient

class AnalyticsLibrary:
    def __init__(self, mixpanel_token, mongo_uri, db_name, collection_name):
        self.mp = mixpanel.Mixpanel(mixpanel_token)
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def _send_to_mixpanel(self, event_name, user_id, properties={}):
        self.mp.people_set(user_id, properties)  # Use this method to set People properties
        self.mp.track(user_id, event_name, properties)

    def _store_in_mongo(self, event_name, user_id, properties={}):
        document = {
            'event_name': event_name,
            'user_id': user_id,
            'properties': properties
        }
        self.collection.insert_one(document)

    def track_event(self, event_name, user_id, properties={}):
        self._send_to_mixpanel(event_name, user_id, properties)
        self._store_in_mongo(event_name, user_id, properties)

    def get_user_events(self, user_id):
        return list(self.collection.find({'user_id': user_id}))

    def get_events_by_type(self, event_type):
        return list(self.collection.find({'event_name': event_type}))

    def get_events_in_time_range(self, start_time, end_time):
        return list(self.collection.find({'properties.timestamp': {'$gte': start_time, '$lte': end_time}}))

    def get_user_property(self, user_id, property_name):
        user_data = self.collection.find_one({'user_id': user_id, 'properties.' + property_name: {'$exists': True}})
        return user_data['properties'][property_name] if user_data else None

    def get_total_event_count(self, event_name):
        """Returns the total number of times an event occurred."""
        return self.collection.count_documents({'event_name': event_name})

    def get_event_counts_per_user(self, event_name):
        """Returns the number of times an event occurred per user."""
        pipeline = [
            {"$match": {"event_name": event_name}},
            {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_active_users(self, start_time, end_time):
        """Returns users who had events between a given time range."""
        return self.collection.distinct('user_id', {'properties.timestamp': {'$gte': start_time, '$lte': end_time}})

    def get_top_events_for_user(self, user_id, limit=5):
        """Returns the top events a user triggered the most."""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": "$event_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        return list(self.collection.aggregate(pipeline))
    def set_user_property(self, user_id, property_name, value):
        self.collection.update_one({'user_id': user_id}, {'$set': {'properties.' + property_name: value}})

    def create_funnel(self, funnel_name, event_steps):
        # This is a simple definition. In a real-world scenario, you'd want more attributes and validations.
        self.db['funnels'].insert_one({'funnel_name': funnel_name, 'event_steps': event_steps})

    def define_funnel(self, funnel_name, steps):
        """
        Defines a new funnel or updates an existing funnel with a given name and sequence of steps.

        Parameters:
            - funnel_name: Name of the funnel.
            - steps: A list containing the ordered steps of the funnel.
        """
        self.db['funnels'].update_one(
            {'funnel_name': funnel_name},
            {'$set': {'event_steps': steps}},
            upsert=True
        )

    def track_funnel_progress(self, funnel_name, user_id, step):
        """
        Tracks the user's progression through a specified funnel.

        Parameters:
            - funnel_name: Name of the funnel.
            - user_id: The unique identifier for the user.
            - step: The step in the funnel.
        """
        # Validate if the provided step is in the defined funnel
        funnel = self.db['funnels'].find_one({'funnel_name': funnel_name})
        if not funnel or step not in funnel['event_steps']:
            raise ValueError("Invalid funnel or step provided.")

        self.track_event(step, user_id)

    def get_funnel_conversion(self, funnel_name):
        """
        Returns the conversion rates for each step of the specified funnel.

        Parameters:
            - funnel_name: Name of the funnel.
        """
        funnel = self.db['funnels'].find_one({'funnel_name': funnel_name})
        if not funnel:
            return None

        conversion_rates = []
        total_users = self.collection.count_documents({'event_name': funnel['event_steps'][0]})

        for idx, event in enumerate(funnel['event_steps'][1:]):
            total_users_next_step = self.collection.count_documents({'event_name': event})
            conversion_rate = (total_users_next_step / total_users) * 100
            conversion_rates.append({
                'step': event,
                'conversion_rate': conversion_rate
            })
            total_users = total_users_next_step

        return conversion_rates

    def get_drop_off(self, funnel_name):
        conversions = self.get_funnel_conversion(funnel_name)
        drop_offs = []

        for i, conversion in enumerate(conversions[:-1]):
            next_conversion = conversions[i + 1]
            drop_off_rate = 100 - (next_conversion['conversion_rate'] - conversion['conversion_rate'])
            drop_offs.append({
                'step': conversion['step'],
                'drop_off_rate': drop_off_rate
            })

        return drop_offs
