# Polus Render

Enables the embedding of content from polus-render within Jupyer notebooks.


![image](https://github.com/jcaxle/polus-render/assets/145499292/9ef28b98-3207-47d0-bdf9-207599239e3c)

## Requirements
* Python 3.9+

## Installation
pip install polus-render

## Sample usage
``` Python
from polus import render
from urllib.parse import urlparse
from pathlib import Path

# Embeds a render into Jupyter notebooks at https://render.ci.ncats.io/
render()

# Renders zarr file hosted at "https://viv-demo.storage.googleapis.com/LuCa-7color_Scan1/"
render(urlparse("https://viv-demo.storage.googleapis.com/LuCa-7color_Scan1/"))

# Renders a zarr file hosted locally at "C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"
render(Path(r"C:\Users\JeffChen\OneDrive - Axle Informatics\Documents\zarr files\pyramid.zarr"))
```

## Functions
``` Python
def render(path:ParseResult|PurePath = "", width:int=960, height:int=500, port:int=0)->None:
    """
    Displays "https://render.ci.ncats.io/" with args to specify display dimensions, port to serve
    .zarr files to Polus Render, and dataset to use.
    
    Param:
        path (ParseResult|Purepath): Acquired from urllib.parse.ParseResult or Path, renders url in render.
                            If not specified, renders default render url
        width (int): width of render to be displayed, default is 960
        height (int): height of render to be displayed, default is 500
        port (int): Port to run local zarr server on if used (default is 0 which is the 1st available port).
    Pre: port selected (if used) is not in use IF path given is Purepath
    """
```
