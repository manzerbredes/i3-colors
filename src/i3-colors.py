#!/usr/bin/python 
import config, theme, os, argparse, subprocess,sys

##### Utils Functions #####
def log(msg,title=""):
    if len(title)>0:
        print("\033[92m{}\033[00m: {}" .format(title,msg))
    else:
        print(msg)
###########################

##### Apply Theme #####
def apply(args):
    loaded_theme=theme.load(args.theme_path)
    config_file=os.environ["HOME"]+"/.config/i3/config"
    if args.config_path:
        config_file=args.config_path
    config.apply(config_file,loaded_theme)
    for meta_key,meta_value in loaded_theme["meta"].items():
        log(meta_value,title=meta_key.title())
        if args.restart:
            subprocess.Popen("i3-msg restart".split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
#######################
def aleatory(args):
    t=theme.random_theme().as_dict()
    config.apply(os.environ["HOME"]+"/.config/i3/config",t)
    if args.restart:
        subprocess.Popen("i3-msg restart".split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
##### Extract Theme #####
def extract(args):
    t=config.extract_theme(args.config_path)
    print(t.as_yaml())
#######################

##### Parse Arguments #####
argsMainParser = argparse.ArgumentParser(description='I3 Window Manager Colors Themer.')
argsSubParsers = argsMainParser.add_subparsers()
argsApplyParser = argsSubParsers.add_parser("apply")
argsApplyParser.add_argument('theme_path', type=str, nargs='?',
                    help='I3 YAML theme path.')
argsApplyParser.add_argument('-r', '--restart' ,action='store_true', help='Restart i3 after applying theme.')
argsApplyParser.add_argument('config_path', type=str, nargs='?',
                    help='I3 configuration file.')
argsApplyParser.set_defaults(func=apply)

argsExtractParser = argsSubParsers.add_parser("extract")
argsExtractParser.add_argument('config_path', type=str, nargs='?',
                    help='Extract theme from config file.')
argsExtractParser.set_defaults(func=extract)

argsAleatoryParser = argsSubParsers.add_parser("aleatory")
argsAleatoryParser.add_argument('-r', '--restart' ,action='store_true', help='Restart i3 after applying theme.')
argsAleatoryParser.set_defaults(func=aleatory)


if __name__ == "__main__":
    args = argsMainParser.parse_args()
    if len(sys.argv)>1:
        args.func(args)
    else:
        argsMainParser.print_help()
###########################
