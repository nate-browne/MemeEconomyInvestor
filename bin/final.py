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
usage = "\tSee usage.txt for info on how to use this script"

def run_bot(investor):
  # type: (Investor) -> None
  '''This is the function given to each thread of execution. Has each investor
  search for posts and sleeps if none are found.'''
  while True:
    subID = investor.find_posts()
    if subID is not None:
      investor.invest(subID)
    else:
      print "Investor {} found nothing; sleeping for 1 min".format(investor.name)
      sleep(60)

def process_args():
  # type: () -> int, Tuple(str, str, int, str, str, str)
  '''This function processes the command line arguments and parses the given
  file to get the info for the bots. Returns the count of bots as well as the
  list of the bot info'''

  out_list = []

  if argv[1] == '-f':

    # Get the filename argument
    filename = argv[2]
    if '.tsv' not in argv[2]:
      filename += '.tsv'

    try:
      with open(filename, 'r') as bots:
        print 'Parsing file...'
        reader = csv.reader(bots, delimiter='\t')
        next(reader)
        count = 0
        for row in reader:
          out_list.append((row[0], row[1], int(row[2]), row[3], row[4], row[5]))
          count += 1
      print 'File processed.'
      return count, out_list
    except IOError:
      print "File does not exist. Double check your file name"
      exit(1)

  else:
    print "\n\tinvalid argument: {}".format(argv[1])
    print usage
    exit(1)

def cleanup():
  # type: () -> None
  '''"Cleans up" by removing the nohup output file'''
  if exists("../nohup.out"):
    remove("../nohup.out")

def main():
  # type: () -> None
  '''Main driver for the program'''

  # Process command line args, create pools
  n_threads, out_list = process_args()
  logins = [None] * n_threads
  threads = [None] * n_threads

  try:
    # Create a thread for each bot parsed
    for num in range(len(out_list)):
      logins[num] = Investor(out_list[num][0], out_list[num][1], out_list[num][2], out_list[num][3], out_list[num][4], out_list[num][5])
      threads[num] = t.Thread(target=run_bot, args=([logins[num]]))
      threads[num].daemon = True

    # Start up each thread
    for thread in threads:
      thread.start()

    # Keep the main thread alive
    while True:
      sleep(1)
  except(EOFError, KeyboardInterrupt):
    cleanup()
    print "\nExiting..."
    exit(0)

# Standard boilerplate
if __name__ == "__main__":

  # Error check number of arguments
  if len(argv) != 3:
    print "\n\tERROR: Script called with wrong number of arguments"
    print usage
    exit(1)

  main()

