# Python Template
# Ctrl+R -> Python (Run)

def add(a, b):
    return a + b

def main():
    print("Welcome to the Python Template!")
    
    # Example of using a function
    result = add(5, 3)
    print(f"5 + 3 = {result}")

    # List comprehension example
    squares = [x**2 for x in range(1, 6)]
    print(f"Squares from 1 to 5: {squares}")

    # Exception handling example
    try:
        value = int(input("Enter a number to divide 10: "))
        print(f"10 / {value} = {10 / value}")
    except ZeroDivisionError:
        print("Cannot divide by zero!")
    except ValueError:
        print("Please enter a valid number.")

    # Wait for user to press Enter before closing
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
