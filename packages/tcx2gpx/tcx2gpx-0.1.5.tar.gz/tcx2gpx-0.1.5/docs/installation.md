# Installation

There are several methods of installing `tcx2gpx` depending and which depends on whether you wish to simply use a stable
version that (hopefully) "Just Works(tm)" out of the box, try out the latest development version or get the development
version and perhaps contribute.

| Usage          | Install Method             |
|:---------------|:---------------------------|
| Convert Files  | PyPI install using `pip`   |
| Latest Version | GitLab install using `pip` |
| Contribute     | Fork and clone repository  |

## PyPI

`tcx2gpx` is available on [PyPI](https://pypi.org/project/tcx2gpx/), the Python Package Index. To install, ideally under
a virtual environment simply use the following to get the latest stable release.

``` bash
pip install tcx2gpx
```


## Latest Version

Occasionally I do some work on `tcx2gpx` and do not release it. You can install these development branches directly from
GitLab using `pip`, replace `<branch>` with the branch you wish to clone.


``` bash
pip install git+https://gitlab.com/nshephard/tcx2gpx.git@<branch>
```


## Contributing

To contribute you should [fork the repository](https://gitlab.com/nshephard/tcx2gpx/-/forks/new) and then clone your
fork locally to work on it. Assuming you do not rename the repository when you fork it replace `<username>` in the
following with your GitLab username. Then install in editable mode.


``` bash
git clone git@gitlab.com:<username>/tcx2gpx.git
pip install -e .
```
