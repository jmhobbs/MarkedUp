# -*- coding: utf-8 -*-
# http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg00462.html
class Curry:
	# keep a reference to all curried instances·
	# or they are immediately garbage collected
	instances = []
	def __init__(self, func, *args, **kwargs):
		self.func = func
		self.pending = args[:]
		self.kwargs = kwargs.copy()
		self.instances.append(self)

	def __call__(self, *args, **kwargs):
		kw = self.kwargs
		kw.update(kwargs)
		funcArgs = self.pending + args
		# sometimes we want to limit the number of arguments that get passed,
		# calling the constructor with the option __max_args__ = n will limit
		# the function call args to the first n items
		maxArgs = kw.get("__max_args__", -1)
		if maxArgs != -1:
			funcArgs = funcArgs[:maxArgs]
			del kw["__max_args__"]
		return self.func(*funcArgs, **kw)