from transformers import pipeline
from abstracts.image_actions import ImageActions

class RemoveBackground(ImageActions):

	def action(self, input_path: str, output_path: str) -> str:
		pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)
		pillow_image = pipe(input_path)  # applies mask on input and returns a pillow image
		pillow_image.save(output_path)
		return output_path