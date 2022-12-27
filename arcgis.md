## Python ArcGIS Install
You will need these Python tools:  
```
sudo apt-get install python3-venv
sudo apt install python3-pip
```

Then you will need a Virtual Environment:
```
py -m venv ~/projects/dir/.venv/arcgis
source ~/projects/dir/.venv/arcgis/bin/activate
```

Your Linux environment will need the Kerberos development package, as even though we will be using annonymous access when calling ArcGIS via the SDK, the installation requires all components needed for using Kerberos authentication.  
```
sudo apt-get install libkrb5-dev
```

If you don't have a c compiler installed then add cc and also check you have the python wheel pacakge.
```
sudo apt-get install build-essential
pip install wheel
```

Then install these ArcGIS required packages in this sequence (note, the jupyter-server will include a jupyter-client which is incompatible and must then be downgraded).  
```
pip install ujson
pip install requests_ntlm
pip install requests_toolbelt
pip install requests-gssapi
pip install requests-oauthlib
pip install requests
pip install cachetools
pip install geomet
pip install --force-reinstall jupyter-server==1.21
pip install --force-reinstall jupyter-client==6.1.12
pip install notebook
pip install ipywidgets
pip install jupyterlab
pip install keyring
pip install lerc
pip install lxml
pip install pandas
pip install matplotlib
pip install pyshp
pip install python-certifi-win32
```
Note:  On some linux environemnts requests-gssapi may fail to build gssapi (even though libkrb5-dev is intalled).  However, some environments do require this package (penguin linux) and others to not (debian).  

The reason we have just installed all these package manually is that the ArcGIS package includes a version of Pyhon, which we definitely do not want to attempt to install over the top of the existing version within our environment.  To prevent his from happening you must use the **--no-deps** flag when adding ArcGIS.
```
pip install arcgis==2.0.1 --no-deps
```
Note: this version of ArcGIS is 2.0.1 (the latest as of Dec 22), which is only compatible with Python major versions 3.7 to 3.9.  


