# -*- coding: utf-8 -*-

from Liquirizia.WebApplication.Errors import BadRequestError
from Liquirizia.WebApplication.Properties import Responsible
from Liquirizia.WebApplication.Responses import ResponseBadRequest

__all__ = (
	'BadRequest'
)


class BadRequest(BadRequestError, Responsible):
	def response(self):
		return ResponseBadRequest(str(self), 'text/plain', 'utf-8')
