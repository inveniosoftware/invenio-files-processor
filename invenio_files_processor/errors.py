# SPDX-FileCopyrightText: 2020 CERN.
# SPDX-License-Identifier: MIT

"""Processor errors."""


class ProcessorError(Exception):
    """Base class for Processor errors."""

    def __init__(self, processor):
        """Initialize exception."""
        self.processor = processor


class DuplicatedProcessor(ProcessorError):
    """Processor is already registered."""

    def __str__(self):
        """Return description."""
        return "Processor {} is already registered.".format(self.processor)


class UnsupportedProcessor(ProcessorError):
    """Processor is not supported."""

    def __str__(self):
        """Return description."""
        return "Processor {} is not supported.".format(self.processor)


class InvalidProcessor(ProcessorError):
    """Processor is not registered."""

    def __init__(self, processor, file):
        """Initialize exception."""
        self.file = file
        super().__init__(processor)

    def __str__(self):
        """Return description."""
        return "Processor {id} can't be applied to file {file}.".format(
            id=self.processor,
            file=self.file
        )
