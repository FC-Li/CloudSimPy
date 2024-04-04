def round_to_threshold(input_list, thresholds):
    flattened_list = [element for sublist in input_list for element in (sublist if isinstance(sublist, list) else [sublist])]
    ls = []
    for value in flattened_list:
        # Ensure the value is within the expected range
        value = max(value, 0)
        
        # Initialize the minimum distance to be greater than any possible distance in the range [0, 1]
        min_distance = float('inf')
        closest_threshold = value  # Default to the original value in case no thresholds are provided
        
        for threshold in thresholds:
            distance = abs(value - threshold)
            if distance < min_distance:
                min_distance = distance
                closest_threshold = threshold
        
        ls.append(closest_threshold)

    return ls

def min_max_normalize_list(input_list, min_value, max_value):
    flattened_list = [element for sublist in input_list for element in (sublist if isinstance(sublist, list) else [sublist])]
    normalized_values = [(x - min_value) / (max_value - min_value) for x in flattened_list]
    return normalized_values

# # Example usage:
# value = 0.35
# rounded_value = round_to_threshold(value)
# print(f"The value {value} is rounded to {rounded_value}")
