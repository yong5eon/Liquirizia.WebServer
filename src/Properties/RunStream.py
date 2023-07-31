# -*- coding: utf-8 -*-

from Liquirizia.WebApplication import (
	Request,
	RequestStreamRunner,
	RequestReader,
	ResponseWriter,
	CrossOriginResourceSharing,
)
from Liquirizia.WebApplication import Error
from Liquirizia.WebApplication.Properties import Responsible

from Liquirizia.Validator import Validator

from ..Route import Route
from ..Runnable import Runnable

__all__ = (
	'RunStream'
)


class RunStream(Route, Runnable):
	"""
	Runner to serve output stream web application
	"""

	def __init__(
		self,
		object: type(RequestStreamRunner),
		method: str,
		url: str,
		qs: Validator = None,
		cors=CrossOriginResourceSharing(),
	):
		super(RunStream, self).__init__(method, url, cors=cors)
		self.object = object
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
			if self.qs:
				request.qs = self.qs(request.qs)
	
			obj = self.object(request, parameters)
			# TODO : set headers from route to writer
			response = obj.run(reader, writer)
			return response
		except Error as e:
			if isinstance(e, Responsible):
				writer.send(e.response(), headers=self.headers(request))
				return e.response()
			raise e
	