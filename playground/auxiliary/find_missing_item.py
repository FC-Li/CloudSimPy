def find_first_missing_integer(my_list):
    my_list = sorted(set(my_list))  # Sort and remove duplicates
    missing_int = 1  # Start checking from 1
    for item in my_list:
        if item == missing_int:
            missing_int += 1
        else:
            break  # Exit early if the current item is not the expected integer
    return missing_int