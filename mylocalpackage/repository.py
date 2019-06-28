from google.cloud import firestore
import json

class FeedRepository():
    def save_feed_topics_by_domain(self, domain_name, new_data):
        db = firestore.Client()
        topic_doc_ref = db.collection(u'feeds').document(domain_name)
        topic_doc_ref.set(new_data, merge=True)

    def get_active_feed_urls(self, domain_name, is_active=False):
        db = firestore.Client()
        topic_doc_ref = db.collection(u'feeds').document(domain_name)
        topics = topic_doc_ref.get().to_dict()
        return [topic for topic in topics['topics'] if topic['is_active'] == is_active]
