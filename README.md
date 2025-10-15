# Project Folger Structure
```
MLE-REFACTORING-IM/
├── 001_data/
│ └── King_County_House_prices_dataset.csv
├── 002_notebooks/
│ ├── King-County.ipynb
│ └── project-for-today.md
├── 003_scripts/
│ ├── 01.load_data.py
│ ├── 02.clean_data.py
│ ├── 03.feature_engineering.py
│ ├── 04.explore_data.py
│ ├── 05.split_data.py
│ ├── 06.train_model.py
│ ├── 07.evaluate_model.py
│ ├── 08.safe_model.py
│ ├── main.py
│ ├── README.md
│ ├── schemas.py
│ └── utils.py
├── 004_reports_and_images/
│ ├── DS_LC.png
│ ├── king_county_districts.jpeg
│ └── seattle_skyline.jpg
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
```
# Refactoring Project

Please do not fork this repository, but use this repository as a template for your refactoring project. Make Pull Requests to your own repository even if you work alone and mark the checkboxes with an `x`, if you are done with a topic in the pull request message.

## Project for today

The task for today you can find in the [project-for-today.md](./project-for-today.md) file.

## Setup

The necessary libraries are listed in the [requirements.txt](./requirements.txt) file. You can install them with the following commands:

#### **`macOS`**
```BASH
  pyenv local 3.11.3
  python -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
#### **`WindowsOS`**
 For `PowerShell` CLI :

  ```PowerShell
  pyenv local 3.11.3
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

  For `Git-Bash` CLI :

  ```
  pyenv local 3.11.3
  python -m venv .venv
  source .venv/Scripts/activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```