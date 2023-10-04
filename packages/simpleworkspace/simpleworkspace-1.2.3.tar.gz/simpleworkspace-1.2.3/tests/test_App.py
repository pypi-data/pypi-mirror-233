import json
import simpleworkspace.loader as sw
from simpleworkspace.app import App
from basetestcase import BaseTestCase


class AppTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        App.Setup(self.testAppName, self.testAppCompany)

    def tearDown(self) -> None:
        super().tearDown()
        if self.testAppName in App.path_AppData and self.testAppCompany in App.path_AppData:
            sw.io.directory.Remove(App.path_AppData)
        else:
            raise LookupError("Could not find appcompany and appname in filepath, not removing them for safety precaution")

    def test_settings_json(self):
        App.settingsManager.LoadSettings()
        App.settingsManager.Settings["test1"] = 10
        App.settingsManager.Settings["test2"] = 20
        App.settingsManager.SaveSettings()
        savedSettingData = sw.io.file.Read(App.settingsManager._settingsPath)
        obj = json.loads(savedSettingData)
        self.assertEqual(obj, {"test1": 10, "test2": 20})

    def test_appdata_logging(self):
        App.logger.debug("test log 1")
        App.logger.debug("test log 2")
        App.logger.debug("test log 3")
        for handler in App.logger.handlers:
            handler.flush()
        logData = sw.io.file.Read(App._path_LogFile)
        result = sw.utility.regex.Match(f"/(.*?) (\w+?) <(.*?)>: (.*)/i", logData)
        
        self.assertEqual(len(result),  3)
        self.assertEqual(result[0][4],  "test log 1")
        self.assertEqual(result[1][4],  "test log 2")
        self.assertEqual(result[2][4],  "test log 3")
        pass
