#!/usr/bin/python

import csv
import threading as t
from time import sleep
from os import remove, walk
from getpass import getpass
from Investor import Investor
from sys import argv, exit, stdout
from os.path import join, expanduser

# Usage string for error reporting
usage = "\tSee usage.txt for info on how to use this script"

def find_file(filename):
  for root, dirs, files in walk(expanduser("~")):
    if filename in files:
      return join(root, filename)
  return None

def run_bot(investor):
  # type: (Investor) -> None
  '''This is the function given to each thread of execution. Has each investor
  search for posts and sleeps if none are found.'''
  while True:
    subID = investor.find_posts()
    if subID is not None:
      investor.invest(subID)
    else:
      print "Investor {} found nothing; sleeping for 45 seconds".format(investor.name)
      sleep(45)

def process_args():
  # type: () -> int, List[Tuple(str, str, int, str, str, str)]
  '''This function processes the command line arguments and parses the given
  file to get the info for the bots. Returns the count of bots as well as the
  list of the bot info'''

  out_list = list()

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
  to_remove = find_file("nohup.out")
  if to_remove is not None:
    remove(to_remove)


def main():
  # type: () -> None
  '''Main driver for the program'''

  # Process command line args, create thread pool
  n_threads, out_list = process_args()
  logins = [None] * n_threads - 1
  threads = [None] * n_threads - 1

  try:
    # Create a thread for each bot parsed - 1
    for num in range(len(out_list) - 1):
      logins[num] = Investor(out_list[num][0], out_list[num][1], out_list[num][2], out_list[num][3], out_list[num][4], out_list[num][5])
      threads[num] = t.Thread(target=run_bot, args=([logins[num]]))
      threads[num].daemon = True

    # Start up each thread
    for thread in threads:
      thread.start()

    # In the main thread, run the last bot
    investor = Investor(out_list[-1][0], out_list[-1][1], out_list[-1][2], out_list[-1][3], out_list[-1][4], out_list[-1][5])
    run_bot(investor)
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

