import feedparser
from mylocalpackage.repository import FeedRepository, DomainRepository
import json
import datetime


def extract_info(parsed_feed):
    extracted_data = []
    for entry in parsed_feed['entries']:
        extracted_data.append({
            "url": entry['feedburner_origlink'],
            "time": datetime.datetime.strptime(entry['published'],'%a, %d %b %Y %H:%M:%S %z')
        })
    return extracted_data

def parse_feeds():
    repo = FeedRepository()
    domain_repo = DomainRepository()
    active_feeds = repo.get_active_feed_urls('time')
    for feed_url in active_feeds:
        if feed_url.get('etag', '') != '':
            parsed_feed = feedparser.parse(feed_url['topic_url'])
        else:
            parsed_feed = feedparser.parse(feed_url['topic_url'], etag=feed_url['etag'])
        # print(parsed_feed)
        # f = open('output.json', 'a')
        # f.write(json.dumps(parsed_feed))
        # f.close()
        if parsed_feed['status'] == 200:
            data = extract_info(parsed_feed)
            print(data)
            domain_repo.save_extracted_url_with_content('time', data)
            feed_url['etag'] = parsed_feed['etag']
    print(active_feeds)
    # update etags to the urls
    repo.save_feed_topics_by_domain('time', active_feeds)

if __name__ == "__main__":
    parse_feeds()