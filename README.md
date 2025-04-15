# QwikSort: Rule-Based File Sorting
![QwikLogo](https://github.com/user-attachments/assets/fd9a0640-dd28-4dc4-a4af-3d903cfec13e)

QwikSort is a file sorting software developed for the Windows 10/11 operating system which utilizes a sorting rule system to give the user deep control over how their files are moved, while also making sorting effecient through mass file operations.

## Features
### Rulesets
- Rulesets are lists of sorting rules, each assigned to a specific folder.
- Users can create new rules on a folder which will be added to the folder's ruleset.
- Rules can be created to sort files based on name contents, file extension, or even creation/modification date.
- Each ruleset can be modified to follow a "Match All" or "Match One" definition, where either all rules or one rule must apply to any given file.
- All rulesets in the current session can be saved to a QwikSort Rulesets (.qsr) file, and loaded whenever the rulesets are needed again.
### File Operations
- By referencing defined rulesets, users can perform mass file move operations by selecting the "Sort" button in the main interface, which querys each file in the target directory and moves it to the folder with the rule it matches with (or no folder if no rulesets apply to the file).
- Users can also mass recycle files by pressing the "Delete" button in the main interface, which provides a warning before confirmation that recycling cannot be undone. Users can restore their files by using the Windows file explorer to navigate to the Recycling Bin and use the "Restore" option on any files.
### Undo & Rollback
- Users can undo the last sorting operation (up to 5 operations) by selecting the **Rollback > Undo** menu option, or by using the shortcut **Ctrl+Z**.
- Users can also create a restore point of the target directory by selecting the **Rollback > Create New Restore Point** menu option, which they can rollback to at any moment with **Rollback > Rollback to Restore Point**. Rollbacks do not consider recycled files.

## Installation
**Prerequisites**
Make sure you have the following installed:
- Python 3.8+
- Git

**Steps**
```
# 1. Clone this repo
git clone https://github.com/omegadc/QwikSort.git
cd projectdirectory

# 2. Create venv
# Windows
python -m venv venv
venv\Scripts\Activate

# 3. Install dependencies
pip install pyside6
pip install send2trash

# 4. Run QwikSort
python main.py
```

## Contributing
This project was originally created as part of a university course and is not being actively maintained.

You are more than welcome to fork the repository and use it for your own learning and projects, but we are not accepting pull requests or issues at this time.

## License
This project is licensed under the MIT license—see the LICENSE file for details.

## Acknowledgements
Made possible by the talented WIT Software Engineering Spring 2025 Group 5:
- Nicholas Jencks
- Kathy Cao
- David Cerna (omegadc)
- Reggie Andrade (reggie-andrade)
