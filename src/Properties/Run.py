# -*- coding: utf-8 -*-

from Liquirizia.WebApplication import (
	Request,
	RequestRunner,
	RequestFilter,
	ResponseFilter,
	RequestReader,
	ResponseWriter,
	CrossOriginResourceSharing,
)
from Liquirizia.WebApplication import Error
from Liquirizia.WebApplication.Properties import Responsible

from Liquirizia.WebApplication.Serializer import SerializerHelper
from Liquirizia.Validator import Validator

from ..Route import Route
from ..Runnable import Runnable

__all__ = (
	'Request'
)


class Run(Route, Runnable):
	"""
	Runner Class to serve web application
	"""

	def __init__(
		self,
		object: type(RequestRunner),
		method: str,
		url: str,
		qs: Validator = None,
		body: Validator = None,
		onRequest: RequestFilter = None,
		onRequestOrigin: RequestFilter = None,
		onResponseOrigin: ResponseFilter = None,
		onResponse: ResponseFilter = None,
		cors=CrossOriginResourceSharing(),
	):
		super(Run, self).__init__(method, url, cors=cors)
		self.object = object
		self.onRequest = onRequest
		self.onRequestOrigin = onRequestOrigin
		self.onResponseOrigin = onResponseOrigin
		self.onResponse = onResponse
		self.qs = qs
		self.body = body
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
			if request.size:
				request.body = SerializerHelper.Decode(
					reader.read(request.size),
					format=request.format,
					charset=request.charset,
				)
	
			if self.onRequest:
				request = self.onRequest.run(request)
	
			# TODO : do cache instead of origin
			if self.onRequestOrigin:
				request = self.onRequestOrigin.run(request)
	
			if self.qs:
				request.qs = self.qs(request.qs)
	
			if self.body:
				request.body = self.body(request.body)
	
			obj = self.object(request, parameters)
			response = obj.run(request.body)
	
			if self.onResponseOrigin:
				response = self.onResponseOrigin.run(response)
	
			if self.onResponse:
				response = self.onResponse.run(response)
	
			writer.send(response, headers=self.headers(request))
			return response
		except Error as e:
			if isinstance(e, Responsible):
				writer.send(e.response(), headers=self.headers(request))
				return e.response()
			raise e
