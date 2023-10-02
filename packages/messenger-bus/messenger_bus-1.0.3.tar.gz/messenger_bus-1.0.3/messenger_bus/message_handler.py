import json
import logging
import pathlib
import re
from collections import namedtuple
from typing import NamedTuple

from phoenix.messenger.envelope import Envelope
from phoenix.messenger.stamp import AmqpStamp, ResultStamp

FORMAT = '%(asctime)s %(levelname)s:%(name)s:%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('messenger')
logger.setLevel(logging.DEBUG)

_handlers = []


class CommandInterface(namedtuple('CommandInterface','payload')):
    pass



def handler(transport:str=None, bus:str=None, binding_key:str=None, priority:int=0, command:CommandInterface=None):
    def wrapper(fn):
        def func(*args,**kwargs):
            return fn(*args, **kwargs)

        item = {
            "transport":transport,
            "bus":bus,
            "binding_key":binding_key,
            "priority": priority,
            "command": command,
            "callback":func,
            "controller":fn
        }

        if type(fn) == type: # annotation mise sur une class
            item["type"] = "class"
        elif type(fn).__name__ == "function": # annotation mise sur une function
            item["type"] = "function"

        _handlers.append(item)
        return func
    return wrapper



def process_handlers(envelope:Envelope):
    from phoenix.messenger.transport import AMQPTransport

    stamp = envelope.last("TransportStamp")
    transport = stamp.transport
    transport_attributes:dict = stamp.attributes

    stamp = envelope.last("BusStamp")
    bus = stamp.bus
    message = envelope.message

    print(transport_attributes)

    _handlers_selected = []
    for p in _handlers:

        is_ok = True
        criterias = {}
        # un check transport est actif
        if p.get("transport"):
            criterias["transport"] = False
            if p.get("transport") == transport.definition.name:
                criterias["transport"] = True

        # un check bus est actif
        if p.get("bus"):
            criterias["bus"] = False
            if p.get("bus") == bus.definition.name:
                criterias["bus"] = True

        # un check binding_key est actif
        if p.get("binding_key"):
            criterias["binding_key"] = False

            if not isinstance(message,CommandInterface):
                binding_key = message.get("action")
                if re.search(r"^{}$".format(p.get("binding_key")), binding_key):
                    criterias["binding_key"] = True


        # un check command est actif
        if p.get("command"):
            criterias["command"] = False
            if isinstance(message, CommandInterface):
                if isinstance(message,p.get("command")):
                    criterias["command"] = True
                    print(dir(p["controller"]),p["controller"].__annotations__)

        if p["type"] == "class":
            instance_ = p["controller"]()
            for name,inst in instance_.__call__.__annotations__.items():
                if isinstance(message,inst):
                    criterias["command_type_hint"] = True
                    break

        elif p["type"] == "function":
            for name,inst in p["controller"].__annotations__.items():
                if isinstance(message,inst):
                    criterias["command_type_hint"] = True
                    break

        # critères d'invalidité
        if transport_attributes.get("transport") and p.get("transport") != transport_attributes.get("transport"):
            criterias = {k:False for k,v in criterias.items()}

        if transport_attributes.get("bus") and p.get("bus") != transport_attributes.get("bus"):
            criterias = {k:False for k,v in criterias.items()}


        # check de validation globale
        if len(criterias):
            for k,v in criterias.items():
                if v == False:
                    is_ok = False
                    break

            if is_ok:
                _handlers_selected.append(p)

    _handlers_selected.sort(key=lambda i: i["priority"], reverse=True)

    for p in _handlers_selected:
        callback = p["callback"]
        properties = transport_attributes
        ret = None

        if isinstance(transport, AMQPTransport):
            amqpStamp: AmqpStamp = envelope.last("AmqpStamp")
            if amqpStamp:
                properties = amqpStamp.attributes.__dict__

        argv = [envelope.message]
        argc = 1
        if p["type"] == "class":
            callback = callback()
            argc = len(callback.__call__.__annotations__)

        elif p["type"] == "function":
            argc = len(p["controller"].__annotations__)

        if (argc >= 2):
            argv.append(properties)
        ret = callback(*argv)

        if ret:
            envelope = envelope.update(ResultStamp(ret))

    return envelope

class MessageHandlerInterface:

    def __call__(self, message):
        raise NotImplementedError

class HandlerInterface:

    def __init__(self, binding_key:str, priority:int = 0):
        self._binding_key = binding_key
        self.priority = priority

    def check(self,binding_key:str = "") -> bool:
        match = re.search(r"^{}$".format(self._binding_key), binding_key)
        return True if match else False

    def start(self,binding_key:str, payload:dict,properties:dict={}):
        if self.check(binding_key):
            return self.run(binding_key,payload,properties)
        return None

    def run(self,binding_key:str, payload:dict, properties:dict={}):
        raise NotImplementedError

    def getUsableBindingKey(self):
        binding_key = self._binding_key
        b = binding_key.split(".")
        if len(b) > 2:
            b.pop()
            binding_key = ".".join(b)
        return binding_key

class HandlerManager:

    def __init__(self, handlers:list=[]):
        self._handlers = []

        for handler in handlers:
            self._add(handler)

        self._handlers.sort(key=lambda el: el.priority, reverse=True)

    def _add(self, handler: HandlerInterface):
        try:
            self._handlers.index(handler)
        except ValueError as e:
            self._handlers.append(handler)
        return self


    def run(self,match:str, payload:dict, properties:dict={}):

        self._handlers.sort(key=lambda el: el.priority, reverse=True)

        for handler in self._handlers:
            rst = handler.start(match, payload, properties)
            if rst:
                return rst

        return None

@handler(transport="async", priority=0)
class DefaultMessageHandler(MessageHandlerInterface):
    def __init__(self):
        super().__init__()

    def __call__(self, message, properties:dict={}):
        from .service_container import handler_manager

        logger.debug("-----> message handled <----: ")
        logger.debug(json.dumps(message)+" / "+json.dumps(properties))
        handler_manager.run(message['action'],message['payload'], properties)
