def validate_index(i, dataframe):
    try:
        idx = int(i)
    except ValueError:
        raise ValueError("The index must be an integer. Please, try again!")
    if idx < 0 or idx >= len(dataframe):
        raise ValueError("Position not found, please, try again!")
    return idx


# Helper function to get valid user input
def get_valid_input(prompt, default_value, validate_fn):
    while True:
        user_input = input(f"{prompt} (Current: {default_value}): ")
        if not user_input:  # If the input is empty, keep the current value
            return default_value
        try:
            # Use the validation function to check the input
            return validate_fn(user_input)
        except ValueError as e:
            print(f"Invalid input. {str(e)}")