import requests
import hashlib
import sys

# Step 1: Prompt the user to enter a password
password = input("Hey there! Please enter a password that includes both uppercase and lowercase letters, numbers, and at least one special character (like 'Abc123!'):- ")

# Step 2: Validate the password criteria
has_lower = any(char.islower() for char in password)  # Check for lowercase letters
has_upper = any(char.isupper() for char in password)  # Check for uppercase letters
has_digits = any(char.isdigit() for char in password)  # Check for digits
has_special_characters = any(not char.isalnum() for char in password)  # Check for special characters

# Step 3: Provide feedback based on password validity
if has_lower and has_upper and has_digits and has_special_characters:
    print("Great job! You entered a valid password:", password)
else:
    print("Oops! It looks like your password is missing something. Please make sure to include lowercase letters, uppercase letters, numbers, and at least one special character. Try again!")

# Step 4: Function to request API data
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char  # Create the URL for the API request
    res = requests.get(url)  # Send the request to the API
    if res.status_code != 200:  # Check if the request was successful
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')  # Raise an error if not
    return res  # Return the response

# Step 5: Function to get the count of password leaks
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())  # Split the response into lines
    for h, count in hashes:  # Iterate through the hashes
        if h == hash_to_check:  # Check if the hash matches
            return count  # Return the count if found
    return 0  # Return 0 if not found

# Step 6: Function to check if the password has been pwned
def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()  # Hash the password using SHA-1
    first5_char, tail = sha1_password[:5], sha1_password[5:]  # Split the hash into the first 5 characters and the rest
    response = request_api_data(first5_char)  # Request data from the API
    print(first5_char, tail)  # Print the first 5 characters and the tail for debugging
    print(response)  # Print the API response for debugging
    return get_password_leaks_count(response, tail)  # Check for leaks

# Step 7: Main function to handle the password checking process
def main(args):
    for password in args:  # Iterate through the list of passwords
        count = pwned_api_check(password)  # Check each password
        if count:  # If the password was found in the pwned database
            print(f'{password} was found {count} times... you should probably change your password!')
        else:  # If the password was not found
            print(f'{password} was NOT found. Carry on!')

    return 'done!'  # Return a done message

# Step 8: Check if the script is run directly and perform the check
pwned_api_check(password)  # Check the user's password

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))  # Run the main function with command-line arguments