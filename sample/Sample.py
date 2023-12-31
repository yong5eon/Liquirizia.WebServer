# -*- coding: utf-8 -*-

from Liquirizia.WebServer import Server, ServerHandler

from Liquirizia.System import Signal
from Liquirizia.System.Util import GetProcessId, GetThreadId
from Liquirizia.FileSystemObject import FileSystemObjectHelper
from Liquirizia.FileSystemObject.Implements.FileSystem import FileSystemObject, FileSystemObjectConfiguration

from Liquirizia.WebApplication import RequestFilters

from filters import *

from sys import stdout,stderr


class SampleHandler(ServerHandler):
	def onStart(self, host, port, version, name=None):
		print('START             : {} - {}:{}, {}{}'.format(GetProcessId(), host, port, version, ', {}'.format(name) if name else ''), file=stdout)
		return

	def onStop(self):
		print('STOP              : {}'.format(GetProcessId()), file=stdout)
		return

	def onError(self, e):
		print('ERROR             : {} - {}'.format(GetThreadId(), str(e)), file=stderr)
		if hasattr(e, 'error') and e.error:
			print(e.error, file=stderr)
		if hasattr(e, 'trace') and e.trace:
			print(e.trace, file=stderr)
		return

	def onConnected(self, address, port):
		print('CONNECTED         : {} - {}:{}'.format(GetThreadId(), address, port), file=stdout)
		return

	def onRequest(self, request):
		print('REQUEST           : {} - {} {}'.format(GetThreadId(), request.remote, str(request)), file=stdout)
		return

	def onRequestSuccess(self, request, response=None):
		if response:
			print('REQUEST SUCCEEDED : {} - {} {} - {}'.format(GetThreadId(), request.remote, str(request), str(response)), file=stdout)
		else:
			print('REQUEST SUCCEEDED : {} - {} {}'.format(GetThreadId(), request.remote, str(request)), file=stdout)
		return

	def onRequestError(self, request, e):
		print('REQUEST ERROR     : {} - {} {} - {}'.format(GetThreadId(), request.remote, str(request), str(e)), file=stderr)
		if hasattr(e, 'error') and e.error:
			print(e.error, file=stderr)
		if hasattr(e, 'trace') and e.trace:
			print(e.trace, file=stderr)
		return

	def onClosed(self, address, port):
		print('CLOSED            : {} - {} {}'.format(GetThreadId(), address, port), file=stdout)
		return


if __name__ == '__main__':

	FileSystemObjectHelper.Set(
		'Sample',
		FileSystemObject,
		FileSystemObjectConfiguration('public/images')
	)

	server = Server(name='Sample Web Application Server(Liquirizia.WebServer)', handler=SampleHandler())
	server.addFile('public/view/welcome.html', '/')
	server.addFile('public/favicon.ico', '/favicon.ico')
	server.addFiles('public/css', '/css')
	server.addFileSystemObject(
		FileSystemObjectHelper.Get('Sample'),
		'/thumbs',
		onRequestOrigin=RequestFilters(ToJPEG())
	)
	server.load('runs/*.py')
	# server.load('runs', pattern='*.conf')

	def stop(sig):
		server.stop()
		return

	signal = Signal(Signal.HUP, Signal.INT, Signal.QUIT, Signal.KILL, Signal.STOP, fn=stop)
	signal.attach(Signal.TERM, fn=stop)

	server.run()
