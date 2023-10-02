import unittest
from src import dynamic_heartbeat as dhb


class TestDynamicHeartbeat(unittest.TestCase):
    def test_dynamic_heartbeat(self):

        dhb.main()
