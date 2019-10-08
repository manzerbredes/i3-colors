import yaml,re, sys,random

def configure(theme):
    """
    Apply user define colors and apply some correction factors.
    """
    if "colors" in theme:
        colors=theme["colors"]
        window_colors=theme["window_colors"]

        ##### Apply colors to window #####
        for key1,value1 in window_colors.items():
            for key2,value2 in value1.items():
                if re.match("#.*",value2) == None:
                    window_colors[key1][key2]=colors[value2]
        theme["window_colors"]=window_colors
        ##################################
                
        ##### Apply color to bar #####
        bar_colors=theme["bar_colors"]
        for key1,value1 in bar_colors.items():
            if isinstance(value1,dict):
                for key2,value2 in value1.items():
                    if re.match("#.*",value2) == None:
                        bar_colors[key1][key2]=colors[value2]
            else:
                if re.match("#.*",value1) == None:
                    bar_colors[key1]=colors[value1]
        theme["bar_colors"]=bar_colors
        ##############################
        
    ##### I3-style theme do not include child_border by default #####
    window_colors=theme["window_colors"]
    for key,value in window_colors.items():
        if not("child_border" in value):
            newvalue=value
            theme["window_colors"][key]["child_border"]=newvalue["border"] # Set it to border by default
    #################################################################
    return(theme)

def validate(theme):
    """
    Abort if theme is in a wrong format.
    """
    abort=lambda msg: sys.exit("Error while loading theme: "+msg)
    inv_key=lambda key: abort("invalid key \""+key+"\"")
    for key,value in theme.items():
        if not(key in ["meta","colors","window_colors","bar_colors"]):
            inv_key(key)
        if key=="bar_colors":
            for key,value in value.items():
                if not(key in ["separator","background","statusline",
                               "focused_workspace","active_workspace","inactive_workspace","urgent_workspace"]):
                    inv_key(key)
        if key=="window_colors":
            for key,value in value.items():
                if not(key in ["focused","focused_inactive","unfocused","urgent","child_border"]):
                    inv_key(key)
                    
def load(theme_file):
    """
    Load a theme as a dict():
      - Open YAML file
      - Parse it as a dict
      - Configure the parsed dict
      - Validate the configured dict
    """
    f=open(theme_file,mode="r")
    theme=yaml.load(f,Loader=yaml.FullLoader)
    f.close()
    theme=configure(theme)
    validate(theme)
    return(theme)


class ThemeBuilder:
    def __init__(self):
        self.theme={"meta": {"description": "Generated From i3-colors"},
                        "window_colors":dict(),
                        "bar_colors":dict()}
        self.vars=list()
        self.vars_values=dict()
        
    def as_yaml(self):
        return(yaml.dump(self.theme))

    def as_dict(self):
        return(self.theme)

        
    def get(self,key):
        if key in self.vars:
            return(self.vars_values[key])
        else:
            return(key)
        
    def parse(self,line):
        if re.match("client.*",line):
            tokens=line.split()
            key=tokens[0].replace("client.","")
            tokens.pop(0)
            subkeys=["border","background","text","indicator","child_border"]
            self.theme["window_colors"][key]=dict()
            for token in tokens:
                self.theme["window_colors"][key][subkeys[0]]=self.get(token)
                subkeys.pop(0)
        elif re.match(".*background.*",line):
            self.theme["bar_colors"]["background"]=self.get(line.split()[1])
        elif re.match(".*statusline.*",line):
            self.theme["bar_colors"]["statusline"]=self.get(line.split()[1])
        elif re.match(".*separator.*",line):
            self.theme["bar_colors"]["separator"]=self.get(line.split()[1])
        elif re.match(".*_workspace.*",line):
            tokens=line.split()
            key=tokens[0]
            tokens.pop(0)
            subkeys=["border","background","text"]
            self.theme["bar_colors"][key]=dict()
            for token in tokens:
                self.theme["bar_colors"][key][subkeys[0]]=self.get(token)
                subkeys.pop(0)
        elif re.match("(\s)*set\s",line):
            lineList=line.split()
            key=lineList.pop(0)
            name=lineList.pop(0)
            value=" ".join(str(x) for x in lineList)
            self.vars.append(name)
            self.vars_values[name]=value
            
def random_theme():
    r= lambda: "#"+hex(random.randint(0,16777214))[2:]
    t=ThemeBuilder()
    t.parse("client.focused          {} {} {} {} {}".format(r(),r(),r(),r(),r()))
    t.parse("client.unfocused          {} {} {} {} {}".format(r(),r(),r(),r(),r()))
    t.parse("client.urgent          {} {} {} {} {}".format(r(),r(),r(),r(),r()))
    t.parse("background          {}".format(r()))
    t.parse("statusline          {}".format(r()))
    t.parse("separator          {}".format(r()))
    t.parse("focused_workspace          {} {} {}".format(r(),r(),r()))
    t.parse("active_workspace          {} {} {}".format(r(),r(),r()))
    t.parse("inactive_workspace          {} {} {}".format(r(),r(),r()))
    t.parse("urgent_workspace          {} {} {}".format(r(),r(),r()))
    return(t)
