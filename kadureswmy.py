#Importing the string module to use its punctuation constant 
import string

# Loads values from a file into a dictionary.
def load_values(file_path):
    values = {}
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Separate each line into a letter and its matching value, then convert the value to an integer.
                letter, value = line.strip().split()
                values[letter] = int(value)
            except ValueError:
                # Handle lines that lack the proper format (e.g., missing value).
                pass
    return values

# Function for calculating a letter's score based on its position and context in a word.
def calculate_score(letter, position, is_first, is_last, values):
    try:
        # If the letter is the first letter in a word, it receives a score of 0.
        if is_first:
            return 0
        # If the letter is the last letter of a word (excluding 'E'), it receives a score of 20 or 5.
        elif is_last:
            return 20 if letter == 'E' else 5
        else:
            # Estimate the score based on the letter's position in the word and its value.
            position_value = 1 if position == 2 else (2 if position == 3 else 3)
            return position_value + values.get(letter, 0)
    except KeyError:
        # Handle scenarios where the letter is missing from the values
        return 0
       
    return values


# Function that generates three-letter abbreviations for each word in a name.
def generate_abbreviations(name, values):
    words = [word.strip(string.punctuation) for word in name.split()]
    abbreviations = set()

    for word in words:
        first_letter = word[0]
        for i in range(1, len(word) - 1):
            second_letter = word[i]
            for j in range(i + 1, len(word)):
                third_letter = word[j]
                # Create the abbreviation and calculate its score.
                abbreviation = f"{first_letter}{second_letter}{third_letter}"
                score = calculate_score(second_letter, i, False, j == len(word) - 1, values) + calculate_score(third_letter, j, False, True, values)
                abbreviations.add((abbreviation, score))

    return abbreviations

# Main function for carrying out the complete process
def main():
    # Ask the user for the input file name and load values from values.txt.
    input_file = input("Enter the name of the input file (with .txt extension): ")
    values_file = "values.txt"  # You may need to change this based on your file location
    values = load_values(values_file)

    # Read names from the input file
    with open(input_file, 'r') as file:
        names = [line.strip() for line in file]

    # Ask the user for their surname and specify the name of the output file.
    surname = input("Enter your surname: ")
    output_file = f"{surname.lower()}_{input_file[:-4]}_abbrevs.txt"


    # Generate abbreviations for each name, select the best abbreviation, then save the results to the output file.
    with open(output_file, 'w') as file:
        for name in names:
            abbreviations = generate_abbreviations(name.upper(), values)
            best_abbreviation, best_score = min(abbreviations, key=lambda x: x[1])
            file.write(f"{name.upper()}: {best_abbreviation} ({best_score} points)\n")

# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
