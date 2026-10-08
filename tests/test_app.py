import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
import main  # noqa: E402


class TestApp(unittest.TestCase):
    def test_env_values_are_used(self):
        info = main.student_info({"STUDENT_NAME": "A", "STUDENT_SURNAME": "B",
                                  "STUDENT_GROUP": "G", "STUDENT_ID": "1"})
        self.assertEqual(info["name"], "A")
        self.assertEqual(info["student_id"], "1")

    def test_defaults_exist(self):
        self.assertEqual(main.student_info({})["surname"], "Boyarkin")

    def test_banner_contains_success_message(self):
        text = main.banner(main.student_info({}))
        self.assertIn("Application is running successfully!", text)
        self.assertIn("Student ID: 37752", text)


if __name__ == "__main__":
    unittest.main()
