from tortoise import fields
from tortoise.models import Model


class SavedTrack(Model):
    id = fields.TextField(primary_key = True)
    audio_file_id = fields.TextField()