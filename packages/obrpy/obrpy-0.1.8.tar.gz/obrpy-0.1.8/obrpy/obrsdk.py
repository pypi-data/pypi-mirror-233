import subprocess
import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), 'obrsdk'))

def OBRSDKcalibration(self, verbose=True) -> None:
    """ Performs Luna's OBR-4600 calibration
     
        Only works in a Windows environment :( 
    
    """
    try: 

        current_directory = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')

        output = subprocess.check_output(f"{exe_path} -c")

        if verbose:
            for line in output.splitlines():
                print(line)

    except subprocess.CalledProcessError as e:
        # Extract the exit status from the error message
        exit_status_match = re.search(r'non-zero exit status (\d+)', str(e))
        if exit_status_match:
            exit_status = int(exit_status_match.group(1))
            print(f"Error: The subprocess exited with non-zero exit status: {exit_status}. Try running OBRSDKinstallLibraries() to fix the error.")
        else:
            print(f"Error running the application: {str(e)}")


def OBRSDKalignment(self,verbose=True) -> None:
    """ Performs Luna's OBR-4600 optical alignment         
    
        Only works in a Windows environment :( 
    
    """

    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')
        
        output = subprocess.check_output(f"{exe_path} -a")

        if verbose:
            for line in output.splitlines():
                print(line)

    except subprocess.CalledProcessError as e:
        # Extract the exit status from the error message
        exit_status_match = re.search(r'non-zero exit status (\d+)', str(e))
        if exit_status_match:
            exit_status = int(exit_status_match.group(1))
            print(f"Error: The subprocess exited with non-zero exit status: {exit_status}. Try running OBRSDKinstallLibraries() to fix the error.")
        else:
            print(f"Error running the application: {str(e)}")

def OBRSDKscan(self,filepath:str,verbose=True):
    """ Acquires measurement

        * param: filepath: path to save the .obr file

        Only works in a Windows environment :( 

    """
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')

        output = subprocess.check_output(f"{exe_path} -s {filepath}")

        if verbose:
            for line in output.splitlines():
                print(line)

    except subprocess.CalledProcessError as e:
        # Extract the exit status from the error message
        exit_status_match = re.search(r'non-zero exit status (\d+)', str(e))
        if exit_status_match:
            exit_status = int(exit_status_match.group(1))
            print(f"Error: The subprocess exited with non-zero exit status: {exit_status}. Try running OBRSDKinstallLibraries() to fix the error.")
        else:
            print(f"Error running the application: {str(e)}")

    return

def OBRSDKextendedScan(self,filepath:str,verbose=True):
    """ Acquires measurement in extended scan format (less precission)

        * param: filepath: path to save the .obr file

        Only works in a Windows environment :( 
    
    """

    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')

        output = subprocess.check_output(f"{exe_path} -e {filepath}")

        if verbose:
            for line in output.splitlines():
                print(line)

    except subprocess.CalledProcessError as e:
        # Extract the exit status from the error message
        exit_status_match = re.search(r'non-zero exit status (\d+)', str(e))
        if exit_status_match:
            exit_status = int(exit_status_match.group(1))
            print(f"Error: The subprocess exited with non-zero exit status: {exit_status}. Try running OBRSDKinstallLibraries() to fix the error.")
        else:
            print(f"Error running the application: {str(e)}")

    return


def OBRSDKinstallLibraries(self):
    """ Function to install necesary Visual C++ redistributable libaries """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Path to the Visual C++ redistributable installer
    vc_redist_path = os.path.join(current_directory, 'obrsdk' , 'vcredist_x86.exe')

    # Check if the installer exists
    if os.path.isfile(vc_redist_path):
        # Execute the installer for Visual C++ redistributable
        install_command = f'{vc_redist_path}'
        subprocess.run(install_command, shell=True)
        print("Visual C++ redistributable installed successfully.")
    else:
        print("Visual C++ redistributable installer not found.")
