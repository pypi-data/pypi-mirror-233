from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from secret_provider import SecretProvider
from typing import Optional


class CbCmd:
    id: str
    payload: dict

    def __init__(self, id, payload):
        self.id = id
        self.payload = payload


class CbQry:
    query: str
    params: list

    def __init__(self, query, params: Optional[list] = []):
        self.query = query
        self.params = params


class CouchbaseClusterFactory:
    def __init__(self):
        self._secret_provider = SecretProvider()

    def create_cluster(self):
        username = self._secret_provider.get_secret("COUCHBASE_USERNAME")
        password = self._secret_provider.get_secret("COUCHBASE_PASSWORD")
        return Cluster(
            "couchbase://localhost",
            ClusterOptions(PasswordAuthenticator(username, password)),
        )


class CouchbaseClusterManager:
    def __init__(self):
        self._cluster_factory = CouchbaseClusterFactory()
        self._cluster = self._cluster_factory.create_cluster()

    def get_cluster(self):
        return self._cluster

    def close(self):
        self._cluster.close()


class CouchbaseCollectionManager:
    def __init__(self, bucket_name: str, scope_name: str, collection_name: str):
        self._scope_name = scope_name
        self._collection_name = collection_name
        self._cluster_manager = CouchbaseClusterManager()
        self._bucket = self._cluster_manager.get_cluster().bucket(bucket_name)

    def get_scope(self):
        return self._bucket.scope(self._scope_name)

    def get_collection(self):
        return self.get_scope().collection(self._collection_name)

    async def upsert(self, document_id, json_payload):
        collection = self.get_collection()
        collection.upsert(document_id, json_payload)


class CouchbaseCmdManager:
    def __init__(self, bucket_name: str, scope_name: str, collection_name: str):
        self._collection = CouchbaseCollectionManager(
            bucket_name, scope_name, collection_name
        )

    async def command(self, cmd: CbCmd):
        return await self._collection.upsert(cmd.id, cmd.payload)


class CouchbaseQryManager:
    def __init__(self):
        self._cluster_manager = CouchbaseClusterManager()
        pass

    def query(self, qry: CbQry):
        return self._cluster_manager.get_cluster().query(qry.query, params=qry.params)
