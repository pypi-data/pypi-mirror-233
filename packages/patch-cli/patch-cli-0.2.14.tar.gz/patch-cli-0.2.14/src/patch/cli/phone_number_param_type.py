import typing as t

import click
import phonenumbers

from patch.tp.phone_number import PhoneNumber


class PhoneNumberParamType(click.ParamType):
    #  pylint: disable=no-init

    name = 'Phone Number'

    def convert(self, value: t.AnyStr, _param, _ctx) -> t.Optional[PhoneNumber]:
        if value is None:
            return None
        if not value.startswith("+"):
            self.fail(click.style("Phone numbers must begin with a country code, prefixed with `+`", fg="red"))
        ph = phonenumbers.parse(value)
        return PhoneNumber(ph.national_number, ph.country_code)
