import ConfigParser
cf = ConfigParser.ConfigParser()
class MatInfo(object):
    def __init__(self, attributes_path='../config/attributes.conf', retrieval_path = '../config/retrieval.conf'):
        self.attributes_path = attributes_path
        self.retrieval_path = retrieval_path
        self.att_conf = self._loadAttributesConf()
        self.retrieval_conf = self._loadRetrievalConf(self.att_conf)

    def _loadAttributesConf(self):
        cf.read(self.attributes_path)
        conf = {}
        for item in cf.items('attributes'):
            if item[1] not in conf:
                conf[item[1]] = []
            conf[item[1]].append(item[0])
        return conf

    def _loadRetrievalConf(self, att_conf):
        key = 'retrieval'
        cf.read(self.retrieval_path)
        sections = cf.sections()
        retrieval_conf = {}
        if key not in att_conf:
            raise KeyError('there is no retrieval attributes in config file')
        for att in att_conf[key]:
            if att not in sections:
                continue
            retrieval_conf[att] = []
            for val in cf.items(att):
                retrieval_conf[att].append(val[1])
        return retrieval_conf