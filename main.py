def save_dictionary_to_file(dictionary, filename):
    """
    Saves a dictionary to a .txt file in key-value pairs format
    
    Args:
        dictionary: The dictionary to save
        filename: The output filename (e.g., 'data.txt')
    """
    try:
        with open(filename, 'w') as file:
            for key, value in dictionary.items():
                file.write(f"{key}={value}\n")
        print(f"Dictionary saved to {filename}")
    except Exception as e:
        print(f"Error saving dictionary: {e}")