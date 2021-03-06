from . import logger
from .valued_obj import ValuedObj
from .user_obj import UserObj
class Constant(ValuedObj):
	''' A class representing a mathematical constant, such as '4' or 'pi'

	This class can be directly instantiated, but still requires keyword arguments. The User-class
	UserConstant can be substituted if ease of use is required. However, Constant is much more 
	robust.
	'''
	__slots__ = ('_value', )
	def __str__(self):
		return str(self.value)
	@ValuedObj.value.getter
	def value(self):
		##TODO: FIX THIS
		if self._value is not self._DEFAULT_VALUE:
			return super().value
		return 0

	def isconst(self, du):
		assert self is not du
		assert not du.hasvalue()
		return True
	
class UserConstant(UserObj, Constant):
	''' The UserObj for Constant

	See UserObj for more information on User objects.
	'''
	def __init__(self, value = Constant._DEFAULT_VALUE):
		''' Initiates self.
		
		This function passes 'value' to Constant's constructor, and nothing else.

		Arguments:
			value -- The value of this class. (default: Constant._DEFAULT_VALUE)
		Returns:
			None
		'''
		super().__init__(value = value)


	def _gen_repr(self, args, kwgs):
		assert not args and not kwgs
		if self.hasvalue():
			args = (self.value, )
		return args, kwgs

	__slots__ = ('_value', )



