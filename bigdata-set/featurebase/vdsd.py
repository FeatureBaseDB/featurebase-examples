import yaml


ALLOWED_FIELD_OPTIONS = (
    "cache-size",
    "cache-type",
    "packed",
    "min",
    "max",
    "scale",
    "time-quantum",
    "disable-aggregate",
)


class FieldOptions:
    def __init__(self, **kwargs):
        self._opts = {}
        for (k, v) in kwargs.items():
            key = k.replace("_", "-")  # Normalize option names, e.g. cache_type -> cache-type
            if key not in ALLOWED_FIELD_OPTIONS:
                raise TypeError("Invalid field option: " + k)
            self._opts[key] = v

    def as_dict(self):
        return self._opts


class Field:
    def __init__(
        self, name, type, primary_key=False, ignore=False, auto_increment=False, options=None
    ):
        self.name = name
        self.type = type
        self.primary_key = primary_key
        self.ignore = ignore
        self.auto_increment = auto_increment
        self.options = options

    def as_dict(self):
        d = {
            "name": self.name,
            "type": self.type,
            "primary-key": self.primary_key,
            "ignore": self.ignore,
            "auto-increment": self.auto_increment,
        }
        if self.options:
            d["options"] = self.options.as_dict()
        return d


class VDSD:
    fields = None

    def __init__(self, name, description="", fields=None):
        self.version = 1
        self.name = name
        self.description = description
        if fields:
            self.fields = fields

    def as_dict(self):
        doc = {
            "version": self.version,
            "name": self.name,
            "description": self.description,
        }
        if self.fields:
            doc["schema"] = {"fields": []}
            for field in self.fields:
                doc["schema"]["fields"].append(field.as_dict())
        return doc

    def render(self):
        return yaml.dump(self.as_dict(), default_flow_style=False)
