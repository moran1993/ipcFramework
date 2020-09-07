from CORE.Core import ServerCore
import unittest,time

class CoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.Server = ServerCore()
        self.Server.createMainSocketThreadAndRun()

    def test_notBlockSendRequest(self):
        starttime = time
        print(self.Server.sendRequest("OK"))

    def test_blockSendRequest(self):
        print(self.Server.sendRequest("OK",block=True))

if __name__ == "__main__":
    unittest.main()
