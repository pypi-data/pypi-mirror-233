# pwmaker

Helps you generate a strong and random password with variable length through the command line interface.

## Installation

Install through pip:

```
pip install pwmaker
```

## Usage

To use the password generator use the command pwmaker in the terminal. Passwords can be customized with these options:

- -l LENGTH : The length of the password. Default is 10.
- -n NUMBERS : Digit characters where NUMBERS is the total quantity.
- -u : Include uppercase characters in the password.
- -s SPECIAL : Special characters where SPECIAL is the total quantity.

```bash
pwmaker -l 16 -u -n 4 -s 2
```

## License
pwmaker is released under the MIT license. See LICENSE for details.