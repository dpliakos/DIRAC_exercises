"""Task 4 module."""

from elasticsearch import Elasticsearch


class ElasticSearchClient(object):
    """Elastic search client."""

    def __init__(self, protocol="http", host="localhost",
                 port="9200", auth=None):
        """Figure out the elastic search url."""
        self.url = "{}://{}:{}".format(protocol, host, port)
        self.es = None

    def __connect(self):
        """Conect to the elasticsearch."""
        es = Elasticsearch(self.url)
        self.es = es

    def getES(self):
        """Get the es connection."""
        if (self.es is None):
            self.__connect()

        return self.es

    def create_index(self, index):
        """Create an index."""
        es = self.getES()
        res = es.indices.create(index=index)
        return res

    def add_data(self, index, doc_type, id, body):
        """Update an index with data."""
        es = self.getES()
        # res = es.indices.create(index=index, body=body, ignore=400)
        res = es.index(index=index, doc_type=doc_type, id=id, body=body)
        return res

    def read_data(self, index, doc_type, id):
        """Get the data for a given set of document identifiers."""
        es = self.getES()
        res = es.get(index, doc_type=doc_type, id=id)
        return res

    def get_all_indices(self):
        """List all indices."""
        es = self.getES()
        return es.indices.get(["_all"])

    def delete_all_indices(self):
        """Delete all indices."""
        es = self.getES()
        res = es.indices.delete(["_all"])
        return res

    def delete_index(self, index):
        """Delete an index."""
        es = self.getES()
        res = es.indices.delete([index])
        return res
