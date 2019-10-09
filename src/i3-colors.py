#!/usr/bin/env python 
import config, theme, os, argparse, subprocess,sys

##### Apply Theme #####
def apply(args):
    if not(args.theme_path):
        argsMainParser.print_help()
        exit(1)
    loaded_theme=theme.load(args.theme_path)
    config_file=os.environ["HOME"]+"/.config/i3/config"
    if args.config_path:
        config_file=args.config_path
    if not(args.dry):
        config.apply(config_file,loaded_theme)
        for meta_key,meta_value in loaded_theme["meta"].items():
            print("\033[92m{}\033[00m: {}" .format(meta_key.title(),meta_value))
            if args.restart:
                subprocess.Popen("i3-msg restart".split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        new_config=config.apply(config_file,loaded_theme,dry=True)
        print(new_config)
#######################

##### Aleatory #####
def aleatory(args):
    t=theme.random_theme().as_dict()
    config.apply(os.environ["HOME"]+"/.config/i3/config",t)
    if args.restart:
        subprocess.Popen("i3-msg restart".split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
####################

##### Extract Theme #####
def extract(args):
    if not(args.config_path):
        argsMainParser.print_help()
        exit(1)
    t=config.extract_theme(args.config_path)
    print(t.as_yaml())
#######################

##### Entry Point #####
if __name__ == "__main__":
    ##### Main Parser
    argsMainParser = argparse.ArgumentParser(description='I3 Window Manager Colors Themer.')
    argsSubParsers = argsMainParser.add_subparsers()
    ##### Apply Parser
    argsApplyParser = argsSubParsers.add_parser("apply")
    argsApplyParser.add_argument('theme_path', type=str, nargs='?',
                                 help='I3 YAML theme path.')
    argsApplyParser.add_argument('config_path', type=str, nargs='?',
                                 help='I3 config file path.')
    argsApplyParser.add_argument('-r', '--restart' ,action='store_true', help='Restart i3 after applying theme.')
    argsApplyParser.add_argument('-d', '--dry' ,action='store_true', help='Do not apply theme, just print config file.')
    argsApplyParser.set_defaults(func=apply)
    ##### Extract Parser
    argsExtractParser = argsSubParsers.add_parser("extract")
    argsExtractParser.add_argument('config_path', type=str, nargs='?',
                                   help='Extract theme from config file.')
    argsExtractParser.set_defaults(func=extract)
    ##### Aleatory Parser
    argsAleatoryParser = argsSubParsers.add_parser("aleatory")
    argsAleatoryParser.add_argument('-r', '--restart' ,action='store_true', help='Restart i3 after applying theme.')
    argsAleatoryParser.set_defaults(func=aleatory)
    ##### Launch i3-colors
    args = argsMainParser.parse_args()
    if len(sys.argv)>1:
        args.func(args)
    else:
        argsMainParser.print_help()
###########################
