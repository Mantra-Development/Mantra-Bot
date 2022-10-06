from hikari.api.config import CacheComponents
from hikari.impl.config import CacheSettings

CACHE_SETTINGS = (
    CacheSettings(
        components=CacheComponents.GUILDS
        | CacheComponents.GUILD_CHANNELS
        | CacheComponents.ME
        | CacheComponents.MEMBERS
        | CacheComponents.ROLES
        | CacheComponents.VOICE_STATES
    ),
)
