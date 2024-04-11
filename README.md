# Building the LFRic development environment with Spack

A working Spack installation is required for this - please follow the instructions in the [Spack docs](https://spack-tutorial.readthedocs.io/en/latest/tutorial_basics.html#installing-spack).

When Spack is installed, clone this Git repository and use Spack to add the package repo:
```shell
git clone https://github.com/UniExeterRSE/lfric-env
spack repo add lfric-env/repo
```

It's recommended to check the spec of the installation to ensure that the correct dependencies are being targetted. Once these are correct, install the environment:
``` shell
spack spec lfric-env
spack install lfric-env
```

The environment can be loaded with ```spack load lfric-env```. You are now ready to build LFRic!

### Contributions
This recipe has been tested on a very small number of platforms, so any feedback about issues or bugs with different platforms are welcome. Feel contribute via issues and pull-requests as well.

