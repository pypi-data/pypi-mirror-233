import os
import sys
import argparse



class DirectoryNotFoundError(Exception):
    pass


def set_root_directory(directory):
    """
    Generate a Python command to add the root directory to sys.path.
    """
    cmd = f"""import os, sys
current_path = os.path.normpath(os.getcwd())
root_path = os.path.join(current_path.split(os.sep + '{directory}')[0], '{directory}')"""
    return cmd

def generate_module(module_name,directory=".",root_directory=(os.getcwd().split(os.sep))[-1],is_module_only=True):
    """
    Generate a module and __init__.py (in case of package) files in the specified directory.
    Most importantly set root directory  and add root directory path to sys path so that absolute path imports will work
    even in child modules.
    To add root directory path to sys path manually and import parent modules, check the below link:
    https://www.geeksforgeeks.org/python-import-from-parent-directory/

    NOTE: 
    Relative path import wont work with this package. 
    Recommended to use the package from root directory and create all modules and packages from root itself.

    Args:
        module_name (str): The name of the module to create.
        directory (str, optional): The directory where the module should be created. Defaults to current path "."
        root_directory (str, optional): The root directory for sys.path. Defaults to current folder.
                                        The root directory must be the same working directory or one of its parent directory.
                                        Can never be the child of current working directory.
        is_module_only (Boolean, optional): If True, sys path will be updated only in __init__.py 
                                            else if False, sys path will be updated in the module ({module_name}.py) itself
                                            so that when running as main, won't throw error while importing parent modules 
    """
    try:
        if root_directory not in (os.getcwd().split(os.sep)):
            raise DirectoryNotFoundError(f"Directory '{root_directory}' not found in the current path. Hence, cannot be set as root directory.")
    
        #If no directory given, then no __init__.py file needs to be created as it won't be a package
        if directory !=".":

            # Normalize the directory path to handle different OS path separators
            directory = os.path.normpath(directory)

            # Split the directory path into individual folder names
            folders = directory.split(os.sep)
        else:
            folders=[]

        # Create the intermediate directories as needed and __init__.py files
        current_path = ""
        for folder in folders:
            current_path = os.path.join(current_path, folder)

            # Create the directory if it doesn't exist
            if not os.path.exists(current_path):
                os.makedirs(current_path)

            # Create the __init__.py file if it doesn't exist
            init_file = os.path.join(current_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write(f"""#adding the root directory to sys path\n{set_root_directory(root_directory)}""") 

        # Create the module file with the specified name
        module_file = os.path.join(current_path, f"{module_name}.py")
        if not os.path.exists(module_file):
            with open(module_file, "w") as f:

                #If directory is present, then will be handled like a child module
                #Parent module imports must be handled 
                if current_path:

                    #If the module will not be used as main, then the __init__.py code will handle parent module imports
                    #Hence, no additional lines needed in module itself
                    if is_module_only:
                        f.write("")

                    #If module is set to be used as main as well, then root directory must be added to sys path
                    #explicitly in the module itself to avoid any errors while importing
                    else:
                        f.write(f"""#adding the root directory to sys path\n{set_root_directory(root_directory)}\n#Add remaining imports below\n\n\n\nif __name__=='__main__':\n\t'Your Main code here'""") 
                
                #If no directory is given as input, it is a single module in root folder. 
                #Hence, no need to handle parent module import issue
                else:
                    f.write("")
    
    except DirectoryNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(description="""Generate a module and __init__.py (in case of package) files in the specified directory. Enable parent module imports using absolute paths (from root dir).""")
    parser.add_argument("module_name", help="Name of the module to generate")
    parser.add_argument("--directory", default=".", help="Directory where the module should be created")
    parser.add_argument("--root_directory", default=None, help="The root directory for sys.path. (Default:current folder)")
   
    # Use store_true action for --is_module_only to accept True as the default value
    parser.add_argument("--is_module_only", default=True, action="store_true", help="Specify if the module should be used as a module only")

    # Add --no-is_module_only flag to set is_module_only to False
    parser.add_argument("--not_is_module_only", dest="is_module_only", action="store_false", help="Specify if the module should be used as a main program as well")

    args = parser.parse_args()

    
    # Check for None values and apply defaults
    root_directory = args.root_directory if args.root_directory is not None else (os.getcwd().split(os.sep))[-1]
    generate_module(args.module_name, args.directory, root_directory, args.is_module_only)


if __name__ == '__main__':
    main()



# Example usage:

#Generate a module named "mymodule" in the current directory (default settings):
#pymodulegen mymodule

#Generate a module named "chatgpt" in the "app/api/v1/endpoints" directory with root directory "project-root" and use it as a main program as well:
#pymodulegen chatgpt --directory "app/api/v1/endpoints" --root_directory "project-root" --not_is_module_only

#Generate a package (with __init__.py) named "my_package" in the current directory (default settings) with a module my_module:
#pymodulegen my_module --directory "my_package"






