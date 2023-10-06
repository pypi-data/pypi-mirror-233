import unittest
import subprocess
import os

class TestPymodulegenCLI(unittest.TestCase):

    def test_help_command(self):
        """
        To test the help command
        """
        # Simulate running '__main__.py --help' in the command line
        result = subprocess.run(['python', os.path.join('src', 'pymodulegen', '__main__.py'), '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(result.returncode, 0)  # Check if the command ran successfully
        self.assertIn("usage: __main__.py", result.stdout)  # Check if the expected help text is present

    def test_create_module_1(self):
        """
        To create a module in the root directory without __init__.py file as it is not a package.
        And the content must be empty as the --is_module_only flag is provided
        """
        # Define the command to run
        cmd = ['python', os.path.join('src', 'pymodulegen', '__main__.py'), 'some_module_1', '--is_module_only']

        try:
            
            # Simulate running the command
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Check if the file 'some_module_1.py' exists
            assert os.path.exists('some_module_1.py'), "Module file 'some_module_1.py' was not created."

            #Check if the file content is empty
            file_size = os.path.getsize('some_module_1.py')
            assert file_size == 0, "Module file 'some_module_1.py' is not empty."

        finally:

            # Clean up: Delete the 'some_module_1.py' file if it exists
            if os.path.exists('some_module_1.py'):
                os.remove('some_module_1.py')

    def test_create_package_1(self):
        """
		src\pymodulegen\__main__.py authentication --directory "api" --is_module_only
        To create a package api in the root directory with __init__.py file.
        And create a module authentication.py under api package and the content must be empty as the --is_module_only flag is provided
        """

        # Define the command to run
        cmd = ['python', os.path.join('src', 'pymodulegen', '__main__.py'), 'authentication','--directory','api','--is_module_only']

        try:
            
            # Simulate running the command
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
			# Check if the folder api exists
            assert os.path.exists('api'), "Directory 'api' was not created."
			
            # Check if the file 'api/authentication.py' exists
            assert os.path.exists(os.path.join('api', 'authentication.py')), "Module file 'api/authentication.py' was not created."

            #Check if the file content is empty
            file_size = os.path.getsize(os.path.join('api', 'authentication.py'))
            assert file_size == 0, "Module file 'api/authentication.py' is not empty."
			
			# Check if the file 'api/__init__.py' exists
            assert os.path.exists(os.path.join('api', '__init__.py')), "Module file 'api/__init__.py' was not created."

            #Check if the file content is as expected
            directory = (os.getcwd().split(os.sep))[-1]
            expected_content=f"root_path = os.path.join(current_path.split(os.sep + '{directory}')[0], '{directory}')"
            with open((os.path.join('api', '__init__.py')),'r') as init_file:
                file_content = init_file.read();
            
            # Perform assertions on the content
            assert expected_content in file_content, "Content of the module file does not match expectations. root_path is wrong."

        finally:

            # Clean up: Delete the 'api' folder, 'api/authentication.py' and 'api/__init__.py' file if it exists
            if os.path.exists('api'):
                for item in os.listdir('api'):
                    item_path = os.path.join('api', item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    else:
                        os.rmdir(item_path)
            os.rmdir('api')
            
    def test_create_package_2(self):
        """
        src\pymodulegen\__main__.py authentication --directory "api" --not_is_module_only
        To create a package api in the root directory with __init__.py file.
        And create a module authentication.py under api package and the content must be having root path sessting as the --not_is_module_only flag is provided
        """
        # Define the command to run
        cmd = ['python', os.path.join('src', 'pymodulegen', '__main__.py'), 'authentication','--directory','api','--not_is_module_only']

        try:
            
            # Simulate running the command
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Check if the folder api exists
            assert os.path.exists('api'), "Directory 'api' was not created."
            
            # Check if the file 'api/authentication.py' exists
            assert os.path.exists(os.path.join('api','authentication.py')), "Module file 'api/authentication.py' was not created."

            #Check if the file content is as expected
            directory = (os.getcwd().split(os.sep))[-1]
            expected_content=f"root_path = os.path.join(current_path.split(os.sep + '{directory}')[0], '{directory}')"
            with open(os.path.join('api','authentication.py'),'r') as init_file:
                file_content = init_file.read();
            
            # Perform assertions on the content
            assert expected_content in file_content, "Content of the module file does not match expectations. root_path is wrong."   
            assert "if __name__=='__main__':" in file_content, "Content of the module file does not match expectations. if __name__=='__main__': is missing"   
            
            
            # Check if the file 'api/__init__.py' exists
            assert os.path.exists(os.path.join('api','__init__.py')), "Module file 'api/__init__.py' was not created."

            #Check if the file content is as expected
            directory = (os.getcwd().split(os.sep))[-1]
            expected_content=f"root_path = os.path.join(current_path.split(os.sep + '{directory}')[0], '{directory}')"
            with open(os.path.join('api','__init__.py'),'r') as init_file:
                file_content = init_file.read();
            
            
            # Perform assertions on the content
            assert expected_content in file_content, "Content of the module file does not match expectations. root_path is wrong."

            
            

        finally:

            # Clean up: Delete the 'api' folder, 'api/authentication.py' and 'api/__init__.py' file if it exists
            if os.path.exists('api'):
                for item in os.listdir('api'):
                    item_path = os.path.join('api', item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    else:
                        os.rmdir(item_path)
            os.rmdir('api')


if __name__ == '__main__':
    unittest.main()

#To run tests use command
#python -m unittest discover -s tests
