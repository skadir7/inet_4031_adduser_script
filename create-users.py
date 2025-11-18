#!/usr/bin/python3

# INET4031
# Sidra Fathi
# 11/07/25

#os:to run system commands like adduser and passwd, re:to detect comment lines using regular expressions, sys:to read input line by line fron input file.
import os
import re
import sys


def main():
    for line in sys.stdin:

        #This expression checks whethe the line begins with #. Lines starting with # are treated as comments in the input file and must be skipped
        match = re.match("^#",line)

        #Split the line into its fields (username,password,groups) using : as the seperator.
        fields = line.strip().split(':')

        #Skip the line if it is a comment (starts with #) or if it does not contain exactly 5 fields
        if match or len(fields) != 5:
            continue

        #Extract username, password, and build the gecos full name field for creating the user
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        #So the user can be added to each group individually
        groups = fields[4].split(',')

        #To inform the admin which user account is about to be created
        print("==> Creating account for %s..." % (username))
        #Build full adduser coomand with gecos info and username. CMD will contain the exact shell command to create the user account
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        print(cmd)
        os.system(cmd)

        #To show that the script is about to set the password for this user
        print("==> Setting the password for %s..." % (username))
        #Build a command that pipes the password twice so it can be set non-interactively. CMD contains the shell command that updates the users password.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        print(cmd)
        os.system(cmd)

        for group in groups:
            #Check if the group is not '-', meaning no group. If its real, it will add the user to that group
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
