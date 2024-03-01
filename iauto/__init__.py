"""
`iauto` is a Low-Code intelligent automation tool that integrates LLM and RPA.

Classes:
* Playbook
* PlaybookExecutor
"""

from .actions import Playbook, PlaybookExecutor
from .agents import _actions
from .llms.actions import register_actions as register_llm_actions

VERSION = "0.1.6"
"""The current version."""

# Register actions

register_llm_actions()

__all__ = [
    "Playbook",
    "PlaybookExecutor"
]
