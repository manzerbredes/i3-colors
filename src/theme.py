import yaml,re


def configure(theme):
    if "colors" in theme:
        colors=theme["colors"]
        window_colors=theme["window_colors"]
        for key1,value1 in window_colors.items():
            for key2,value2 in value1.items():
                if re.match("#.*",value2) == None:
                    window_colors[key1][key2]=colors[value2]
        theme["window_colors"]=window_colors
        
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
    return(theme)

def load(theme_file):
    f=open(theme_file,mode="r")
    theme=yaml.load(f,Loader=yaml.FullLoader)
    f.close()
    return(configure(theme))
