# PRObs data conversion module

This module contains scripts and rules for converting data to PRObs RDF.

These scripts are compatible with [RDFox](https://www.oxfordsemantic.tech) version 6.3a.

## Running the RDFox scripts

First, overwrite the `load_data.rdfox` and the `load_rules.rdfox` files in "scripts/data-conversion" (obviously, keeping the same names) to load the data files you want to convert.

Then run:

```sh
RDFox sandbox <root> scripts/data-conversion/master
```

where `<root>` is the path to this folder.

The converted data will be written to `data/probs_original_data`.

## Using probs-runner

Using [probs-runner](https://github.com/probs-lab/probs-runner), this module can be run using the `probs_convert_data` function.
