@echo off
REM Batch Template

echo Welcome to the Batch Template!

:: Enable delayed expansion
setlocal EnableDelayedExpansion

:: Example of a simple function
set /a sum=5+3
echo 5 + 3 = %sum%

:: Error handling example
set /p value="Enter a number to divide 10: "
if "%value%"=="" (
    echo You must enter a number.
) else (
    if "%value%"=="0" (
        echo Cannot divide by zero!
    ) else (
        set /a intResult=10/%value%
        set /a remainder=10%%%value%
        
        if !remainder! neq 0 (
            set /a decimal=100*!remainder!/%value%
            echo 10 / %value% = !intResult!.!decimal!
        ) else (
            echo 10 / %value% = !intResult!
        )
    )
)

pause
