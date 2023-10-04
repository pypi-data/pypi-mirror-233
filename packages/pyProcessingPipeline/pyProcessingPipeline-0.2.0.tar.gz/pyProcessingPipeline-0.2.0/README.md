# pyProcessingPipeline

The pyProcessingPipeline is a package for creating persistent and transparent
data processing pipelines using a MySQL database as a persistent layer.

It stores every intermediate result, allowing everyone with access to the
processing database to recreate your ProcessingRuns and validate your results.

copyright (c) 2021-2023 THM Giessen (LSE, workgroup Prof. Stefan Bernhard)

Authors: Christian Teichert, Alexander Mair, Matthias Haub, Urs Hackstein, Stefan Bernhard

This program is free software: you can redistribute it and/or modify it under the terms of
the GNU Affero General Public License Version 3 as published by the Free Software Foundation. 

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHATABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details. 

You should have received a copy of the GNU Affero General Public License along with this program. 

IF not, see <http://www.gnu.org/licenses/>. 

---

# Getting Started

## Installing via PyPi

Simply run
```
pip install pyProcessingPipeline
```

## Installing from source
If you want to install the most recent version (e.g. with unfished features)
you can install from source.
To install the pyProcessingPipeline from source, clone this repository via
```
git clone https://gitlab.com/agbernhard.lse.thm/agb_public/pyProcessingPipeline
```
and then simply run pip install:
```
cd pyProcessingPipeline
pip install .
```
## Creating your first pipeline

Defining your fist processing pipeline is as easy as creating a ProcessingRun and
adding as many processing steps as you want:
```python
from pyProcessingPipeline import ProcessingRun
import pyProcessingPipeline.steps as prs

# Create a ProcessingRun, which groups all steps and handles the processing
processing_run = ProcessingRun(
    name="TestProcessingRun", description="Just a test :)", persist_results=True
)

# You may now add as many steps as you might want.
# Steps are executed in the same order as added.
processing_run.add_step(
    prs.misc.Cut(global_lower_bound=10, global_upper_bound=90)
)
processing_run.add_step(
    prs.filters.butterworth.LowpassButter(
        cutoff_frequency=1.5,
        filter_order=3,
        sampling_frequency=125,
    )
)
processing_run.add_step(
    prs.preprocessing.normalization.NormalizeFundamentalFrequency()
)
...

# To execute all steps, simply call the run-function on
# the list of timeseries you want to process.
processing_run.run([sample_data])

# The results will then be available in the run results:
processing_run.results
```

For creating and storing persistent runs, see the documentation.

## Building Documentation

To build the documentation, you will need to install the optional dependencies needed for documentation.
Switch to the root folder and run:

```
$ pip install '.[docs]'
```

Now you can build the documentation by calling
```
make docs
```
## Running Tests

First, install the optional test dependencies
```
$ pip install '.[test]'
```

and run
```
make unittest
```

## Checking Code

To check if your code satisfies the style requirements, you can install the optional dev dependencies
```
$ pip install '.[dev]'
```

and call

```
make check
````

This will run black for auto-formatting of code, flake8 for checking the codestyle and mypy for static code analysis.
