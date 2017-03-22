from . import base


class SimpleDictDataSource(base.DatasourceBase):

    def __init__(self, dict=None, **kargv):
        super(SimpleDictDataSource, self).__init__(dict=dict, **kargv)
        self.dict = dict

    def run(self, query_list, query_keys):
        cur = self.dict
        for key, val in query_list:
            if key in cur and val in cur[key]:
                cur = cur[key][val]
                continue
            return None

        if(not query_keys):
            return cur

        result = {}
        for k in query_keys:
            if(k in cur):
                result[k] = cur[k]
            else:
                result[k] = None

        return result





