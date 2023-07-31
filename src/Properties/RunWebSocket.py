# -*- coding: utf-8 -*-

from Liquirizia.WebApplication import (
	Request,
	RequestWebSocketRunner,
	RequestReader,
	ResponseWriter,
	WebSocket,
	CrossOriginResourceSharing,
)

from Liquirizia.WebApplication import Error
from Liquirizia.WebApplication.Errors import (
	NotAcceptableError,
)
from Liquirizia.WebApplication.Properties import Responsible

from Liquirizia.Validator import Validator

from ..Route import Route
from ..Runnable import Runnable

__all__ = (
	'RunWebSocket'
)


class RunWebSocket(Route, Runnable):
	"""
	Runner to serve web socket application
	"""

	def __init__(
		self,
		object: type(RequestWebSocketRunner),
		url: str,
		protocol: str = None,
		qs: Validator = None,
		cors=CrossOriginResourceSharing(),
	):
		super(RunWebSocket, self).__init__('GET', url, cors=cors)
		self.object = object
		self.protocol = protocol
		self.qs = qs
		return

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
		parameters: dict,
		version: str,
		server: str = None
	):
		try:
			if self.protocol and self.protocol != request.header('Sec-WebSocket-Protocol'):
				raise NotAcceptableError(reason='{} is not acceptable protocol'.format(request.header('Sec-WebSocket-Protocol')))
	
			if self.qs:
				request.qs = self.qs(request.qs)
						
			obj = self.object(request, parameters)
			# TODO : set headers from route to writer
			ws = WebSocket(reader, writer)
			ws.switch(request.header('Sec-WebSocket-Key'), protocol=request.header('Sec-WebSocket-Protocol'))
			ws.begin()
			ws.run(obj.run)
			ws.end()
			return
		except Error as e:
			if isinstance(e, Responsible):
				writer.send(e.response(), headers=self.headers(request))
				return e.response()
			raise e
