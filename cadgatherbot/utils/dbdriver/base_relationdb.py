class BaseRelationDBDriver(object):

    def __init__(self, **kargv):
        pass

    def query(self, *argv):
        return QueryHandler(self.run, argv)

    def run(self, query_list, query_keys):
        raise NotImplementedError('DatasourceBase must be implemented.')


class QueryHandler(object):

    def __init__(self, run_fn, query_keys):
        self.chain_query = []
        self.run_fn = run_fn
        self.query_keys = query_keys

    def key(self, key, value):
        self.chain_query.append((key, value))
        return self

    def run(self):
        return self.run_fn(self.chain_query, self.query_keys)
