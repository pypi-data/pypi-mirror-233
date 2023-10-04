from __future__ import absolute_import

from .api import Api


class Client(object):

    def __init__(self, base_url, username=None, password=None, api_version='v1'):
        self.api = Api(base_url, username, password, api_version)

    def get_cluster_metrics(self):
        res = self.api.send(method='get', resource='/cluster/metrics')
        return res

    def get_cluster_nodes(self, states=None):
        res = self.api.send(method='get', resource='/cluster/nodes', params={'states': states})
        return res

    def get_cluster_appstatistics(self, states, applicationTypes):
        res = self.api.send(method='get', resource='/cluster/appstatistics',
                            params={'states': states, 'applicationTypes': applicationTypes})
        return res

    def get_cluster_apps(self, appid):
        res = self.api.send(method='get', resource='/cluster/apps', resource_id=appid)
        return res
