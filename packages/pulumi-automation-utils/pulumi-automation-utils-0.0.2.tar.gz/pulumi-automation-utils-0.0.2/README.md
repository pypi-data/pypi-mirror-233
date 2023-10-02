# pulumi-automation-utils
Collection of utilities useful for deploying 


## Building and Publishing 

To build the package, navigate to this directory and issue the following command:
`python3 -m build`

Once the build is completed, two files should be present in the [dist](./dist/) directory. The tar.gz file is a source distribution whereas the .whl file is a built distribution. Newer pip versions preferentially install built distributions, but will fall back to source distributions if needed. You should always upload a source distribution and provide built distributions for the platforms your project is compatible with. In this case, our example package is compatible with Python on any platform so only one built distribution is needed.

