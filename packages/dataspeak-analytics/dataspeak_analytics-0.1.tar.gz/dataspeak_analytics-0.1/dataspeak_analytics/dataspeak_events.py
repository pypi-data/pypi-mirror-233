from .analytics_library import AnalyticsLibrary
from datetime import datetime

class DataspeakEvents(AnalyticsLibrary):

    def chat_session_created(self, user_id, chatbot_id):
        properties = {
            'Chatbot_ID': chatbot_id,
            'Session_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Chat_Session_Created', user_id, properties)

    def user_chat_interaction(self, user_id, chatbot_id, message_content):
        properties = {
            'Chatbot_ID': chatbot_id,
            'Message_Content': message_content,
            'Interaction_Timestamp': datetime.now().isoformat()
        }
        self.track_event('User_Chat_Interaction', user_id, properties)

    def data_added_to_chatbot(self, user_id, chatbot_id, data_type):
        properties = {
            'Chatbot_ID': chatbot_id,
            'Data_Type': data_type,
            'Addition_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Data_Added_to_Chatbot', user_id, properties)

    def data_source_utilized(self, user_id, chatbot_id, data_source_id):
        properties = {
            'Chatbot_ID': chatbot_id,
            'Data_Source_ID': data_source_id,
            'Utilization_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Data_Source_Utilized', user_id, properties)

    def api_accessed(self, user_id, auth_key, api_endpoint, request_type, response_status):
        properties = {
            'Auth_Key': auth_key,
            'API_Endpoint': api_endpoint,
            'Request_Type': request_type,
            'Response_Status': response_status,
            'API_Access_Timestamp': datetime.now().isoformat()
        }
        self.track_event('API_Accessed', user_id, properties)

    def chatbot_updated(self, user_id, chatbot_id, update_type):
        properties = {
            'Chatbot_ID': chatbot_id,
            'Update_Type': update_type,
            'Update_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Chatbot_Updated', user_id, properties)

    def chatbot_embedded(self, user_id, chatbot_id, website_url):
        properties = {
            'Chatbot_ID': chatbot_id,
            'Website_URL': website_url,
            'Embed_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Chatbot_Embedded', user_id, properties)

    def chatbot_created(self, user_id, chatbot_id, chatbot_name, data_type):
        properties = {
            'Chatbot_ID': chatbot_id,
            'Chatbot_Name': chatbot_name,
            'Data_Type': data_type,
            'Creation_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Chatbot_Created', user_id, properties)

    # Funnels
    def onboarding_funnel(self, user_id, step):
        steps = ["User_Registration", "Chat_Session_Created", "First_Chat_Interaction", "Data_Addition_to_Chatbot"]
        if step in steps:
            self.track_event(step, user_id)

    def user_registration(self, user_id, user_type):
        properties = {
            'User_Type': user_type,
            'Registration_Timestamp': datetime.now().isoformat()
        }
        self.track_event('User_Registration', user_id, properties)

    def user_login(self, user_id, user_type):
        properties = {
            'User_Type': user_type,
            'Login_Timestamp': datetime.now().isoformat()
        }
        self.track_event('User_Login', user_id, properties)

    def new_chatbot_creation(self, user_id, chatbot_name):
        properties = {
            'Chatbot_Name': chatbot_name,
            'Creation_Timestamp': datetime.now().isoformat()
        }
        self.track_event('New_Chatbot_Creation', user_id, properties)

    def chatbot_deletion(self, user_id, chatbot_name):
        properties = {
            'Chatbot_Name': chatbot_name,
            'Deletion_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Chatbot_Deletion', user_id, properties)

    def api_key_generated(self, user_id, key_type):
        properties = {
            'Key_Type': key_type,
            'Generation_Timestamp': datetime.now().isoformat()
        }
        self.track_event('API_Key_Generated', user_id, properties)

    def document_view(self, user_id, doc_section):
        properties = {
            'Doc_Section': doc_section,
            'View_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Document_View', user_id, properties)

    def search_query(self, user_id, search_term, results_found):
        properties = {
            'Search_Term': search_term,
            'Results_Found': results_found,
            'Search_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Search_Query', user_id, properties)

    def feedback_submitted(self, user_id, feedback_type, chat_session_id):
        properties = {
            'Feedback_Type': feedback_type,
            'Chat_Session_Id': chat_session_id,
            'Feedback_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Feedback_Submitted', user_id, properties)

    def error_occurred(self, user_id, error_type, error_message):
        properties = {
            'Error_Type': error_type,
            'Error_Message': error_message,
            'Error_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Error_Occurred', user_id, properties)

    def session_ended(self, user_id, session_duration, reason):
        properties = {
            'Session_Duration': session_duration,
            'End_Reason': reason,
            'End_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Session_Ended', user_id, properties)

    def user_logout(self, user_id, user_type):
        properties = {
            'User_Type': user_type,
            'Logout_Timestamp': datetime.now().isoformat()
        }
        self.track_event('User_Logout', user_id, properties)

    def feature_request(self, user_id, feature_description):
        properties = {
            'Feature_Description': feature_description,
            'Request_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Feature_Request', user_id, properties)

    def profile_updated(self, user_id, fields_updated):
        properties = {
            'Fields_Updated': fields_updated,
            'Update_Timestamp': datetime.now().isoformat()
        }
        self.track_event('Profile_Updated', user_id, properties)