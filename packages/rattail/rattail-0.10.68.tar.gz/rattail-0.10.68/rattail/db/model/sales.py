# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Data models for sales
"""

import sqlalchemy as sa

from .core import Base, uuid_column


class Tender(Base):
    """
    Represents a tender for taking payment, or tracking thereof.
    """
    __tablename__ = 'tender'
    __versioned__ = {}

    uuid = uuid_column()

    code = sa.Column(sa.String(length=10), nullable=True, doc="""
    Unique code for the tender.
    """)

    name = sa.Column(sa.String(length=100), nullable=True, doc="""
    Common name for the tender.
    """)

    notes = sa.Column(sa.Text(), nullable=True, doc="""
    Extra notes to describe the tender.
    """)

    def __str__(self):
        return str(self.name or '')
