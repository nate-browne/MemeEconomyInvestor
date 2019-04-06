#!/usr/bin/python

import csv
import threading as t
from os import remove
from time import sleep
from os.path import exists
from getpass import getpass
from Investor import Investor
from sys import argv, exit, stdout

# Usage string for error reporting
usage = "\tUSAGE: ./final.py -f <filename of bot info> [--to-terminal/--to-file]\
OR ./final.py -n <number of bots> [--to-terminal/--to-file]"

def init_set():
  # type: () -> Set[str]
  '''This function grabs all of the invested links from the file and loads them into memory'''
  retval = set()
  with open("logs.txt", "r") as infile:
    for line in infile:
      retval.add(line.strip('\n'))
  return retval

def run_bot(investor):
  # type: (Investor) -> None
  '''This is the function given to each thread of execution. Has each investor search for posts and sleeps
  if none are found.'''
  while True:
    subID = investor.find_posts()
    if subID is not None:
      investor.invest(subID)
    else:
      print "Investor {} found nothing; sleeping for 2 mins, 10 seconds".format(investor.name)
      sleep(130)

def join_and_write(logins):
  # type: (List[Investor]) -> None
  '''This function takes the bots and writes all of their investments to a file'''
  combined = set()
  for login in logins:
    combined.update(login.replied)
  with open("logs.txt", 'w') as outfile:
    for postID in combined:
      outfile.write(postID + "\n")

def process_args(out_list):
  '''This function processes the command line arguments and performs
  error checks when necessary. Updates the `out_list` parameter as an output
  param if the user inputted a file of bots'''

  # file of bots to use
  if argv[1] == '-f':
    filename = argv[2]
    if '.tsv' not in argv[2]:
      filename += '.tsv'
    with open(filename, 'r') as bots:
      print 'Parsing file...'
      reader = csv.reader(bots, delimiter='\t')
      next(reader)
      count = 0
      for row in reader:
        out_list.append((row[0], row[1], int(row[2])))
        count += 1
    print 'File processed.'
    return count

  # User wants to manually run with a specified number of bots
  elif argv[1] == '-n':
    return int(argv[2])
  else:
    print "\n\tinvalid argument: {}".format(argv[1])
    print usage
    exit(1)

def main():
  # type: () -> None
  '''Main driver for the program'''

  # Process command line args, create pools
  out_list = list()
  n_threads = process_args(out_list)
  logins = [None] * n_threads
  threads = [None] * n_threads
  started = False

  try:
    # Parse user input for each bot
    if argv[1] == '-n':
      for num in range(n_threads):
        uname = raw_input("Enter reddit username: ")
        passwd = getpass("Enter password (not saved anywhere): ")
        opt = raw_input("Invest full amount? (y/n): ")
        amt = 100
        if opt.upper() != 'Y':
          amt = int(input("Enter an amount to invest (number without the percent sign): "))

        # Create the thread for this bot
        logins[num] = Investor(uname, passwd, amt, init_set())
        threads[num] = t.Thread(target=run_bot, args=([logins[num]]))
        threads[num].daemon = True
    else:
      # Create a thread for each bont parsed
      for num in range(len(out_list)):
        logins[num] = Investor(out_list[num][0], out_list[num][1], out_list[num][2], init_set())
        threads[num] = t.Thread(target=run_bot, args=([logins[num]]))
        threads[num].daemon = True

    # Start up each thread
    for thread in threads:
      thread.start()

    # Keep the main thread alive
    started = True
    while True:
      sleep(1)
  except(EOFError, KeyboardInterrupt):
    if started:
      join_and_write(logins)
    if exists("./nohup.out"):
      remove("./nohup.out")
    print "\nExiting..."
    exit(0)

# Standard boilerplate
if __name__ == "__main__":
  if len(argv) != 4:
    print "\n\tERROR: Script called with wrong number of arguments"
    print usage
    exit(1)

  if argv[3] == '--to-terminal':
    main()
  else:
    try:
      old_stdout = stdout
      log_file = open("output.log", 'w')
      stdout = log_file
      main()
    finally:
      stdout = old_stdout
      log_file.close()
