# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

__all__ = (
	'ServerHandler'
)


class ServerHandler(ABC):
	"""Web Application Server Handler Interface"""

	@abstractmethod
	def onStart(self, host, port, version, name=None):
		raise NotImplementedError('{} must be implemented onStart'.format(self.__class__.__name__))

	@abstractmethod
	def onConnected(self, address, port):
		raise NotImplementedError('{} must be implemented onConnected'.format(self.__class__.__name__))

	@abstractmethod
	def onRequest(self, request):
		raise NotImplementedError('{} must be implemented onRequest'.format(self.__class__.__name__))

	@abstractmethod
	def onRequestSuccess(self, request, response=None):
		raise NotImplementedError('{} must be implemented onRequestSuccess'.format(self.__class__.__name__))

	@abstractmethod
	def onRequestError(self, request, e):
		raise NotImplementedError('{} must be implemented onRequestError'.format(self.__class__.__name__))

	@abstractmethod
	def onClosed(self, address, port):
		raise NotImplementedError('{} must be implemented onClosed'.format(self.__class__.__name__))

	@abstractmethod
	def onError(self, e):
		raise NotImplementedError('{} must be implemented onError'.format(self.__class__.__name__))

	@abstractmethod
	def onStop(self):
		raise NotImplementedError('{} must be implemented onStop'.format(self.__class__.__name__))
