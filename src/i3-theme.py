#!/usr/bin/python 
import parser, theme, os, argparse, subprocess


##### Utils Functions #####
def log(title, content): print("\033[92m{}\033[00m: {}" .format(title,content))
###########################


##### Parse Arguments #####
args_parser = argparse.ArgumentParser(description='I3 Window Manager Colors Themer.')
args_parser.add_argument('theme_path', type=str, nargs='?',
                    help='I3 YAML theme path.')
args_parser.add_argument('-r', '--restart' ,action='store_true', help='Restart i3 after applying theme.')
args = args_parser.parse_args()
###########################

##### Apply Theme #####
loaded_theme=theme.load(args.theme_path)
for meta_key,meta_value in loaded_theme["meta"].items():
    log(meta_key.title(),meta_value)
parser.apply_theme(os.environ["HOME"]+"/.config/i3/config",loaded_theme)
if args.restart:
    subprocess.Popen("i3-msg restart".split()) 
#######################

