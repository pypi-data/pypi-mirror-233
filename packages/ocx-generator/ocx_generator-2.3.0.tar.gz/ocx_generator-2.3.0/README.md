# ocx-generator
CLI python script for managing OCX schema databinding and versioning according to PEP 440.
See the documentation of [xsdata](https://xsdata.readthedocs.io/en/latest/) for details on the python databindings.

## Installation

    pip install ocx_generator
## Changes
[CHANGELOG](CHANGELOG.md)

## Usage
    python -m ocx_generator --help
    Usage: python -m ocx_generator [OPTIONS] COMMAND [ARGS]...

    Options:
      --install-completion  Install completion for the current shell.
      --show-completion     Show completion for the current shell, to copy it or
                            customize the installation.
      --help                Show this message and exit.

    Commands:
      generate  Generate code from xml schemas, webservice definitions and...
      version   Print the version number and exit.

    python -m ocx_generator generate --help
    Usage: python -m ocx_generator generate [OPTIONS] SOURCE PACKAGE VERSION

      Generate code from xml schemas, webservice definitions and any xml or json
      document. The input source can be either a filepath, uri or a directory
      containing  xml, json, xsd and wsdl files

    Arguments:
      SOURCE   [required]
      PACKAGE  [required]
      VERSION  [required]

    Options:
      --config TEXT                 [default: xsdata.xml]
      --stdout / --no-stdout        [default: no-stdout]
      --recursive / --no-recursive  [default: no-recursive]
      --help                        Show this message and exit.

## Example
Generate the databindings from the unitsML schema url:

    python -m ocx_generator generate https://3docx.org/fileadmin/ocx_schema/unitsml/unitsmlSchema_lite-0.9.18.xsd unitsml 0.9.18

    2023-09-04 11:17:28.705 | INFO     | ocx_generator.generator:generate:64 - New databinding package name is unitsml_0918 with version: 0.9.18 is created in C:\PythonDev\ocx-generator\unitsml
    ========= xsdata v23.8 / Python 3.11.5 / Platform win32 =========

    Parsing schema https://3docx.org/fileadmin/ocx_schema/unitsml/unitsmlSchema_lite-0.9.18.xsd
    Parsing schema file:///C:/miniconda3/envs/generator/Lib/site-packages/xsdata/schemas/xml.xsd
    Compiling schema file:///C:/miniconda3/envs/generator/Lib/site-packages/xsdata/schemas/xml.xsd
    Builder: 5 main and 2 inner classes
    Compiling schema https://3docx.org/fileadmin/ocx_schema/unitsml/unitsmlSchema_lite-0.9.18.xsd
    Builder: 38 main and 2 inner classes
    Analyzer input: 43 main and 4 inner classes
    Analyzer output: 35 main and 0 inner classes
    Generating package: init
    Generating package: unitsml_0918

This has now generated a subdirectory ``unitsml``  with the following structure


    C:.
    └───unitsml
        └───unitsml_0918
and with the content:

       Length Name
       ------ ----
        29577 unitsml_0918.py
         2145 xsdata.xml
         1531 __init__.py

## API documentation

[API](https://ocxstandard.github.io/ocx-generator/)
