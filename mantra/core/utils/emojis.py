from enum import Enum


class Emojis(str, Enum):
    ERROR = "❌"
    SUCCESS = "✅"
    WARNING = "⚠️"
    DELETE = "🗑️"
    FIRST = "<:first:1030527373189324821>"
    PREV = "<:prev:1030527370970538095>"
    NEXT = "<:next:1030527368512680017>"
    LAST = "<:last:1030527366184829039>"
    COPY = "©"
