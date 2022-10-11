# Create models here
from tortoise import fields
from tortoise.models import Model

from mantra.config import bot_config


class LogModel(Model):
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        abstract = True


class Guild(LogModel):
    id = fields.BigIntField(pk=True, description="ID of the Server")
    prefix = fields.TextField(
        default=bot_config.prefix,
        max_length=10,
        description="Custom Prefix for the server",
    )

    class Meta:
        """Class to set the table name and description"""

        table = "guilds"
        table_description = "Stores information about the guild."
