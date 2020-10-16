import requests
import hashlib
import sys
import stdiomask

# Comment out this section if you are using the command line check function.
# This will hide your password when you type it in your terminal. No prying eyes!
print('This app will check to see if your password has been pawned.\nYour full password will never be shared with the outside world.')
question = stdiomask.getpass(
    prompt='What password would you like to check? : ')


# This sends the password check query
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching:{res.status_code}, check the API and try again.')
    return res


# This function gets the count of your password pawns
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


# This hashes and splits your password in order to share it with the internet.
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


# #Uncomment and call this function if you want to input the password from the command line
# def main_command(args):
#     for password in args:
#         count = pwned_api_check(password)
#         first_lettrs = password[:5]
#         if count:
#             print(
#                 f'{first_lettrs}****** was found {count} times... Find a better password!!')
#         else:
#             print(f'{first_lettrs}****** was NOT found. Good job! Use it.')
#     return 'Done!'

# This is the function that does all the checking work and prints the information returned.
def main(password):
    count = pwned_api_check(password)
    first_lettrs = password[:5]
    if count:
        print(
            f'{first_lettrs}****** was found {count} times... Find a better password!!')
    else:
        print(f'{first_lettrs}****** was NOT found. Good job! Use it.')
    return 'Check Complete.'


# Input string call. Be sure to comment this command if using the one below.
if __name__ == "__main__":
    sys.exit(main(str(question)))

# Command line call. Uncomment and comment the code above to use.
# if __name__ == "__main__":
#   main_command(sys.argv[1:])
