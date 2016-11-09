from . import NonCommutativeOperator, AddOperator, reduce
from . import SeededOperator
class SubOperator(NonCommutativeOperator): # 'x - y'.
	SPACES = AddOperator.SPACES
	NAME = '-'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a - b, args))

	def _format_get_parens(self, args, fancy):
		assert args
		if isinstance(args[0], SeededOperator) and isinstance(args[0].base, AddOperator):
			yield str(args[0])
			args = args[1:]
		for arg in args:
			if self._needs_parens(arg):
				yield '(%s)' % arg
			else:
				yield str(arg)

	deriv_function = AddOperator.deriv_function














