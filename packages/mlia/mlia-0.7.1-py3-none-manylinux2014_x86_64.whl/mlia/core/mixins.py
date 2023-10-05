# SPDX-FileCopyrightText: Copyright 2022, Arm Limited and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0
"""Mixins module."""
from __future__ import annotations

from typing import Any

from mlia.core.context import Context


class ContextMixin:
    """Mixin for injecting context object."""

    context: Context

    def set_context(self, context: Context) -> None:
        """Context setter."""
        self.context = context


class ParameterResolverMixin:
    """Mixin for parameter resolving."""

    context: Context

    def get_parameter(
        self,
        section: str,
        name: str,
        expected: bool = True,
        expected_type: type | None = None,
        context: Context | None = None,
    ) -> Any:
        """Get parameter value."""
        ctx = context or self.context

        if ctx.config_parameters is None:
            raise Exception("Configuration parameters are not set")

        section_params = ctx.config_parameters.get(section)
        if section_params is None or not isinstance(section_params, dict):
            raise Exception(
                f"Parameter section {section} has wrong format, "
                "expected to be a dictionary"
            )

        value = section_params.get(name)

        if not value and expected:
            raise Exception(f"Parameter {name} is not set")

        if value and expected_type is not None and not isinstance(value, expected_type):
            raise Exception(f"Parameter {name} expected to have type {expected_type}")

        return value
