# ME51-25
This GitHub will contain all the code we will mess with in class.

## PIV
To use [open_piv](https://openpiv.readthedocs.io/en/latest/), you will need to 
``` py
pip install openpiv
```
To quickly test, run the sample code (called TheirExample.py).

If you want to use the LabVIEW front end, it will allow you to easily build a UI around your python code (much easier than tkinter or pygame).  You will need to get the latest LabVIEW Community Version from [here](https://www.ni.com/en/support/downloads/software-products/download.labview-community.html?srsltid=AfmBOoqOB9BLQDbdo4P0HVpJtPcjJFU_pPSB6Bp9tKQvbSYrWMcZdUWJ#570612) and the first time you run it, it will ask you where your python is and test to make sure open_piv is installed.  If you do not know where your python is, simply open up Thonny and look at the first line (in grey) in the REPL - it will give you the complete path.


## How to install on Linux
1. Follow the NI instructions; it works pretty simply for 2025Q3: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000YGwsCAG&l=en-IL
   ```
   LabVIEW 2023Q1 and Later (Download feeds package)
With the release of version 2023Q1, LabVIEW is installed using package feeds, which is the usual method of installing software on Linux distributions.

    Download the  .zip file for the LabVIEW version and edition (Community, Full, Pro.) you wish to install.
    Open the .zip file and extract the package file (.rpm or .deb) for your Linux distribution and version. 
    Install the package (e.g., for Ubuntu 20.04 use: sudo apt install ./ni-labview-2023-pro_23.1.0.49229-0+f77-ubuntu2004_all.deb)
    When the package has been installed, refresh the feeds for your package manager.
        For example, with Ubuntu, use: sudo apt update
    The package manager now includes feeds for the repositories that contain the edition of LabVIEW you wish to install.
    Install LabVIEW with the Linux distribution package manager (apt, zypper, or yum)
    The package name is in the format: ni-labview-<version>-<edition>
        The name of the .rpm/.deb file you extracted has the same name formatting, with extra numbers and supported OS. 
        LabVIEW 2023 Professional Edition is called with ni-labview-2023-pro
        Ubuntu use: sudo apt install ni-labview-2023-pro
        You can use the search tools inthe  package manager to find the correct package (e.g., apt search labview-2024)
    Reboot the PC
    Note: The LabVIEW Run Time Engine (RTE) package name is labview-2023-rte.
  ```
2. Go to your terminal and type `which python`.  I use miniconda, so I got: `/home/user/miniforge3/bin/python`, but it's better to create a separate environment where you can install the newest `openpiv-python` and then
```
conda create -n openpiv python=3.12
conda activate openpiv 
pip install openpiv
```
Then `which python` will give you `/home/user/miniforge3/envs/openpiv/bin/python` or similar for your username

3. Run LabVIEW from the Start menu or from the terminal, or open the `LabVIEW_GUI.vi` from the File manager. Initially, I received a request to update Python. I typed 3.12 in the first text box and then Open -> copy/paste the location of Python 3.12 `/home/user/miniforge3/envs/openpiv/bin/python` and things just worked.


<img width="1280" height="1024" alt="image" src="https://github.com/user-attachments/assets/4bf64b2c-ba50-4c62-aca0-89dcad7245d4" />

