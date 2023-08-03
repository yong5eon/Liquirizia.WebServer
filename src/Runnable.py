# -*- coding: utf-8 -*-

from Liquirizia.WebApplication import (
	Request,
	RequestReader,
	ResponseWriter,
)

from abc import ABC, abstractmethod

__all__ = (
	'Runnable'
)


class Runnable(ABC):
	"""Runnable Interface"""

	@abstractmethod
	def run(self, request: Request, reader: RequestReader, writer: ResponseWriter, parameters: dict, version: str, server: str = None):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
