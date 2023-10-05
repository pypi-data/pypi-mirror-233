# **PyAxisVM** - The official python package for **AxisVM**

![alt text](https://github.com/AxisVM/DynamoToAxisVM/blob/master/Documentation/images/AxisVM%20logo.bmp)

<table>
    <tr>
        <td>Latest Release</td>
        <td>
            <a href="https://pypi.org/project/axisvm/"/>
            <img src="https://badge.fury.io/py/axisvm.svg"/>
        </td>
    </tr>
    <tr>
        <td>License</td>
        <td>
            <a href="https://opensource.org/licenses/MIT"/>
            <img src="https://img.shields.io/badge/License-MIT-yellow.svg"/>
        </td>
    </tr>
</table>

## Overview

The **PyAxisVM** project offers a high-level interface to **AxisVM**, making its operations available directly from Python. It builds on top of Microsoft's COM technology and supports all the features of the original **AxisVM** COM type library, making you able to
  
* build, manipulate and analyse **AxisVM** models

* find better solutions with iterative methods

* combine the power of **AxisVM** with third-party Python libraries

* build extension modules

On top of that, **PyAxisVM** enhances the type library with Python's slicing mechanism, context management and more, that enables writing clean, concise, and readable code.

## Installation

This is optional, but we suggest you to create a dedicated virtual enviroment at all times to avoid conflicts with your other projects. Create a folder, open a command shell in that folder and use the following command

```console
>>> python -m venv venv_name
```

Once the enviroment is created, activate it via typing

```console
>>> .\venv_name\Scripts\activate
```

The **AxisVM** python package can be installed (either in a virtual enviroment or globally) from PyPI using `pip` on Python >= 3.7 <= 3.10:

```console
>>> pip install axisvm
```

or chechkout with the following command over HTTPS via <https://github.com/AxisVM/pyaxisvm.git> or by using the GitHub CLI

```console
gh repo clone AxisVM/pyaxisvm
```

and install from source by typing

```console
>>> pip install .
```

If you want to run the tests, you can install the package along with the necessary optional dependencies like this

```console
>>> pip install ".[test]"
```

### Development mode

If you are a developer and want to install the library in development mode, the suggested way is by using this command:

```console
>>> pip install "-e .[test, dev]"
```

If you plan to touch the docs, you can install the requirements for that as well:

```console
>>> pip install "-e .[test, dev, docs]"
```

## **Documentation and Issues**

The ***AxisVM API Reference Guide*** is available in pdf format,  you can download it [***here***](https://axisvm.eu/axisvm-downloads/#application).

The documentation of this library is available [***here***](https://axisvm.github.io/pyaxisvm-docs/).

Please feel free to post issues and other questions at **PyAxisVM** Issues. This is the best place to post questions and code related to issues with this project.

## Dependencies

You will need a local licenced copy of **AxisVM** version >= 13r2. To get a copy of **AxisVM**, please visit our [***homepage***](https://axisvm.eu/).

## Getting Started

### Register the AxisVM Type Library

If this is not your first time using **AxisVM** through a COM interface on your machine, you should already have a registered type library and you can skip this step. Otherwise, follow the instructions at the beginning of the ***AxisVM API Reference Guide***.

### Launch AxisVM

The `axisvm.com.client` submodule implements various tools to handle the client side operations of creating a COM connection. Import the module and start a new application instance with the `start_AxisVM` method:

```python
from axisvm.com.client import start_AxisVM
axapp = start_AxisVM(visible=True)
```

To test the connection, you can query the path of the executable being run by typing `axapp.FullExePath`.

### Basic Usage

If the connection is complete, create a new model and get an interface to it:

```python
modelId = axapp.Models.New()
axmodel = axapp.Models.Item[modelId]
```

Every time you create a new **AxisVM** instance with the `start_AxisVM` command, an attempt is made to import the type library as a python module, or to generate one if necessary. The generated module is then accessible as `axisvm.com.tlb`.

The next block of commands adds a line to the scene:

```python
from axisvm.com.tlb import lgtStraightLine, RLineGeomData
n1 = axmodel.Nodes.Add(0, 0, 0)
n2 = axmodel.Nodes.Add(1, 1, 1)
l1 = axmodel.Lines.Add(n1, n2, lgtStraightLine, RLineGeomData())
```

Put **AxisVM** on top and scale model to fill up the current view:

```python
axapp.BringToFront()
axmodel.FitInView()
```

At the end of your session, release the connection and close the application simply by typing

```python
axapp.UnLoadCOMClients()
axapp.Quit()
```

Take a look at the jupyter notebooks in the [***examples***](https://github.com/AxisVM/pyaxisvm/tree/main/examples) folder of this repository for more use cases.

## Tips and Tricks

**PyAxisVM** wraps up the COM type library, allowing users to exploit the elegant and concise syntax that Python provides, while still leaving everything on the table for legacy code. If for example, we wanted to calculate areas of surface elements, the out of box solution would be something like

```python
areas = []
for i in range(axmodel.Surfaces.Count):
    areas.append(axmodel.Surfaces.Item[i+1].Area)
```

or using a list comprehension

```python
areas = [axmodel.Surfaces.Item[i+1].Area for i in range(axmodel.Surfaces.Count)]
```

With **PyAxisVM**, evaluation of single item properties over collections is as easy as

```python
areas = [s.Area for s in axmodel.Surfaces]
```

or simply

```python
areas = axmodel.Surfaces[:].Area
```

Click [***here***](https://github.com/AxisVM/pyaxisvm/blob/6abfebdfd26a76721836e1b490465d1f5a474a83/tips_and_tricks.md) to get a full overview about the pythonic usage of the library.

## License

**PyAxisVM** is licensed under the [MIT license](https://opensource.org/license/mit/).

This module, **PyAxisVM** makes no commercial claim over AxisVM whatsoever. This tool extends the functionality of **AxisVM** by adding a Python interface to the **AxisVM** COM service without changing the core behavior or license of the original software. The use of **PyAxisVM** requires a legally licensed local copy of **AxisVM**.
