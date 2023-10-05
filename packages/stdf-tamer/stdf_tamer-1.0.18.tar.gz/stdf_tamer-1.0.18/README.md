## stdf tamer
This package was originally developed at DC Jona / ams-OSRAM.

It is a general purpose stdf file parser / generator / simulator / analyser and converter.

But mainly it is used for these use cases.:

 - write STDF files from robotframework test cases
 - analyse STDF file content
 - convert STDF files to other file formats

Source.:
https://gittf.ams-osram.info/labor-rapperswil-jona/ams-tamer

Documentation.:
https://labor-rapperswil-jona.git-pages.ams-osram.info/ams-tamer/index.html


# Tips and tricks

## Speed

In order to speed up conversion of STDF files to other file formats use 2 stdf-tamer installations.

parse the stdf file using stdf-tamer on pypy, and create a pickle file (polars is not suported on pypy)
convert the pickle into the desired file format using stdf-tamer and CPython

