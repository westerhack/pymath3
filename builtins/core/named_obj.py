from . import logger
from .math_obj import MathObj
class NamedObj(MathObj):
	''' Represents an object that can have a name.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.
	'''

	_default_name = None
	_allowed_name_types = (str, bytes, type(None))
	def __init__(self, *args, name = None, **kwargs):
		'''Initialize self.

		This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
		warning will be logged.

		Arguments:
			*args    -- Ignored
			name     -- The name of this class. (default: None)
			**kwargs -- Ignored
		Returns:
			None
		'''

		if type(self) == NamedObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))

		super().__init__(*args, **kwargs)
		if name is None:
			name = self._default_name
		self.name = name


	name = property(doc = "The name of this class")

	@name.getter
	def name(self):
		return self._name

	@name.setter
	def name(self, newname):
		if hasattr(self, '_name'):
			logger.info('Overriding name {} with {}'.format(self.name, newname))
		if not isinstance(newname, self._allowed_name_types):
			logger.warning("Name is unknown type '{}'. Allowed types: {}".format(
				type(newname).__qualname__,
				', '.join('%r' % x.__qualname__ for x in self._allowed_name_types)))
		self._name = newname

	def hasname(self):
		''' Return true if this this class has a name. '''
		return self.name != self._default_name

	def __str__(self):
		''' Returns a string representation of this class.

		Returns:
			str(self.name)    -- If 'self.hasname()' evaluates to True
			super().__str__() -- If 'self.hasname()' doesn't evaluate to True
		'''
		if self.hasname():
			return str(self.name)

		assert __debug__ or not self.hasname()

		return super().__str__()


	def __repr__(self):
		if self.hasname():
			return '{}(name={!r})'.format(type(self).__qualname__, self.name)
		assert not self.hasname()
		return super().__repr__()
__all__ = ('NamedObj', )








