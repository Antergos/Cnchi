#!/bin/bash
# Reflector actually does perform speed tests when called and doesn't use speed results
# from Arch's main server like we originally thought. If you monitor your network I/O
# while running reflector command, you will see it is doing much more than
# downloading the 4kb mirrorlist file. If ran with --verbose and without --save param it
# will output the speed test results to STDOUT.

reflector -l 40 -p http -f 10 --save /etc/pacman.d/mirrorlist
