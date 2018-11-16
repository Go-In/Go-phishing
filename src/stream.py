import certstream
import tldextract

def print_callback(message, context):
    all_domains = message['data']['leaf_cert']['all_domains']
    
    for domain in all_domains:
        extracted = tldextract.extract(domain)

        print(domain)
        print(extracted.domain)

certstream.listen_for_events(print_callback, 'wss://certstream.calidog.io')
