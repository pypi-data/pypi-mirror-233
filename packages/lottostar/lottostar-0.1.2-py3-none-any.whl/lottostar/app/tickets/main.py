"""
Ticket module
"""
from dataclasses import dataclass
from typing import Optional
from lottostar.app.ballsets.main import BallSet


@dataclass
class Ticket:
    """
    Ticket class.
    Constructs a ticket from a ballset
    """
    ballset: BallSet
    ticket_number: Optional[int] = None
