Quastat
==================

This is just a set of experiments for statistical analysis using celestial data.

Currently it will use publicly released [NASA Veroncat](https://heasarc.gsfc.nasa.gov/W3Browse/all/veroncat.html) datasets.

Updating data
-------------

To update the data you will need to download them as CSV from the [Veroncat](http://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3table.pl?tablehead=name%3Dcaixa&Action=More+Options) website using format *cleartext* and limit *0* (unlimited)

Running
-------

This is a standalone python script that will run on any system with the **python-matplotlib** package. This is inlcuded in most GNU/Linux distributions.

To generate the default graphs under **./images/** just run: `python src/parser.py`

Directory Tree is organised as follows
--------------------------------------

* under `./src/`:
	* `parser.py`: The main app. Start reading the source there.

* under `./data/`: Public Verocat data in CSV

* under `./images/`: All outputs graphs go there.

License
-------

[GPLv3](./LICENSE)
