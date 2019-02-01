# eight-two-seven
analysis work of SB 827 and SB 50

## inventory of current notebooks/scripts
1. _Headway Analysis v3.ipynb_ -- most current version of the script that reads an agency's GTFS and generates stop-by-stop average headways for the time periods described in SB 50
2. _Los Angeles Spatial Analysis.ipynb_ -- uses GeoPandas to compare upzoning footprints generated in _Headway Analysis v3_ to those created by other analysts, like [Transit Rich Housing](https://transitrichhousing.org).
3. _download-gtfs.py_ -- Python script for downloading the most recent versions of GTFS files for all available transit agencies in California.


## to-do
- <s>fix interpolator</s>
- <s>deal with many-schedule agencies (e.g. AC Transit) (pick arbitrary dates, use all service_ids active on those dates)</s>
- <s>filter by route_type (mode)</s>
- <s>run all agencies in one command</s>
- comment code
- evaluate/validate results
