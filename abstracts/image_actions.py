from abc import ABC, abstractmethod
import torch

class ImageActions(ABC):

	@classmethod
	@property
	def device(cls):
		return "cuda" if torch.cuda.is_available() else "cpu"

	@abstractmethod
	def action(self, **kwargs):
		pass
