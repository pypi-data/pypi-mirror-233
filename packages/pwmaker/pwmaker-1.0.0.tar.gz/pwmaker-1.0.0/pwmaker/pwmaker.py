import random
import string
import argparse


class Password:
    def __init__(self, password: str) -> None:
        self._password = password

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, pw: str) -> None:
        self._password = pw

    def __str__(self) -> str:
        return self._password

    def __len__(self) -> int:
        return len(self.password)


class PasswordBuilder:
    def __init__(self) -> None:
        self._length = 10
        self._numbers = (False, 0)
        self._uppercase = False
        self._special = (False, 0)

    def length(self, _length: int) -> "PasswordBuilder":
        self._length = _length
        return self

    def numbers(self, count: int = 1) -> "PasswordBuilder":
        self._numbers = (True, count)
        return self

    def uppercase(self) -> "PasswordBuilder":
        self._uppercase = True
        return self

    def special(self, count: int = 1) -> "PasswordBuilder":
        self._special = (True, count)
        return self

    def build(self) -> Password:
        char_pool = string.ascii_lowercase
        r = random.SystemRandom()

        count = 0
        if self._numbers[0] or self._special[0]:
            if self._numbers[1] + self._special[1] > self._length:
                raise ValueError(
                    "Length can't be smaller than the count of digit and special characters"
                )
            else:
                count = self._numbers[1] + self._special[1]

        if self._uppercase:
            char_pool += string.ascii_uppercase

        password: list[str] = [r.choice(char_pool) for _ in range(self._length - count)]

        if self._numbers[0]:
            password += [r.choice(string.digits) for _ in range(self._numbers[1])]

        if self._special[0]:
            password += [r.choice(string.punctuation) for _ in range(self._special[1])]

        r.shuffle(password)
        p = Password("".join(password))
        return p


def int_plus(s: str) -> int:
    try:
        val = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Expected positive integer, got: {s}")
    else:
        if val <= 0:
            raise argparse.ArgumentTypeError(
                f"Expected positive integer, but {val} was given"
            )

    return val


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a strong and random password with variable length"
    )

    parser.add_argument(
        "-l",
        "--length",
        type=int_plus,
        action="store",
        help="What will be the length of the password",
    )

    parser.add_argument(
        "-n",
        "--numbers",
        type=int_plus,
        action="store",
        help="How many digit characters will the password have",
    )

    parser.add_argument(
        "-u",
        "--uppercase",
        action="store_true",
        dest="upper",
        help="Include uppercase characters in the password",
    )

    parser.add_argument(
        "-s",
        "--special",
        type=int_plus,
        action="store",
        help="How many special characters will the password have",
    )

    args = parser.parse_args()

    builder = PasswordBuilder()
    if args.length:
        builder.length(args.length)
    if args.numbers:
        builder.numbers(args.numbers)
    if args.upper:
        builder.uppercase()
    if args.special:
        builder.special(args.special)

    try:
        print(builder.build())
    except ValueError as e:
        print(e)
        raise SystemExit(1)

    return 0


if __name__ == "__main__":
    exit(main())
