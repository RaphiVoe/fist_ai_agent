import sys

if len(sys.argv) > 1:
    expression = sys.argv[1]
    try:
        result = eval(expression)
        print(result)
    except Exception as e:
        print(f"Error: Invalid expression: {e}")
else:
    print("Error: No expression provided")