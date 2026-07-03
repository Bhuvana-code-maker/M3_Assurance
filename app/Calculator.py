def add(num1: float, num2: float) -> float:
    """Return the sum of two numbers."""
    return num1 + num2
 
 
def subtract(num1: float, num2: float) -> float:
    """Return the difference between two numbers."""
    return num1 - num2
 
 
def multiply(num1: float, num2: float) -> float:
    """Return the product of two numbers."""
    return num1 * num2
 
 
def divide(num1: float, num2: float):
    """
    Return the quotient of two numbers.
    Raises ZeroDivisionError if num2 is zero, which is
    handled by the caller.
    """
    if num2 == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return num1 / num2
 
 
def get_number(prompt: str) -> float:
    """
    Prompt the user for a number and keep asking until a
    valid float is entered.
    """
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a numeric value (e.g. 10 or 3.5).\n")
 
 
def show_menu() -> None:
    """Display the calculator's main menu."""
    print("\n===== CLI Calculator =====")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
    print("===========================")
 
 
def main() -> None:
    """Main program loop that drives the calculator."""
    # Map menu choices to their corresponding operation and symbol
    operations = {
        "1": ("Add", add, "+"),
        "2": ("Subtract", subtract, "-"),
        "3": ("Multiply", multiply, "*"),
        "4": ("Divide", divide, "/"),
    }
 
    print("Welcome to the CLI Calculator!")
 
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()
 
        # Exit condition
        if choice == "5":
            print("\nThank you for using the CLI Calculator. Goodbye!\n")
            break
 
        # Handle invalid menu choices gracefully
        if choice not in operations:
            print("\nInvalid choice. Please select a number between 1 and 5.\n")
            continue
 
        name, operation, symbol = operations[choice]
 
        # Collect operands from the user
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
 
        # Perform the calculation, handling division-by-zero errors
        try:
            result = operation(num1, num2)
        except ZeroDivisionError as error:
            print(f"\nError: {error}\n")
            continue
 
        # Display a clean, formatted result
        print(f"\n{name}: {num1} {symbol} {num2}")
        print(f"Result: {result}\n")
 
 
# Standard entry point guard so the script only runs when executed directly
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCalculator interrupted by user. Goodbye!\n")
 
