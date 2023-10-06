#!/usr/bin/env python3

# Copyright 2022 Louis Paternault
#
# This file is part of Chval.
#
# Chval is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chval is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with Chval.  If not, see <http://www.gnu.org/licenses/>.

import logging
import random
import sys
import time


def main():
    if len(sys.argv) == 1:
        keyword = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(5, 10))
        )
    if len(sys.argv) == 2:
        keyword = sys.argv[1]
    elif len(sys.argv) > 2:
        logging.error("This program accepts no arguments.")
        sys.exit(1)

    print(
        "SimpleIMAPSSLRetriever:{}@example.{}:993:".format(
            keyword,
            random.choice(("net", "fr", "org", "com")),
        )
    )
    time.sleep(3 * random.random())

    start = random.randint(1, 100)
    number = random.randint(0, 7)
    for i in range(1, number + 1):
        print(
            f"msg {start+i}/{start+number} ({random.randint(1000, 10000)} bytes) delivered"
        )
        sys.stdout.flush()
        time.sleep(random.random())
        if random.randint(1, 20) == 1:
            print(
                f"getmailrc-{keyword}: operation error (no address for mailbox.example.net ([Errno -2] Name or service not known))",
                file=sys.stderr,
            )
            print(
                f"{i} messages ({number * random.randint(1000, 10000)} bytes) retrieved, {start} skipped"
            )
            sys.exit(random.randint(1, 9))
    print(
        f"{number} messages ({number * random.randint(1000, 10000)} bytes) retrieved, {start} skipped"
    )


if __name__ == "__main__":
    main()
