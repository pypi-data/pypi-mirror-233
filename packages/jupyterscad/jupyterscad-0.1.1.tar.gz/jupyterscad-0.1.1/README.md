# Jupyter SCAD: SCAD in Jupyter

Jupyter SCAD renders and interactively visualizes 3D objects described in [SolidPython2](https://github.com/jeff-dh/SolidPython) within a Jupyter notebook.

This program is focused on the use case of generating stl files with Python interactively within a Jupyter notebook.

SolidPython2 generates [OpenSCAD language](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual#The_OpenSCAD_Language_Reference) code from Python code. Jupyter SCAD then uses [OpenSCAD](https://openscad.org) to render the OpenSCAD code to a 3D model and provides interactive visualization. As an alternative to SolidPython2, the OpenSCAD code can also be provided directly.

## Installation

To simply install the package, use pip:

```
pip install jupyterscad
```

Alternatively, use [container-jupyterscad](https://github.com/jreiberkyle/container-jupyterscad) to run Jupyter SCAD and a pinned version
of SolidPython2 in Jupyter lab in a [podman](https://podman.io/) container.

## Usage

### Define an OpenSCAD object

An OpenSCAD object can be defined using SolidPython2 or OpenSCAD.

#### SolidPython2
```python
from solid2 import *
obj = cube([1.5,2,1],center=True)
```

#### OpenSCAD
```python
obj = 'cube([1.5,2,1],center=true);'
```

Note: If a 3D object description integrates an external stl file, then the stl must be in the same directory as the notebook running the code.

See the [OpenSCAD language](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual#The_OpenSCAD_Language_Reference) and [SolidPython2](https://github.com/jeff-dh/SolidPython) pages for more information on how to use these tools.

### Render an OpenSCAD object

```python
from jupyter_scad import render

render(obj)
```
where `obj` is described in OpenSCAD as described above.

![render example](https://github.com/jreiberkyle/jupyterscad/blob/main/images/render_cube.png?raw=True)

The stl generated in rendering can also be saved by defining 'outfile':
```python
from jupyter_scad import render

render(obj, outfile='obj.stl')
```

### Visualize and then Render a stl

```python
from jupyter_scad import visualize_stl, render_stl

render_stl(obj, 'obj.stl')
visualize_stl('obj.stl')
```

These separate steps allow for generating an stl from an OpenSCAD object without
visualization or visualizing an existing stl.

## Alternatives

As an alternative to Jupyter SCAD, one could use a Jupyter notebook as an external editor, using SolidPython2 to update the SCAD file and OpenSCAD to visualize and render the SCAD file.
The benefit to this approach is that one can visualize the preview. The drawback is that the two-program workflow can feel distracting.
See more on using external editors for OpenSCAD [here](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_an_external_Editor_with_OpenSCAD).

Or, one can use [ViewSCAD](https://github.com/nickc92/ViewSCAD), which was the motivation for this project. However the last time ViewSCAD was updated was 2019 (checked on 9/21/2023). It only supports SolidPython, not SolidPython2.

## Transitioning from ViewSCAD

This package was inspired by [ViewSCAD](https://github.com/nickc92/ViewSCAD) and therefore
maintains a very similar interface.

To transition from ViewSCAD, replace
```python
import viewscad

r = viewscad.Renderer()
r.render(obj)
```

with
```python
import jupyterscad

jupyterscad.render(obj)
```

## Visualization Backend

This package uses [pythreejs](https://pythreejs.readthedocs.io/) for visualization.

Alternatives considered, ordered from closest fit to farthest:
- [pyvolume](https://pyvolume.readthedocs.io/): provides mesh visualization and interaction but (as of 2023.09.24) the latest release is alpha and documentation is sparse.
- [matplotlib mplot3d](https://matplotlib.org/2.2.2/mpl_toolkits/mplot3d/faq.html#toolkit-mplot3d-faq): provides mesh visualization and interaction but is slow.
- [pyvista](https://pyvista.org/): provides stl loading and visualization but visualization does not work in docker image.

## Acknowledgements

Thanks to [nickc92](https://github.com/nickc92) for creating [ViewSCAD](https://github.com/nickc92/ViewSCAD), which is the inspiration for this project.
