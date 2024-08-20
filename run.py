#!/usr/bin/env python3

import subprocess
import argparse
import sys

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--distance_def", type=str)
ap.add_argument("--ratio", type=str)
ap.add_argument("--sequence", type=str)
ap.add_argument("--centered", type=str)
args = ap.parse_args()

#string to bool
centered = args.centered.lower() == 'true'

commandargs = ['LUTBasedNSDistanceTransform']

try:
    args.ratio    = ''.join([c for c in args.ratio if c in "/0123456789"])
    args.sequence = ''.join([c for c in args.sequence if c in "12 ,"])
except Exception as e:
    with open('demo_failure.txt', 'w') as file:
        file.write("badparams, Unable to handle form inputs.")
        sys.exit(0)

if centered:
    commandargs += ['-c']

if args.distance_def == 'd4':
    commandargs += ['-4']
elif args.distance_def == 'd8':
    commandargs += ['-8']
elif args.distance_def == 'ratio':
    commandargs += ['-r', str(args.ratio)]
elif args.distance_def == 'sequence':
    commandargs += ['-s', str(args.sequence)]

commandargs += ['-f', 'input_0.png']
commandargs += ['-t', 'png']

commands = ""
def runCommand(command, stdOut=None, stdErr=None, comp=None):
    """
    Run command and update the attribute list_commands
    """
    global commands
    p = subprocess.run(command, stderr=stdErr, stdout=stdOut)
    if p.returncode != 0:
        with open('demo_failure.txt', 'w') as file:
            file.write("ValueError")
            sys.exit(0)

    index = 0
    # transform convert.sh in it classic prog command (equivalent)
    for arg in command:
        if arg == "convert.sh" :
            command[index] = "convert"
        index = index + 1
    command_to_save = ' '.join(['"' + arg + '"' if ' ' in arg else arg
                for arg in command ])
    if comp is not None:
        command_to_save += comp
    commands +=  command_to_save + '\n'
    return command_to_save


with open("resu_r.png", "w") as file:
    runCommand(commandargs, stdOut=file, stdErr=subprocess.PIPE, comp='> resu_r.png')

commandargs = ['convert.sh', '-normalize', 'resu_r.png', 'resu_n.jpg']

runCommand(commandargs, stdErr=subprocess.PIPE)

with open("commands.txt", "w") as f:
    f.write(commands)