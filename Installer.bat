set "log_file=%~dp0installation_log.txt"

call :LOG > %log_file%
exit /B

:LOG
@echo off

echo [%date% %time%] - Installation:
echo -------------------------------------------


set "exe_path=C:\Users\%username%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\CheeseScriptingPlus.exe"
echo Set Variable "exe_path" to "%exe_path%"
set "ico_path=C:\Users\%username%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\CSPICON.ico"
echo Set Variable "ico_path" to "%ico_path%"
set "info_path=C:\Users\%username%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\info.csp"
echo Set Variable "info_path" to "%info_path%"
set "destination_folder=C:\Users\%username%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP"
echo Set Variable "destination_folder" to "%destination_folder%"
set "reg_key=SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\CheeseScriptingPlus"
echo Set Variable "reg_key" to "%reg_key%"
set "app_name=Cheese Scripting +"
echo Set Variable "app_name" to "%app_name%"
set "app_version=Installer Version: VD21M09Y24"
echo Set Variable "app_version" to "%app_version%"
set "app_publisher=Holy Cheese Man"
echo Set Variable "app_publisher" to "%app_publisher%"
set "app_uninstall_string=%destination_folder%\Uninstaller.exe"
echo Set Variable "app_uninstall_string" to "%app_uninstall_string%"
set "install_date=%date:~10,4%%date:~4,2%%date:~7,2%"
echo Set Variable "install_date" to "%install_date%"

set "url_main=https://github.com/HolyCheeseMan/CheeseScriptingPLUS/raw/refs/heads/Main/APP/CheeseScriptingPlus.exe"
echo Set Variable "url_main" to "%url_main%"
set "url_uninstaller=https://github.com/HolyCheeseMan/CheeseScriptingPLUS/raw/refs/heads/Main/APP/Uninstaller.exe"
echo Set Variable "url_uninstaller" to "%url_uninstaller%"
set "url_icon=https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/CSPICON.ico"
echo Set Variable "url_icon" to "%url_icon%"
set "url_info=https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/info.csp"
echo Set Variable "url_info" to "%url_info%"

    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"  

mkdir "%destination_folder%"
echo Created Folder "%destination_folder%"

echo Attempting to download "%url_main%" to "%exe_path%"
curl -L -o "%exe_path%" "%url_main%"

if exist "%exe_path%" (
    for %%A in ("%exe_path%") do set file_size=%%~zA
    echo %exe_path% Installed successfully with size: %file_size% kb.
) else (
    echo Failed to Install %exe_path%
)

echo Attempting to download "%url_uninstaller%" to "%app_uninstall_string%"
curl -L -o "%app_uninstall_string%" "%url_uninstaller%"

if exist "%app_uninstall_string%" (
    for %%A in ("%app_uninstall_string%") do set file_size=%%~zA
    echo %app_uninstall_string% Installed successfully with size: %file_size% kb.
) else (
    echo Failed to Install %app_uninstall_string%
)

echo Attempting to download "%url_icon%" to "%ico_path%"
curl -L -o "%ico_path%" "%url_icon%"

if exist "%ico_path%" (
    for %%A in ("%ico_path%") do set file_size=%%~zA
    echo %ico_path% Installed successfully with size: %file_size% kb.
) else (
    echo Failed to Install %ico_path%
)

echo Attempting to download "%url_info%" to "%info_path%"
curl -L -o "%info_path%" "%url_info%"

if exist "%info_path%" (
    for %%A in ("%info_path%") do set file_size=%%~zA
    echo %info_path% Installed successfully with size: %file_size% kb.
) else (
    echo Failed to Install %info_path%
)

set "userpreferences_path=C:\Users\%username%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\userpreferences.csp"
echo Set Variable "userpreferences_path" to "%userpreferences_path%"

@echo user-preference {>>"%userpreferences_path%"
echo Copied "user-preference {" to "%userpreferences_path%"
@echo	appearance {>>"%userpreferences_path%"
echo Copied "appearance {" to "%userpreferences_path%"
@echo		mode = *Dark*>>"%userpreferences_path%"
echo Copied "mode = *Dark*" to "%userpreferences_path%"
@echo	}>>"%userpreferences_path%"
echo Copied "}" to "%userpreferences_path%"
@echo	last_opened_file {>>"%userpreferences_path%"
echo Copied "last_opened_file {" to "%userpreferences_path%"
@echo		file = *%info_path%*>>"%userpreferences_path%"
echo Copied "file = *%info_path%*" to "%userpreferences_path%"
@echo	}>>"%userpreferences_path%"
echo Copied "}" to "%userpreferences_path%"
@echo }>>"%userpreferences_path%"
echo Copied "}" to "%userpreferences_path%"

reg add "HKLM\%reg_key%" /v "DisplayName" /t REG_SZ /d "%app_name%" /f
if errorlevel 1 echo Failed to create DisplayName for "HKLM\%reg_key%" and "%app_name%"
echo Regedit: DisplayName, for "HKLM\%reg_key%" and "%app_name%"

reg add "HKLM\%reg_key%" /v "DisplayVersion" /t REG_SZ /d "%app_version%" /f
if errorlevel 1 echo Failed to create DisplayVersion for "HKLM\%reg_key%" and "%app_version%"
echo Regedit: DisplayVersion, for "HKLM\%reg_key%" and "%app_version%"

