from abc import ABC, abstractmethod

class ImageActions(ABC):

	@abstractmethod
	def action(self, **kwargs):
		pass