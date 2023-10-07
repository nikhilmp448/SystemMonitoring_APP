# System Monitoring APP
This application is used to monitor our daily works time spend on each activity on a system


https://github.com/nikhilmp448/SystemMonitoring_APP/assets/92564201/15cf34b2-0258-496b-9e59-7f86a01d5829



## Features
track our daily worktime when starts the System Monitoring APP
shares the details to google spreadsheet after clicking stop button
## Requirements
Before running the application, ensure you have the following dependencies installed:

Python 3.x
Tkinter (usually included with Python)
You can install other required packages using pip:

```console
pip install -r requirements.txt
```
## Running the Application
Follow these steps to run the System Monitoring application:

1) Clone or download the repository to your local machine.

2) Open a terminal or command prompt and navigate to the project directory.

3) Run the application script using Python:
```console
python gui.py
```
This command will start the application, and the GUI window will appear.

4) Use the application's GUI to perform the following actions:

    * click start button to start the application
    * click stop button after your all work is over 
    * you can see your time track on google spread sheet
      
5) Enjoy using the SystemMonitoring_APP!

## Building an Executable
If you want to create an executable file to run the application without Python and its dependencies, you can use a tool like PyInstaller. Follow the instructions in the section above titled "Creating an Executable File" to package the application.


## Steps to Create an Executable
Follow these steps to create an executable file for the SystemMonitoring_APP:

1) Install PyInstaller: If you haven't already installed PyInstaller, do so by running the following command:
```console
pip install pyinstaller
```
2) Navigate to the Application Directory: Open a terminal or command prompt and navigate to the directory containing your SystemMonitoring_APP source code.

3) Generate the Spec File: Use PyInstaller to generate a spec file for your application. Replace your_script.py with the name of your Python script:

```console
pyinstaller --name SystemMonitoring_APP --onefile gui.py
```

This command will start the build process, and PyInstaller will create the executable file in a dist directory within your project folder.

5) Distribute the Executable: You can now distribute the executable file to users on different platforms:

On Linux: The generated executable can be run directly.
On Windows: The generated executable will have a ".exe" extension and can be run as a Windows application.
On macOS: The generated executable will be a macOS application bundle. Users can run it by double-clicking.
6) Run the Executable: Test the executable on the respective platform to ensure it works as expected.

## Notes

This application was developed using Python and may have platform-specific considerations when creating executables for Windows, Linux, and macOS.


For any issues, questions, or suggestions, please feel free to contact the developer [a link](https://github.com/nikhilmp448/).


