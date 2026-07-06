def add(num1: float, num2: float) -> float:
    """Return the sum of two numbers."""
    return num1 + num2


def subtract(num1: float, num2: float) -> float:
    """Return the difference between two numbers."""
    return num1 - num2


def multiply(num1: float, num2: float) -> float:
    """Return the product of two numbers."""
    return num1 * num2


def divide(num1: float, num2: float) -> float:
    """
    Return the quotient of two numbers.
    Raises ZeroDivisionError if num2 is zero.
    """
    if num2 == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return num1 / num2


def main() -> None:
    """Run the calculator program."""
    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("*", multiply),
        "4": ("/", divide),
    }

    while True:
        print("\nPython CLI Calculator")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")

        choice = input("Enter choice (1/2/3/4/5): ")

        if choice == "5":
            print("Thank you for using Python CLI Calculator!")
            break

        if choice not in operations:
            print("Invalid choice")
            continue

        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        symbol, operation = operations[choice]

        try:
            result = operation(num1, num2)
            print(f"{num1} {symbol} {num2} = {result}")
        except ZeroDivisionError as error:
            print(error)


if __name__ == "__main__":
    main()