reg add "HKLM\%reg_key%" /v "Publisher" /t REG_SZ /d "%app_publisher%" /f
if errorlevel 1 echo Failed to create Publisher for "HKLM\%reg_key%" and "%app_publisher%"
echo Regedit: Publisher, for "HKLM\%reg_key%" and "%app_publisher%"

reg add "HKLM\%reg_key%" /v "InstallLocation" /t REG_SZ /d "%destination_folder%" /f
if errorlevel 1 echo Failed to create InstallLocation for "HKLM\%reg_key%" and "%destination_folder%"
echo Regedit: InstallLocation, for "HKLM\%reg_key%" and "%destination_folder%"

reg add "HKLM\%reg_key%" /v "UninstallString" /t REG_SZ /d "%app_uninstall_string%" /f
if errorlevel 1 echo Failed to create UninstallString for "HKLM\%reg_key%" and "%app_uninstall_string%"
echo Regedit: UninstallString, for "HKLM\%reg_key%" and "%app_uninstall_string%"

reg add "HKLM\%reg_key%" /v "InstallDate" /t REG_SZ /d "%install_date%" /f
if errorlevel 1 echo Failed to create InstallDate for "HKLM\%reg_key%" and "%install_date%"
echo Regedit: InstallDate, for "HKLM\%reg_key%" and "%install_date%"

reg add "HKLM\%reg_key%" /v "Logo" /t REG_SZ /d "%destination_folder%\CSPICON.ico" /f
if errorlevel 1 echo Failed to create Logo for "HKLM\%reg_key%" and "%destination_folder%\CSPICON.ico%"
echo Regedit: Logo, for "HKLM\%reg_key%" and "%destination_folder%\CSPICON.ico%"

reg add "HKLM\%reg_key%" /v "Icon" /t REG_SZ /d "%destination_folder%\CSPICON.ico" /f
if errorlevel 1 echo Failed to create Icon for "HKLM\%reg_key%" and "%destination_folder%\CSPICON.ico%"
echo Regedit: Icon, for "HKLM\%reg_key%" and "%destination_folder%\CSPICON.ico%"

reg add "HKLM\%reg_key%" /v "DisplayIcon" /t REG_SZ /d "%destination_folder%\CSPICON.ico" /f
if errorlevel 1 echo Failed to create DisplayIcon for "HKLM\%reg_key%" and "%destination_folder%\CSPICON.ico%"
echo Regedit: DisplayIcon, for "HKLM\%reg_key%" and "%destination_folder%\CSPICON.ico%"

reg add "HKLM\%reg_key%" /v "NoModify" /t REG_DWORD /d 1 /f
if errorlevel 1 echo Failed to create NoModify for "HKLM\%reg_key%" and 1
echo Regedit: NoModify, for "HKLM\%reg_key%" and 1

reg add "HKLM\%reg_key%" /v "NoRepair" /t REG_DWORD /d 1 /f
if errorlevel 1 echo Failed to create NoRepair for "HKLM\%reg_key%" and 1
echo Regedit: NoRepair, for "HKLM\%reg_key%" and 1

set "estimated_size=24576"
echo Set Variable "estimated_size" to "%estimated_size%"

reg add "HKLM\%reg_key%" /v "EstimatedSize" /t REG_DWORD /d %estimated_size% /f
if errorlevel 1 echo Failed to create EstimatedSize for "HKLM\%reg_key%" and %estimated_size%
echo Regedit: EstimatedSize, for "HKLM\%reg_key%" and %estimated_size%


set "targetBatchPath=C:\Users\%USERNAME%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\CheeseScriptingPlus.exe"
echo Set Variable "targetBatchPath" to "%targetBatchPath%"
set "shortcutPath=C:\Users\%USERNAME%\downloads\Cheese Scripting +.lnk"
echo Set Variable "shortcutPath" to "%shortcutPath%"
set "iconPath=C:\Users\%USERNAME%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\CSPICON.ico"
echo Set Variable "iconPath" to "%iconPath%"

echo Creating Shortcut

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut("%shortcutPath%") >> "%temp%\CreateShortcut.vbs"
echo Created Shortcut %shortcutPath%
echo oLink.TargetPath = "%targetBatchPath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "%iconPath%, 0" >> "%temp%\CreateShortcut.vbs"
echo Used Icon %iconPath%
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

cscript //nologo "%temp%\CreateShortcut.vbs"

echo Clearing Temp Files

del "%temp%\CreateShortcut.vbs"

set "targetBatchPath=C:\Users\%USERNAME%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\CheeseScriptingPlus.exe"
echo Set Variable "targetBatchPath" to "%targetBatchPath%"
set "shortcutPath=C:\Users\%USERNAME%\downloads\Cheese Scripting +.lnk"
echo Set Variable "shortcutPath" to "%shortcutPath%"
set "iconPath=C:\Users\%USERNAME%\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\CSPICON.ico"
echo Set Variable "iconPath" to "%iconPath%"

echo Creating Shortcut Desktop

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut("%shortcutPath%") >> "%temp%\CreateShortcut.vbs"
echo Created Shortcut %shortcutPath%
echo oLink.TargetPath = "%targetBatchPath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "%iconPath%, 0" >> "%temp%\CreateShortcut.vbs"
echo Used Icon %iconPath%
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

cscript //nologo "%temp%\CreateShortcut.vbs"

echo Clearing Temp Files

del "%temp%\CreateShortcut.vbs"



echo Installation Complete,
echo Opening %log_file%
start notepad "%log_file%"
exit