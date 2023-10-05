from datetime import datetime
from ..storages.storage import Storage
from ..notifier import Notifier
import os

class GAsset():

    storage = Storage()
    notifier = Notifier()

    def __init__(self, name, messageType, title=None, description=None, var=None, show=True) -> None:
        self.name = name
        self.messageType = messageType
        self.title = title
        self.description = description
        self.var = var
        self.created = datetime.now()
        self.modified = self.created
        self.show = show

    def to_json(self):

        result = {
            "name": self.name,
            "messageType": self.messageType,
            "title": self.title,
            "description": self.description,
            "var": self.var,
            "created": str(self.created),
            "modified": str(datetime.now()),
            "show": self.show
        }

        if "BDA_ID" in os.environ:
            result['bdaId'] = os.environ.get('BDA_ID')

        if "SERVICE_ID" in os.environ:
            result['serviceId'] = os.environ.get('SERVICE_ID')

        if "ORGANIZATION_ID" in os.environ:
            result['organizationId'] = os.environ.get('ORGANIZATION_ID')
        
        if "OWNER_ID" in os.environ:
            result['userId'] = os.environ.get('OWNER_ID')

        if "OWNER_ID" in os.environ:
            result['userId'] = os.environ.get('OWNER_ID')

        if "ARGO_NODE_ID" in os.environ:
            result['executionId'] = os.environ.get('ARGO_NODE_ID')

        if "ACCESS_LEVEL" in os.environ:
            result['accessLevel'] = os.environ.get('ACCESS_LEVEL')
        
        return result
    
    def get_path(self):
        return None
    
    def send(self):
        self.path = self.storage.save(path=self.get_path(), metadata=self.to_json())
        self.notifier.something_has_changed(self.to_json())
