from . import logger
from . import UnseededFunction, SeededOperator, SeededFunction

class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator
	NAME, BASE_FUNC = None, None
	SPACES = ('', '')
	if __debug__:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME


	def _collapse_call_args(self, soper):
		logger.info('TODO: fix _collapse_call_args to work with power')
		START = 0
		call_args = soper.call_args
		from . import MultiOperator
		if isinstance(call_args[START], SeededFunction) and call_args[START].unseeded_base is soper.unseeded_base\
			and isinstance(call_args[START].unseeded_base, MultiOperator):
				if START == 0:
					call_args = call_args[START].call_args + call_args[1:]
				else:
					assert START == -1, 'only other defined one atm'
					call_args = call_args[:-1] + call_args[START].call_args
		soper.call_args = call_args

	#str functions


	def format(self, args):
		'''
		10 - x - y - 1 - 4 - z - 5 #start
		10 - x - y - 5 - z - 5 #collapse
		0 - x - y - z  #condensed
		-x - y - z  #weed out

		'''
		args = tuple(args)

		collapsed_args = self._format_collapse(args)
		condensed_args = self._format_condense(collapsed_args)
		weeded_out_args = self._format_weed_out(condensed_args)
		ret = self._format_complete(weeded_out_args)
		assert isinstance(ret, str), ret
		return ret



	def _format_collapse(self, args):
		'''
		Turn 
			-(10, x, y, 1, 4, z, 5)
		Into
			-(10, x, y, 5, z, 5)
		'''
		return args

	def _format_condense(self, args):
		'''
		Turn 
			-(10, x, y, 5, z, 5)
		Into
			-(0, x, y, z)
		'''
		return args
	
	def _format_weed_out(self, args):
		'''
		Turn 
			-(0, x, y, z)
		Into
			-(x, y, z)
		'''
		return args


	def _format_complete(self, args):
		'''
		Turn 
			-(x, y, z)
		Into
			x - y - z
		'''

		joiner = '{0}{2}{1}'.format(*self.SPACES, self.NAME)
		return joiner.join(self._format_get_parens(args))

	def _format_get_parens(self, args):
		for arg in args:
			if self._needs_parens(arg):
				yield '(%s)' % arg
			else:
				yield str(arg)


	def _needs_parens(self, other):
		if not isinstance(other, SeededOperator):
			return False
		return type(other.unseeded_base) in self.paren_classes

	def _gen_format_args(self, args):
		for arg in args:
			if isinstance(arg, SeededOperator) and not arg.hasvalue():
				assert isinstance(arg.unseeded_base, Operator)
				if self._needs_parens(type(arg.unseeded_base)): #only thing that needs parens are SeededOperator
					yield '(' + str(arg) + ')'
					continue
			yield str(arg)

	def deriv_function(self, *args, du):
		raise NotImplementedError