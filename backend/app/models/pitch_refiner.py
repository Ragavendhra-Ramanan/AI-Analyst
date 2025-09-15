from typing import Any, Dict

from pydantic import RootModel


class PitchRefiner(RootModel[Dict[str, Any]]):
    """
    A Pydantic RootModel for parsing arbitrary JSON output.
    """

    pass
