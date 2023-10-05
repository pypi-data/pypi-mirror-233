# -*- coding: utf-8 -*-
import unittest

from axisvm.com.client import start_AxisVM


class TestClient(unittest.TestCase):
    def test_client(self):
        axvm = start_AxisVM(visible=False, daemon=True)
        axvm.Quit()


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
