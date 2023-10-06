# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import logging

import climetlab as cml

LOG = logging.getLogger(__name__)


class FileOutput:
    def __init__(self, owner, path, metadata, **kwargs):
        self._first = True
        metadata.setdefault("expver", owner.expver)
        metadata.setdefault("class", "ml")

        LOG.info("Writing results to %s.", path)
        self.path = path
        self.owner = owner
        self.output = cml.new_grib_output(
            path,
            split_output=True,
            edition=2,
            generatingProcessIdentifier=self.owner.version,
            **metadata,
        )

    def write(self, *args, **kwargs):
        return self.output.write(*args, **kwargs)


class HindcastReLabel:
    def __init__(self, owner, output):
        self.owner = owner
        self.output = output

    def write(self, *args, **kwargs):
        if "date" in kwargs:
            date = kwargs["date"]
        else:
            date = kwargs["template"]["date"]

        kwargs["date"] = self.owner.hindcast_reference_date
        kwargs["hdate"] = date
        return self.output.write(*args, **kwargs)


class NoneOutput:
    def __init__(self, *args, **kwargs):
        LOG.info("Results will not be written.")

    def write(self, *args, **kwargs):
        pass


OUTPUTS = dict(
    file=FileOutput,
    none=NoneOutput,
)


def get_output(name, owner, *args, **kwargs):
    result = OUTPUTS[name](owner, *args, **kwargs)
    if owner.hindcast_reference_date is not None:
        result = HindcastReLabel(owner, result)
    return result


def available_outputs():
    return sorted(OUTPUTS.keys())
