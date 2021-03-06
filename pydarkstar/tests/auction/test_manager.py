import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ...auction.manager import Manager
from ...database import Database
from ...rc import sql

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = Database.pymysql(**sql)
        self.ob = Manager(self.db, fail=True)

    def test_init(self):
        pass