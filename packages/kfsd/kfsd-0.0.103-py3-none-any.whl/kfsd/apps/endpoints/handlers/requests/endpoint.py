from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.handlers.general.data import gen_data_handler
from kfsd.apps.endpoints.serializers.requests.endpoint import EndpointModelSerializer
from kfsd.apps.models.tables.requests.endpoint import Endpoint
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.template import Template
from kfsd.apps.core.utils.http.base import HTTP
import json


def gen_endpoint_handler(instance):
    handler = EndpointHandler(instance.identifier, False)
    qsData = EndpointModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


class EndpointHandler(BaseHandler, HTTP):
    def __init__(self, endpointIdentifier, isDBFetch):
        HTTP.__init__(self)
        BaseHandler.__init__(
            self,
            serializer=EndpointModelSerializer,
            modelClass=Endpoint,
            identifier=endpointIdentifier,
            isDBFetch=isDBFetch,
        )

    def getUrl(self):
        return DictUtils.get(self.getModelQSData(), "url")

    def getMethod(self):
        return DictUtils.get(self.getModelQSData(), "method")

    def getHeaders(self):
        return DictUtils.get(self.getModelQSData(), "headers")

    def getSuccessCode(self):
        return DictUtils.get(self.getModelQSData(), "success_code")

    def getFormattedHeaders(self):
        return {header["key"]: header["value"] for header in self.getHeaders()}

    def getReqMethod(self, method):
        methodMap = {"GET": self.get, "POST": self.post, "DELETE": self.delete}
        return methodMap[method]

    def getDataHandler(self):
        return gen_data_handler(self.getModelQS().body)

    def getReqBody(self, context):
        dataHandler = self.getDataHandler()
        body = dataHandler.getBody()
        if dataHandler.isJson():
            body = dataHandler.getJsonBody()
        if dataHandler.isTemplate():
            contextFormat = {"context": context}
            template = Template(body, contextFormat, {}, True)
            return template.mergeValues()
        return body

    def isJsonType(self, text):
        try:
            json.dumps(text)
            return True
        except Exception:
            return False

    def exec(self, context):
        url = self.getUrl()
        reqMethodType = self.getMethod()
        reqMethod = self.getReqMethod(reqMethodType)
        headers = self.getFormattedHeaders()
        successCode = self.getSuccessCode()
        kwargs = {"headers": headers}
        if reqMethodType == "POST":
            reqBody = self.getReqBody(context)
            if self.isJsonType(reqBody):
                kwargs["json"] = reqBody
            else:
                kwargs["body"] = reqBody
            resp = reqMethod(url, successCode, **kwargs)
            print("Resp: {}".format(resp))
            return resp
        else:
            return reqMethod(url, successCode, **kwargs)
