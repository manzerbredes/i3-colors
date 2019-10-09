import re,tempfile,shutil,theme

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

##### Parsing Utils #####
def contains(r,line):
    """
    Return true if line contains regex r.
    """
    return(re.match(r,line)!=None)
def before_token(token, line):
    """
    Return what is before token in line.
    """
    found=re.search(".*"+token,line)
    if found:
        return(found.group(0)[:-len(token)])
    return("")
def sorted_items(d):
    return(sorted(d.items()))
def no_comment(line):
    """
    Remove comment from a line.
    """
    newline=""
    for ch in line:
        if ch=='#':
            break
        else:
            newline+=ch
    return(newline)
#########################

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
            beforeColor=before_token("colors",line).strip()
            if len(beforeColor)>0:
                tmp.write(beforeColor+"\n")
        if not(is_theme_line) and not(in_colors):
            tmp.write(line_orig)
        if contains(".*}",line) and in_colors:
            in_colors=False    
    f.close()
    tmp.close()
    return(tmp.name)


def extract_theme(config_file):
    """
    Return a ThemeBuilder object of the config_file file.
    """
    f=open(config_file,"r")
    build=theme.ThemeBuilder()
    in_colors=False
    for line_orig in f:
        line=no_comment(line_orig)
        is_theme_line=False
        for key in config_keys:
            if contains(".*"+key+"\s",line):
                is_theme_line=True
        if contains(".*colors",line):
            in_colors=True
        if contains("(\s)*set",line): # If var definition
            build.parse(line_orig)
        elif is_theme_line or in_colors:
            build.parse(line_orig) # Seems to by strange to have comment here
        if contains(".*}",line) and in_colors:
            in_colors=False    
    f.close()
    return(build)


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
            beforeBrace=before_token("}",line).strip()
            if len(beforeBrace)>0:
                tmp.write(beforeBrace+"\n")
            tmp.write("  colors {\n")
            for key,value in sorted_items(bar_theme):
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
    for key,value in sorted_items(client_theme):
        f.write("client."+key+" "+value["border"]+" "+value["background"]+" "+value["text"]+" "+value["indicator"]+" "+value["child_border"]+"\n")
    f.close()


def apply(config_file,theme,dry=False):
    tmp=extract(config_file)
    write_theme(tmp,theme)
    f=open(tmp,mode="r")
    new_config=f.read()
    f.close()
    if not(dry):
        shutil.move(tmp,config_file)
    return(new_config)

