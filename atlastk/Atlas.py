""" 
MIT License

Copyright (c) 2018 Claude SIMON (https://q37.info/s/rmnmqd49)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import XDHq, XDHqSHRD
from threading import Thread, Lock
import inspect, types, socket, signal, sys, os

from XDHq import set_supplier, get_app_url, l

setSupplier = set_supplier
getAppURL = get_app_url

# Options entries
O_CALLBACKS_PREFIX_ = "CallbacksPrefix"
O_CONNECT_ACTION_AFFIX_ = "ConnectActionName"
O_PREPROCESS_ACTION_NAME_ = "PreprocessActionName"
O_POSTPROCESS_ACTION_NAME_ = "PostprocessActionName"

DEFAULT_CALLBACK_PREFIX = "atk"

options_ = {
  # Prefix of the name of a callback corresponding to an action
  # if absent from callbacks dict.
  # If 'None' or '', callbacks for the actions must be in callbacks dict.
  O_CALLBACKS_PREFIX_: DEFAULT_CALLBACK_PREFIX,
  # The affix for the connect action.
  O_CONNECT_ACTION_AFFIX_: "",
  # NOTA: there is no default callback name for below 2 actions.
  # They must be specifically defined in the callbacks dict.
  # Name of the preprocessing action.
  O_PREPROCESS_ACTION_NAME_: "_Preprocess",
  # Name of the postprocessing action.
  O_POSTPROCESS_ACTION_NAME_: "_Postprocess"
}

if sys.version_info[0] == 2:
	import __builtin__ as builtins
else:
	import builtins

# Overriding some functions for the Dev environment.
if XDHqSHRD.isDev():
	if "openpyxl" in sys.modules :
		defaultXLFunction = sys.modules['openpyxl'].load_workbook
		sys.modules['openpyxl'].load_workbook = lambda filename, **kwargs: defaultXLFunction(XDHq.get_asset_filename(filename), **kwargs)
	
	defaultBuiltinsFunction = builtins.open
	builtins.open = lambda filename, *args, **kwargs: defaultBuiltinsFunction(XDHq.get_asset_filename(filename), *args, **kwargs)

def signal_handler(sig, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def createXML(root_tag):
	return XDHq.XML(root_tag)

create_XML = createXML	

def createHTML(root_tag=""):	# If 'root_tag' is empty, there will be no root tag in the tree.
	return XDHq.XML(root_tag)

create_HTML = createHTML

removePattern_ = lambda string, pattern: string[len(pattern):] if string.startswith(pattern) else string

def broadcastAction(action, id = ""):
	assert isinstance(action, (str, types.FunctionType))

	if isinstance(action, types.FunctionType):
		action = removePattern_(action.__name__, options_[O_CALLBACKS_PREFIX_])

	return XDHq.broadcastAction(action, id)

broadcast_action = broadcastAction


def _call(func, userObject, dom, id, action):
	amount = len(inspect.getfullargspec(func).args)
	args = []

	if not(userObject):
		amount += 1

	if amount == 4:
		args.insert(0, action)

	if amount >= 3:
		args.insert(0, id)

	if amount >= 2:
		args.insert(0 ,dom)

	if userObject and ( amount >= 1 ):
		args.insert(0, userObject)

	return func(*args)

def _is_jupyter():
	try:
			shell = get_ipython().__class__.__name__
			if shell == 'ZMQInteractiveShell':
					return True   # Jupyter notebook or qtconsole
			elif shell == 'TerminalInteractiveShell':
					return False  # Terminal running IPython
			else:
					return 'google.colab' in str(get_ipython())  # Other type (?)
	except NameError:
			return False      # Probably standard Python interpreter

def worker(userCallback, dom, callbacks, callingGlobals):
	args=[]
	userObject = None

	if ( userCallback != None ):
		if ( not(inspect.isclass(userCallback)) and len(inspect.getfullargspec(userCallback).args) == 1 ):
			args.append(dom)

		userObject = userCallback(*args)

	while True:
		[action,id] = dom.getAction()

		if action == "":
			if _is_jupyter():
				dom.disableElement("XDHStyle")
			else:
				dom.disableElement("XDHStyleJupyter")

			if XDHqSHRD.isDev():
				dom.debugLog(True)

			dom.language = id[:id.find(';')]
			id = id[id.find(';')+1:]

		if action == ""\
			or not options_[O_PREPROCESS_ACTION_NAME_] in callbacks\
			or _call(callbacks[options_[O_PREPROCESS_ACTION_NAME_]], userObject, dom, id, action) in [None, True]:

			callback = None

			if action in callbacks:
				callback = callbacks[action]
			elif options_[O_CALLBACKS_PREFIX_]:
				callbackName = options_[O_CALLBACKS_PREFIX_] + ( options_[O_CONNECT_ACTION_AFFIX_] if action == "" else action )

				if callbackName in callingGlobals:
					callback = callingGlobals[callbackName]
			
			if callback:
				dom.callbackReturnValue = _call(callback, userObject, dom, id, action )
				
				if options_[O_POSTPROCESS_ACTION_NAME_] in callbacks:
					_call(callbacks[options_[O_POSTPROCESS_ACTION_NAME_]],userObject, dom, id, action)
			else:
				dom.alert("\tDEV ERROR: missing callback for '" + action + "' action!") 
	
	# l() # Exiting thread, closing corresponding instance.

def _callback(userCallback, callbacks, callingGlobals, instance):
	thread = Thread(target=worker, args=(userCallback, XDHq.DOM(instance), callbacks, callingGlobals))
	thread.daemon = True
	thread.start()
	return thread

def _jupyter_supplier(url):
	global _url, _intraLock

	_url = url.replace('http://', 'https://')
	_intraLock.release()

if _is_jupyter():
	import IPython
	global _intraLock, _thread, _jupyterWidth, _jupyterHeight

	_jupyterWidth = "100%"
	_jupyterHeight = "200px"

	_intraLock = Lock()
	XDHq.set_supplier(_jupyter_supplier)

	_thread = None

	def setJupyterWidth(width):
		global _jupyterWidth

		_jupyterWidth = width

	def setJupyterHeight(height):
		global _jupyterHeight

		_jupyterHeight = height

	def terminate():
		global _thread

		if _thread != None:
			XDHq.setBye(True)
			_thread.join()
			XDHq.setBye(False)
			_thread = None


def _launch(callbacks, callingGlobals, userCallback, headContent, l10n):
	if callbacks == None:
		callbacks = {}

	if callingGlobals == None:
		callingGlobals = {}

	try:
		XDHq.launch(_callback, userCallback, callbacks, callingGlobals, headContent, l10n)
	except socket.timeout:
		pass


def retrieve_(var, id, globals):
  if ( var == None ) and ( id in globals ):
    return globals[id]
  
  return var	
	

def launch(callbacks = None, *, globals = None,  userCallback = None, headContent = None):
	if globals != None:
		callbacks = retrieve_(callbacks, "ATK_CALLBACKS", globals)
		userCallback = retrieve_(userCallback, "ATK_USER", globals)
		headContent = retrieve_(headContent, "ATK_HEAD", globals)
		l10n = retrieve_(None, "ATK_L10N", globals)

	if _is_jupyter():
		global _intraLock, _thread

		terminate()
		
		_intraLock.acquire()
		_thread = Thread(target=_launch, args=(callbacks, globals, userCallback, headContent, l10n))
		_thread.daemon = True
		_thread.start()

		_intraLock.acquire()		

		iframe = IPython.display.IFrame(src = _url, width = _jupyterWidth, height = _jupyterHeight)
		_intraLock.release()
		return iframe
	else:
		_launch(callbacks, globals, userCallback, headContent, l10n)

def options(options = None):
  if options != None:
    global options_

    for key in options:
      if not key in options_:
        raise Exception(f"Unknown option '{key}'!")
      else:
        options_[key] = options[key]

  return options_

def isDev():
	return XDHqSHRD.isDev()