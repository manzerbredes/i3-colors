#!/usr/bin/python

import re,tempfile,shutil

theme_keys=["client.focused",
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

def extract_config(config_file):
    f=open(config_file,"r")
    tmp=tempfile.NamedTemporaryFile(mode="w",delete=False)
    for line in f:
        is_theme_line=False
        for key in theme_keys:
            if contains(".*"+key+"\s",line):
                is_theme_line=True
        if not(is_theme_line):
            tmp.write(line)
    
    f.close()
    tmp.close()
    return(tmp.name)

def safe_get(theme,key):
    if key in theme:
        return(theme[key])
    return("")

def apply_to_config(tmp_config,theme):
    f=open(tmp_config,mode="r")
    tmp=tempfile.NamedTemporaryFile(mode="w",delete=False)

    ##### Apply bar theme #####
    bar_theme=theme["bar_colors"]
    for line in f:
        if contains(".*colors\s{",line):
            tmp.write(line)
            for key,value in bar_theme.items():
                if not(isinstance(value,dict)):
                    tmp.write("\t"+key+" "+value+"\n")
                else:
                    tmp.write("\t"+key+" "+value["border"]+" "+value["background"]+" "+value["text"]+"\n")
        else:
            tmp.write(line)
    tmp.close()
    f.close()
    shutil.move(tmp.name,tmp_config)
    
    ##### Apply client theme #####
    client_theme=theme["window_colors"]
    f=open(tmp_config,mode="a")
    for key,value in client_theme.items():
        f.write("client."+key+" "+value["border"]+" "+value["background"]+" "+value["text"]+" "+value["indicator"]+" "+safe_get(value,"child_border")+"\n")
    f.close()
    
def apply_theme(config_file,theme):
    tmp=extract_config(config_file)
    apply_to_config(tmp,theme)
    shutil.move(tmp,config_file)

theme={
    "bar":{
        "separator": "#666666",
        "background": "#333333",
        "statusline": "#bbbbbb",
        "focused_workspace": { "border":"#888888",
                               "background": "#dddddd",
                               "text": "#222222"},
        "active_workspace":  { "border": "#333333",
                               "background": "#555555",
                               "text": "#bbbbbb"},
        "inactive_workspace": { "border": "#333333",
                                "background": "#555555",
                                "text": "#bbbbbb"},
        "urgent_workspace": { "border": "#2f343a",
                              "background": "#900000",
                              "text": "#ffffff"}},
    "client": {
        "client.focused":  { "background": "#888888",
                             "text": "#dddddd",
                             "indicator": "#222222",
                             "child_border": "#2e9ef4"},
        "client.focused_inactive":  { "background": "#333333",
                                      "text": "#555555",
                                      "indicator": "#bbbbbb",
                                      "child_border": "#484e50"},
        "client.unfocused":  { "background": "#333333",
                               "text": "#333333",
                               "indicator": "#888888",
                               "child_border": "#292d2e"},
        "client.urgent":  { "background": "#2f343a",
                            "text": "#900000",
                            "indicator": "#ffffff",
                            "child_border": "#900000"}}
}

