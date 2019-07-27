# -*- coding: utf-8 -*-
import os,sys
import asyncio
path = os.path.join(os.path.dirname(__file__), '../lib/')
sys.path.insert(0, path)

from . import config
from .http_client import HttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
from frugal.provider import FServiceProvider
from frugal.context import FContext

from .proto import LegyProtocolFactory

from .lib.Gen import f_LineService
from .lib.Gen.ttypes import *

class Connection(object):
	def __init__(self, uri_path):
		self.context = FContext()
		self.transport = HttpClient(config.BASE_URL + uri_path)
		self.protocol_factory = TCompactProtocolAcceleratedFactory()
		self.wrapper_factory  = LegyProtocolFactory(self.protocol_factory)
		self.service_provider = FServiceProvider(self.transport, self.wrapper_factory)
		
		self.client = self.ClientFactory()

	def call(self, rfunc: str, *args, **kws) -> callable:
		"""
		Call function from Line Service Client
		args:
			rfunc: pass a string valid attribute from <f_LineService.Client>
			args: pass a args from attribute rfunc
			kws: same as args
		
		Return:
			bool == True or callable
		"""
		assert isinstance(rfunc, str), 'Function name must be str not '+type(rfunc).__name__
		rfr = getattr(self.client, rfunc, None)
		if rfr:
			return rfr(self.context, *args, **kws)
		else:
			raise Exception(rfunc + ' is not exist')

	def renew(self):
		self.client = self.ClientFactory()

	def ClientFactory(self):
		return f_LineService.Client(self.service_provider)
		
	def setHeaders(self, dict_key_val):
		self.transport._headers = map_key_val
		
	def updateHeaders(self, dict_key_val):
		self.transport._headers.update(dict_key_val)
		
	def url(self, path='/'):
		self.transport._url = config.BASE_URL + path
