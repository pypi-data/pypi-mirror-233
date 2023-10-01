from __future__ import annotations

from typing import TYPE_CHECKING, List

from likeinterface.methods.base import Method, Request
from likeinterface.types import Hand

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class GetEvaluationResult(Method[List[Hand]]):
    """
    Use this method to evaluate hands.

    Parameters
      Name     | Type            | Required | Description

      1. board | Array of String | Yes      | Card table, for example, ["Ac", "As", "Ah", "Ad", "Td"]

      2. hands | Array Of String | Yes      | Player hand, for example, ["2c2h", "2d2s"]

    Result
      Array of :class:`likeinterface.types.hand.Hand`
    """

    __name__ = "like/getEvaluationResult"
    __returning__ = List[Hand]

    board: List[str]
    hands: List[str]

    def request(self, interface: Interface) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
