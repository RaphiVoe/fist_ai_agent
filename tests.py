import unittest
from functions import get_files_info, get_file_content, write_file, run_python_file


class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip
    def test_get_files_info_calculator(self):
        result = get_files_info.get_files_info("calculator", ".")
        #print(result)
        self.assertRegex(result, r"- main\.py: file_size=[0-9]+ bytes, is_dir=False")
        self.assertRegex(result, r"- tests\.py: file_size=[0-9]+ bytes, is_dir=False")
        self.assertRegex(result, r"- pkg: file_size=[0-9]+ bytes, is_dir=True")

    @unittest.skip
    def test_get_files_info_calculator_pkg(self):
        result = get_files_info.get_files_info("calculator", "pkg")
        #print(result)
        self.assertRegex(result, r"- calculator\.py: file_size=[0-9]+ bytes, is_dir=False")
        self.assertRegex(result, r"- render\.py: file_size=[0-9]+ bytes, is_dir=False")

    @unittest.skip
    def test_get_files_info_calculator_bin(self):
        result = get_files_info.get_files_info("calculator", "/bin")
        #print(result)
        self.assertEqual(result, 'Error: Cannot list "/bin" as it is outside the permitted working directory')

    @unittest.skip
    def test_get_files_info_calculator_dir_up(self):
        result = get_files_info.get_files_info("calculator", "../")
        #print(result)
        self.assertEqual(result, 'Error: Cannot list "../" as it is outside the permitted working directory')

    @unittest.skip
    def test_get_file_content_calculator_lorem_ipsum(self):
        result = get_file_content.get_file_content("calculator", "lorem.txt")
        self.assertIn("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", result)
        self.assertEqual(len(result), 10000)

    @unittest.skip
    def test_get_file_content_calculator_main(self):
        result = get_file_content.get_file_content("calculator", "main.py")
        #print(result)
        self.assertIn("def main():", result)
        self.assertIn("if __name__ == \"__main__\":", result)
        self.assertIn("main()", result)
        self.assertLessEqual(len(result), 10000)

    @unittest.skip
    def test_get_file_content_calculator_pkg_calculator(self):
        result = get_file_content.get_file_content("calculator", "pkg/calculator.py")
        #print(result)
        self.assertIn("class Calculator:", result)
        self.assertIn("def __init__(self):", result)
        self.assertIn("def evaluate(self, expression):", result)
        self.assertIn("def _evaluate_infix(self, tokens):", result)
        self.assertIn("def _apply_operator(self, operators, values):", result)

    @unittest.skip
    def test_get_file_content_calculator_bin_cat(self):
        result = get_file_content.get_file_content("calculator", "/bin/cat")
        #print(result)
        self.assertEqual('Error: Cannot read "/bin/cat" as it is outside the permitted working directory', result)

    @unittest.skip
    def test_get_file_content_calculator_pkg_does_not_exist(self):
        result = get_file_content.get_file_content("calculator", "pkg/does_not_exist.py")
        #print(result)
        self.assertEqual('Error: File not found or is not a regular file: "pkg/does_not_exist.py"', result)

    @unittest.skip
    def test_write_file_calculator_lorem_ipsum(self):
        result = write_file.write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        #print(result)
        self.assertEqual(result, 'Successfully wrote to "lorem.txt" (28 characters written)')
        with open("calculator/lorem.txt", "r") as f:
            content = f.read()
        self.assertEqual(content, "wait, this isn't lorem ipsum")

    @unittest.skip
    def test_write_file_calculator_pkg_morelorem(self):
        result = write_file.write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        #print(result)
        self.assertEqual(result, 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)')
        with open("calculator/pkg/morelorem.txt", "r") as f:
            content = f.read()
        self.assertEqual(content, "lorem ipsum dolor sit amet")

    @unittest.skip
    def test_write_file_calculator_tmp_temp(self):
        result = write_file.write_file("calculator", "/tmp/temp", "this should not be allowed")
        #print(result)
        self.assertEqual(result, 'Error: Cannot write to "/tmp/temp" as it is outside the permitted working directory')

    def test_run_python_file_calculator_main(self):
        result = run_python_file.run_python_file("calculator", "main.py")
        print(result)
        self.assertIn("STDOUT:", result)
        self.assertIn("STDERR:", result)
        self.assertIn("Calculator App", result)
        self.assertIn('Usage: python main.py "<expression>"', result)
        self.assertIn('Example: python main.py "3 + 5"', result)

    def test_run_python_file_calculator_main_with_args(self):
        result = run_python_file.run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)
        self.assertIn("STDOUT:", result)
        self.assertIn("STDERR:", result)
        self.assertIn('"expression": "3 + 5"', result)
        self.assertIn('"result": 8', result)

    def test_run_python_file_calculator_tests(self):
        result = run_python_file.run_python_file("calculator", "tests.py")
        print(result)
        self.assertIn("STDOUT:", result)
        self.assertIn("STDERR:", result)

    def test_run_python_file_calculator_dir_up_main(self):
        result = run_python_file.run_python_file("calculator", "../main.py")
        print(result)
        self.assertIn('Error: Cannot execute "../main.py" as it is outside the permitted working directory', result)

    def test_run_python_file_calculator_nonexistent(self):
        result = run_python_file.run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertIn('Error: File "nonexistent.py" not found.', result)

    def test_run_python_file_calculator_lorem_ipsum(self):
        result = run_python_file.run_python_file("calculator", "lorem.txt")
        print(result)
        self.assertIn('Error: "lorem.txt" is not a Python file.', result)


if __name__ == "__main__":
    unittest.main()