from google.cloud import firestore
import json

class FeedRepository():
    def save_feed_topics_by_domain(self, domain_name, new_data):
        db = firestore.Client()
        topic_doc_ref = db.collection(u'feeds').document(domain_name)
        data = {
            'name': domain_name,
            'topics': new_data
        }
        topic_doc_ref.set(data, merge=True)

    def get_active_feed_urls(self, domain_name, is_active=False):
        db = firestore.Client()
        topic_doc_ref = db.collection(u'feeds').document(domain_name)
        topics = topic_doc_ref.get().to_dict()
        return [topic for topic in topics['topics'] if topic['is_active'] == is_active]


class DomainRepository():
    def get_new_urls(self, domain_name):
        db = firestore.Client()
        new_urls_doc = db.collection(u'domains').document(domain_name)
        new_urls_doc_results = new_urls_doc.get()
        return new_urls_doc_results.to_dict()

    def save_extracted_url_with_content(self, domain_name, new_data):
        db = firestore.Client()
        new_urls_doc = db.collection(u'domains').document(domain_name)
        data = {
            'name': domain_name,
            'new': new_data
        }
        new_urls_doc.set(data, merge=True)