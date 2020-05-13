# README

### MarkLogic Kernel for Jupyter

This an experimental kernel using the MarkLogic database as the backend.
It uses REST calls to evaluate code, install extensions and upload code modules. 
YMMV

### How do I get set up? ###

* Make sure you have a running MarkLogic server! 
* Copy the code to a folder
* Use pip to install the code with pip install -e . 
* Drop down into /src. Install the kernelspec with jupyter kernelspec install marklogic
* Check it's installed with jupyter kernelspec list
* Start Jupyter with jupyter notebook
* Create a notebook. Switch kernel to marklogic. Write some xquery and enjoy.

### What can I do ###

* Run code in xquery or javascript (experimental)
* Install a REST extension
* Install a code module

### Endpoint setup ###

The kernel talks to MarkLogic through a REST enpoint. This is setup using a magic like so:

%endpoint CODETYPE://USER:PASSWORD@HOST:PORT

Defaults are :
* CODETYPE xquery
* USER admin
* PASSWORD admin
* HOST localhost
* PORT 8000

The endpoint call is persisted in subsequent cells until it's altered.

### Install a REST extension ###
Use the %install magic with the name of the extension follwed by the code in the usal way
%install test Installs an extension called test

### Install a Module ###
Use the %module magic with the path of the module follwed by the code in the usal way
%module test.xqy installs a module /ext/test.xqy in the Modules db for the database.


