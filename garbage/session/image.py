from pydantic import BaseModel

from garbage.session.character import SessionCharacter

class ImageFile(BaseModel):

    speaker: str
    file: str

class ImageStore(BaseModel):

    image_a : ImageFile = None
    image_b : ImageFile = None

    def set_image_a(self, character: SessionCharacter):

        self.image_a = ImageFile(
            speaker = character.character.name,
            file = character.image_path
        )   

    def set_image_b(self, character: SessionCharacter):

        self.image_b = ImageFile(
            speaker = character.character.name,
            file = character.image_path
        )   