import base64
from PIL import Image
from io import BytesIO
from config import Config

class Icon:

    @staticmethod
    def image_to_base64(image_path, size=(40, 40)):
        """Reads an image, resizes it, and converts it to a Base64 string."""
        with Image.open(image_path) as img:
            #img = img.resize(size)  # Resize the image to 40x40 pixels

            # Save image to a bytes buffer
            buffered = BytesIO()
            img.save(buffered, format="PNG")  # You can change format if needed (JPEG, etc.)

            # Convert to Base64
            return base64.b64encode(buffered.getvalue()).decode("utf-8")

    # # Example usage:
    # image_path = "your_image.jpg"  # Change to your image file path
    # base64_str = image_to_base64(image_path)
    # print(base64_str)  # Output the Base64 string

    @staticmethod
    def draw(x, y, element_id, image_id, link, width=Config.image_width, height=Config.image_height):
        element={
              "id": f"{element_id}",
              "type": "image",
              "x": x,
              "y": y,
              "width": width,
              "height": height,
              "angle": 0,
              "strokeColor": "transparent",
              "backgroundColor": "#f8f1ee",
              "fillStyle": "cross-hatch",
              "strokeWidth": 1,
              "strokeStyle": "solid",
              "roughness": 0,
              "opacity": 100,
              "groupIds": [],
              "frameId": None,
              "index": "b0O",
              "roundness": None,
              "isDeleted": None,
              "boundElements": [],
              "link": link,
              "locked": False,
              "status": "saved",
              "fileId": f"{image_id}",
              "scale": [
                1,
                1
              ],
              "crop": None
            }
        return element

    @staticmethod
    def file_element(image_hash, image_base64):
        file = {
                "mimeType": "image/png",
                "id": f"{image_hash}",
                "dataURL": f"data:image/png;base64,{image_base64}"
        }
        return file
