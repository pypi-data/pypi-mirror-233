#  Pyroherd - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present OnTheHerd <https://github.com/OnTheHerd>
#
#  This file is part of Pyroherd.
#
#  Pyroherd is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyroherd is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroherd.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyroherd.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyroherd.raw.core import TLObject
from pyroherd import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class EditAdmin(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``D33C8902``

    Parameters:
        channel (:obj:`InputChannel <pyroherd.raw.base.InputChannel>`):
            N/A

        user_id (:obj:`InputUser <pyroherd.raw.base.InputUser>`):
            N/A

        admin_rights (:obj:`ChatAdminRights <pyroherd.raw.base.ChatAdminRights>`):
            N/A

        rank (``str``):
            N/A

    Returns:
        :obj:`Updates <pyroherd.raw.base.Updates>`
    """

    __slots__: List[str] = ["channel", "user_id", "admin_rights", "rank"]

    ID = 0xd33c8902
    QUALNAME = "functions.channels.EditAdmin"

    def __init__(self, *, channel: "raw.base.InputChannel", user_id: "raw.base.InputUser", admin_rights: "raw.base.ChatAdminRights", rank: str) -> None:
        self.channel = channel  # InputChannel
        self.user_id = user_id  # InputUser
        self.admin_rights = admin_rights  # ChatAdminRights
        self.rank = rank  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditAdmin":
        # No flags
        
        channel = TLObject.read(b)
        
        user_id = TLObject.read(b)
        
        admin_rights = TLObject.read(b)
        
        rank = String.read(b)
        
        return EditAdmin(channel=channel, user_id=user_id, admin_rights=admin_rights, rank=rank)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.user_id.write())
        
        b.write(self.admin_rights.write())
        
        b.write(String(self.rank))
        
        return b.getvalue()
