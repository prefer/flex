import collections

from flex.utils import (
    is_non_string_iterable,
)
from flex.validation.common import (
    validate_object,
)


class ValidationList(list):
    def __init__(self, value=None):
        super(ValidationList, self).__init__()
        if value:
            self.add_validator(value)

    def add_validator(self, validator):
        if is_non_string_iterable(validator)\
           and not isinstance(validator, collections.Mapping):
            for value in validator:
                self.add_validator(value)
        else:
            self.append(validator)

    def validate_object(self, obj):
        validate_object(obj, non_field_validators=self)

    def __call__(self, *args, **kwargs):
        return self.validate_object(*args, **kwargs)


class ValidationDict(collections.defaultdict):
    def __init__(self, validators=None):
        super(ValidationDict, self).__init__(ValidationList)
        if validators is not None:
            if not isinstance(validators, collections.Mapping):
                raise ValueError("ValidationDict may only be instantiated with a mapping")
            for key, validator in validators.items():
                self.add_validator(key, validator)

    def add_validator(self, key, validator):
        self[key].add_validator(validator)

    def update(self, other):
        for key, value in other.items():
            self.add_validator(key, value)

    def validate_object(self, obj):
        """
        Proxy to `flex.validation.common.validate_object`.
        """
        validate_object(obj, field_validators=self)

    def __call__(self, *args, **kwargs):
        return self.validate_object(*args, **kwargs)
