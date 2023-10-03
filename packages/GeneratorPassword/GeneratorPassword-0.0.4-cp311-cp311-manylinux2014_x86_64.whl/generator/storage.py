# Copyright (C) 2022-2023 AyiinXd <https://github.com/AyiinXd>

# This file is part of GeneratorPassword.

# GeneratorPassword is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GeneratorPassword is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with GeneratorPassword.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sqlite3

logger = logging.getLogger(__name__)


class Storage:
    FILE_EXTENSION = ".session"

    def __init__(self, name: str):
        self.name = name
        self.conn: sqlite3.Connection = None
        self.is_connected: bool = False

    def connect(self):
        conn = sqlite3.connect(self.name + self.FILE_EXTENSION)

        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS password(
                user_id INTEGER,
                key TEXT,
                random_id INTEGER
            );
            CREATE TABLE IF NOT EXISTS discount(
                user_id INTEGER,
                percent INTEGER
            );
            """
        )

        conn.execute("VACUUM")

        conn.commit()

        conn.row_factory = sqlite3.Row

        self.conn = conn
        self.is_connected: bool = True

        logger.info("Database Anda Telah Terhubung.")

    def close(self):
        self.conn.close()

        self.is_connected: bool = False

        logger.info("Database Anda Telah Ditutup.")

    def get_conn(self) -> sqlite3.Connection:
        if not self.is_connected:
            self.connect()

        return self.conn

    def add_password(self, user_id, key, random_id):
        self.conn.execute(
            "INSERT INTO password(user_id, key, random_id) VALUES(?, ?, ?)",
            (user_id, key, random_id),
        )
        self.conn.commit()

    def get_password(self, user_id):
        cursor = self.conn.execute("SELECT * FROM password WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def add_discount(self, user_id, key):
        self.conn.execute(
            "INSERT INTO discount(user_id, percent) VALUES(?, ?)",
            (user_id, key),
        )
        self.conn.commit()

    def get_discount(self, user_id):
        cursor = self.conn.execute("SELECT * FROM discount WHERE user_id = ?", (user_id,))
        return cursor.fetchall()
