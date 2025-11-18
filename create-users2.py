#If dry run = true, the script does not run os.system commands. 
#It prints what commands wouls have run and warnings for invalid lines
#If dry run = false, the script runs normally and creates users and groups

#!/usr/bin/python3

# INET4031
# Sidra Fathi
# 11/07/25

#os:to run system commands like adduser and passwd, re:to detect comment lines using regul>
import os
import re
import sys


def main():
    # Ask whether the script should run in dry-run mode
    answer = input("Run in dry-run mode? (Y/N): ").strip().lower()
    dry_run = (answer == "y")

    with open("create-users.input") as f:
        for line in f:

            #This expression checks whethe the line begins with #. Lines starting with>
            match = re.match("^#", line)

            #Split the line into its fields (username,password,groups) using : as the >
            fields = line.strip().split(':')

            #Skip the line if it is a comment (starts with #) or if it does not contai>
            if match or len(fields) != 5:
                if dry_run:
                    print("[DRY RUN] Skipping line:", line)
                continue

            #Extract username, password, and build the gecos full name field for creat>
            username = fields[0]
            password = fields[1]
            gecos = "%s %s,,," % (fields[3], fields[2])

            #So the user can be added to each group individually
            groups = fields[4].split(',')

            #To inform the admin which user account is about to be created
            print("==> Creating account for %s..." % (username))
            #Build full adduser coomand with gecos info and username. CMD will contain the exa>
            cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

            print(cmd)
            if dry_run:
                print("[DRY RUN] Command not executed")
            else:
                os.system(cmd)

            #To show that the script is about to set the password for this user
            print("==> Setting the password for %s..." % (username))
            #Build a command that pipes the password twice so it can be set non-interactively.>
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

            print(cmd)
            if dry_run:
                print("[DRY RUN] Command not executed.")
            else:
                os.system(cmd)

            for group in groups:
                #Check if the group is not '-', meaning no group. If its real, it will add the>
                if group != '-':
                    print("==> Assigning %s to the %s group..." % (username, group))
                    cmd = "/usr/sbin/adduser %s %s" % (username, group)
                    print(cmd)
                    if dry_run:
                        print("[DRY RUN] Command not executed.")
                    else:
                        os.system(cmd)


if __name__ == '__main__':
    main()
