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


class StarConfig(LogModel):
    id = fields.IntField(pk=True)
    guild = fields.ForeignKeyField("main.Guild", related_name="star_config")
    star_count = fields.IntField(
        null=True, description="Represents the star threshold of the server"
    )
    channel_id = fields.BigIntField(
        null=True, description="Represents the starboard channel"
    )
    enabled = fields.BooleanField(default=False)

    class Meta:
        table = "star_config"
        table_description = "This table stores information about Starboard"


class StarboardEntries(LogModel):
    id = fields.IntField(pk=True)
    guild = fields.ForeignKeyField("main.Guild", related_name="starboard_entries")
    channel_id = fields.BigIntField(
        null=True, description="Represents channel ID of the starred message"
    )
    message_id = fields.BigIntField(
        null=True, description="Represents ID of the starred message"
    )
    starboard_message_id = fields.BigIntField(
        null=True, description="Represents the ID of the starboard message"
    )

    class Config:
        table = "starboard_entries"
        table_description = "This table stores all the starboard entries of a server."
