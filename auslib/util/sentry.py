from raven.processors import Processor

class SanitizeHeadersProcessor(Processor):
    def __init__(self, sanitizeHeaders=['Authorization']):
        self.sanitizeHeaders = sanitizeHeaders

    def filter_http(self, data):
        if 'headers' in data:
            for header in self.sanitizeHeaders:
                if header in data['headers']:
                    data['headers'][header] = 'REDACTED'
