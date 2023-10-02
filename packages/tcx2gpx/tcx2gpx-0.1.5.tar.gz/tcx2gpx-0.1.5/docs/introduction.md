# Introduction

This module converts the Garmin [tcx](https://en.wikipedia.org/wiki/Training_Center_XML) GPS file format
to the more commonly used [gpx](https://en.wikipedia.org/wiki/GPS_Exchange_Format) file format.
Both formats are a form of [XML](https://en.wikipedia.org/wiki/XML) but there are some fields in the former that are not
present in the later.
It uses two packages to do the grunt work [tcxparser](https://github.com/vkurup/python-tcxparser/) and
[gpxpy](https://github.com/tkrajina/gpxpy).

## Why?

My motivation for writing this package was two-fold. Firstly I wanted to convert `.tcx` files to `.gpx`, but then I also
wanted to learn more about Python packaging and GitLab's CI/CD pipelines.

### Usage

I used to use Endomondo to track my cycling and running but didn't like sharing my data. I decided to switch to the
privacy respecting [OpenTracks](https://github.com/OpenTracksApp/OpenTracks) which saves all data on your phone and
doesn't share anything with any company.

Unfortunately Endomondo only exported tracks in [tcx](https://en.wikipedia.org/wiki/Training_Center_XML), but OpenTracks
worked, at the time, with [gpx](https://en.wikipedia.org/wiki/GPS_Exchange_Format) (it may import `kml` these days I'm
not sure, it certainly exports to this format).

Thus I had to convert a thousand or so tracks from `tcx` to `gpx` if I wanted to include my legacy runs and cycles in
the application I had chosen to switch to.

### Learning

At the time I started working on `tcx2gpx` I'd only used Python for a year or so and still felt I had a lot to learn.
Packaging and releasing to [PyPI](https://pypi.org/) was one area of deficiency. I'm still learning Python, I think
I always will be, and so I often use the package as a means of learning a new aspect such as incorporating
[pydantic](https://pydantic-docs.helpmanual.io/), using
[versioneer](https://github.com/python-versioneer/python-versioneer) or building and deploying these pages automatically
using GitLab's CI/CD tools.

### Showcase

A beneficial side effect of working on OpenSource projects in public is that it gives me something to showcase when it
comes to applying for jobs. I'd like to think having this repository available helped in my most recent shift in career
to Research Software Engineer.

## Feedback

I'm always looking to improve my knowledge and understanding and that is not limited to Python programming! If however
you encounter problems using `tcx2gpx` please to file a [new
issue](https://gitlab.com/nshephard/tcx2gpx/-/issues/new). I can't guarantee I'll be able to address it immediately due
to work and other responsibilities but will acknowledge receipt and try and give a time line.
