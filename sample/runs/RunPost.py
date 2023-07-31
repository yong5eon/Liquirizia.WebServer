# -*- coding: utf-8 -*-

from Liquirizia.WebApplication import RequestRunner, Request
from Liquirizia.WebApplication.Responses import *

from Liquirizia.WebApplication import RequestRunnerProperties

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import *

from errors import *

__all__ = (
	'RunPost'
)


class RunPost(RequestRunner):
	def __init__(self, request: Request, parameters):
		self.request = request
		self.parameters = parameters
		return

	def run(self, body=None):
		return ResponseJSON({
			'parameters': self.parameters,
			'a': self.request.qs['a'] + body['a'],
			'b': self.request.qs['b'] + body['b'],
			'c': self.request.qs['c']
		})


properties = RequestRunnerProperties(
	RunPost,
	method='POST',
	url='/run/:id',
	qs=Validator(
		IsDictionary(
			IsRequiredIn('a', 'b', error=BadRequest('질의에 a 와 b 는 필수 입니다.')),
			IsMappingOf({
				'a': Validator(
					IsNotToNone(error=BadRequest('a 는 값이 있어야 합니다.')),
					ToInteger(error=BadRequest('a는 정수를 필요로 합니다')),
					IsInteger(
						IsGreaterThan(5, error=BadRequest('a 는 5보다 커야 합니다')),
						error=BadRequest('a 는 정수를 필요로 합니다.')
					)
				),
				'b': Validator(
					IsNotToNone(error=BadRequest('b 는 값이 있어야 합니다')),
					ToFloat(error=BadRequest('b는 실수(부동 소수점)을 필요로 합니다')),
					IsFloat(
						IsGreaterThan(9, error=BadRequest('b 는 9보다 커야 합니다')),
						error=BadRequest('b 는 실수(부동 소수점)을 필요로 합니다.')
					)
				),
				'c': Validator(
					SetDefault(''),
					IsString(error=BadRequest('c 는 문자열을 필요로 합니다.'))
				),
			})
		),
	),
	body=Validator(
		IsNotToNone(error=BadRequest('본문에는 값이 있어야 합니다.')),
		IsDictionary(
			IsRequiredIn('a', 'b', error=BadRequest('본문에 a 와 b 가 필요합니다')),
			IsMappingOf({
				'a': Validator(
					IsNotToNone(error=BadRequest('a 는 값이 있어야 합니다.')),
					ToInteger(error=BadRequest('a는 정수를 필요로 합니다')),
					IsInteger(
						IsLessThan(5, error=BadRequest('a 는 5보다 작아야 합니다')),
						error=BadRequest('a 는 정수를 필요로 합니다.')
					)
				),
				'b': Validator(
					IsNotToNone(error=BadRequest('b 는 값이 있어야 합니다')),
					ToFloat(error=BadRequest('b는 실수(부동 소수점)을 필요로 합니다')),
					IsFloat(
						IsLessThan(9, error=BadRequest('b 는 9보다 작아야 합니다')),
						error=BadRequest('b 는 실수(부동 소수점)을 필요로 합니다.')
					)
				),
			}),
		),
	)
)
