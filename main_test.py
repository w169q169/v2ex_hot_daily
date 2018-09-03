import unittest
from datetime import datetime
import main
import os
import mock

def mocked_requests_get(*args, **kwargs):
    class MockedResponse:
        def __init__(self, response_text, status_code):
            self.text = response_text
            self.status_code = status_code
    

    data = ""
    with open("./test.html", "r") as testFile:
        data = testFile.read()

    if args[0] == "https://www.v2ex.com/?tab=hot":
        return MockedResponse(data, 200)

def mocked_requests_get_failed(*args, **kwargs):
    class MockedResponse:
        def __init__(self, response_text, status_code):
            self.text = response_text
            self.status_code = status_code
    
    if args[0] == "https://www.v2ex.com/?tab=hot":
        return MockedResponse('', 500)

class TestDict(unittest.TestCase):

    @mock.patch("os.makedirs")
    def test_getDir(self, mock_makedirs):
        dateStr = '1991-10-10 23:40:00'
        time = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
        prefix = "json"

        targetDir = main.getDir(time, prefix)
        mock_makedirs.assert_called_once_with(targetDir)

    @mock.patch("os.open")
    def test_saveJsonData(self, mock_open):
        data = []
        json_file = "./data/json/1991/01/01.json"
        main.save_json_data(data, json_file)
        mock_open.assert_called_once_with(json_file, 'w');

    @mock.patch("codecs.open")
    def test_saveMdData(self, mock_open):
        data = []
        dateStr = '1991-10-10 23:40:00'
        time = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")

        md_file = "./data/md/1991/01/01.md"
        main.save_md_data(data, time, md_file)
        mock_open.assert_called_once_with(md_file, 'w', "utf-8");

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_getHotList(self, mock_get):
        retList = main.get_hot_list()

        self.assertTrue(len(retList) == 34)

    @mock.patch("requests.get", side_effect=mocked_requests_get_failed)
    def test_getHotListFailed(self, mock_get):
        retList = main.get_hot_list()
        self.assertTrue(len(retList) == 0)


if __name__ == '__main__':
    unittest.main()
