# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

# Backwards compatibility: helpers.validate_data_dict is defined directly in helpers.py as a lazy
# forwarder to break the circular import that would arise from an eager import here:
#   nexus.nexus_tree → dataconverter.helpers → (this __init__) → validation → nexus.nexus_tree
# Call _apply_monkey_patch() if the real function object is needed (e.g. identity checks).


def _apply_monkey_patch() -> None:
    """Replace the lazy forwarder with the real validate_data_dict from validation."""
    from pynxtools.dataconverter import helpers, validation

    helpers.validate_data_dict = validation.validate_data_dict  # type: ignore
