from strategies.remove_background import RemoveBackground
from abstracts.image_actions import ImageActions
from helpers.aws_s3 import AWSS3


class Registry:
	def __init__(self):
		self.strategies = {}

	def register(self, name: str, class_name: str):
		self.strategies[name] = class_name

	def get_strategy(self, name: str) -> ImageActions:
		return self.strategies.get(name)


registry = Registry()
registry.register("rmbg", RemoveBackground(s3=AWSS3()))
