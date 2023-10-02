# Usage

How you use `tcx2gpx` is entirely upto you. You can import it into an interactive Python session and convert a single
file or you can use the command line version that is bundled and works with a configuration file if provided or command
line options
## Single file conversion

For convenience the `convert()` method runs all steps...

```python
from tcx2gpx.tcx2gpx import TCX2GPX

gps_object = TCX2GPX(tcx_path='file_to_convert.tcx')
gps_object.convert()
```

If you want to run the steps manually...

```python
gps_object.read_tcx()
gps_object.extract_track_points()
gps_object.create_gpx()
gps_object.write_gpx()
```

If you wish to access individual features then these are simply the `@properties` or methods of
[`tcxparser`](https://github.com/vkurup/python-tcxparser/), for example...

```python
gps_object.tcx.activity_type
'running'
```

### Batch conversion

The easiest way to use `tcx2gpx` is the command line version included. It will by default search the current directory
path for files with the `.tcx` extension and convert them to `.gpx`. There are various options available that change
where output is written or the directory that is searched. For details on usage see...

``` bash
tcx2gpx --help
```

For example to use 8 cores and search the directory `~/tmp/` you would...

``` bash
tcx2gpx -d ~/tmp/ -j 8
```
