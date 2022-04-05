# Mesh2SDF

Converts an input mesh to a signed distance field. It can work with arbitrary
meshes, even **non-watertight** meshes from ShapeNet.


## Installation

- Install via the following command:
    ``` shell
    pip install mesh2sdf
    ```

- Alternatively, install from source via the following commands.
    ``` shell
    git clone https://github.com/wang-ps/mesh2sdf.git
    pip install ./mesh2sdf
    ```

## Example

After installing `mesh2sdf`, run the following command to process an input mesh
from ShapeNet: 

```shell
python example/test.py
```

![Example of a mesh from ShapeNet](https://raw.githubusercontent.com/wang-ps/mesh2sdf/master/example/data/result.png)


<!-- ## How does it work? -->

