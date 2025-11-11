@echo off
REM Set your project path
set "PATH_TO_PROJECT=C:\Users\Nico\GitRepos\BillingSystem"

REM Activate the virtual environment and execute billing module
call "%PATH_TO_PROJECT%\.venv\Scripts\activate.bat" & py -m billing -d . -i .
