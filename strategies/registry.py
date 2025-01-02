from strategies.remove_background import RemoveBackground
from abstracts.image_actions import ImageActions

class Registry:
	def __init__(self):
		self.registry = {}

	def register_registry(self, name: str, class_name: str):
		self.registry[name] = class_name

	def get_registry(self, name: str) -> ImageActions:
		action_class = self.registry[name]
		if action_class is not None:
			return action_class()


registry = Registry()
registry.register_registry("rmbg", RemoveBackground)

