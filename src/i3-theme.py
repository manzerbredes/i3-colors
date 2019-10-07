#!/usr/bin/python 
import parser, theme, os, argparse


args_parser = argparse.ArgumentParser(description='Process some integers.')
args_parser.add_argument('theme_path', metavar='theme', type=str, nargs='?',
                    help='YAML i3 theme path')
args = args_parser.parse_args()


##### Apply Theme #####
loaded_theme=theme.load(args.theme_path)
parser.apply_theme(os.environ["HOME"]+"/.config/i3/config",loaded_theme)


