#!/usr/bin/python

import re,tempfile,shutil

config_keys=["client.focused",
            "client.focused_inactive",
            "client.unfocused",
            "client.urgent",
            "separator",
            "background",
            "statusline",
            "focused_workspace",
            "active_workspace",
            "inactive_workspace",
            "urgent_workspace"]

def contains(r,line):
    return(re.match(r,line)!=None)

def no_comment(line):
    newline=""
    for ch in line:
        if ch=='#':
            break
        else:
            newline+=ch
    return(newline)
                    
def extract(config_file):
    """
     Return a temporary file path containing the current user configuration
     without any related theme/colors lines.
    """
    f=open(config_file,"r")
    tmp=tempfile.NamedTemporaryFile(mode="w",delete=False)

    in_colors=False
    for line_orig in f:
        line=no_comment(line_orig)
        is_theme_line=False
        for key in config_keys:
            if contains(".*"+key+"\s",line):
                is_theme_line=True
        if contains(".*colors",line):
            in_colors=True
            beforeColor=re.search(".*colors",line).group(0)[:-6]
            if len(beforeColor)>0:
                tmp.write(beforeColor+"\n")
        if not(is_theme_line) and not(in_colors):
            tmp.write(line_orig)
        if contains(".*}",line) and in_colors:
            in_colors=False    
    f.close()
    tmp.close()
    return(tmp.name)
            
def safe_get(theme,key):
    """
    TODO: To remove (useless now)
    """
    if key in theme:
        return(theme[key])
    return("")

def write_theme(tmp_config,theme):
    """
    Write the theme in a temporary file
    based on tmp_config file.
    """
    f=open(tmp_config,mode="r")
    tmp=tempfile.NamedTemporaryFile(mode="w",delete=False)

    ##### Apply bar theme #####
    bar_theme=theme["bar_colors"]
    in_bar=False
    for line_orig in f:
        line=no_comment(line_orig)
        if contains("(\s)*bar",line):
            in_bar=True
        if contains(".*}",line) and in_bar:
            beforeBrace=re.search(".*}",line).group(0)[:-1]
            if len(beforeBrace)>0:
                tmp.write(beforeBrace+"\n")
            tmp.write("  colors {\n")
            for key,value in bar_theme.items():
                if not(isinstance(value,dict)):
                    tmp.write("    "+key+" "+value+"\n")
                else:
                    tmp.write("    "+key+" "+value["border"]+" "+value["background"]+" "+value["text"]+"\n")
            tmp.write("  }\n}\n")
            in_bar=False
        else:
            tmp.write(line_orig)
    tmp.close()
    f.close()
    shutil.move(tmp.name,tmp_config)
    
    ##### Apply client theme #####
    client_theme=theme["window_colors"]
    f=open(tmp_config,mode="a")
    for key,value in client_theme.items():
        f.write("client."+key+" "+value["border"]+" "+value["background"]+" "+value["text"]+" "+value["indicator"]+" "+safe_get(value,"child_border")+"\n")
    f.close()


def apply(config_file,theme):
    tmp=extract(config_file)
    write_theme(tmp,theme)
    shutil.move(tmp,config_file)

