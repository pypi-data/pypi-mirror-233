## climetlab-wekeo_mercator

A dataset plugin for climetlab for the Mercator Ocean datasets available on WEkEO.

For installation and usage instructions, please refer to [the documentation](https://climetlab-wekeo-mercator.readthedocs.io/).

Features
--------

This plugin provides a simple access to MO datasets provided by WEkEO.

Each dataset presents a number of variables to narrow down the data to download:

- a `layer` that typically specifies the provided information (eg: Sea water velocity).
  The specific name and the description of each layer can be found at the top of each Python file
- an `area` of interest defined as a bounding box
- a `start` and an `end` date
- one or more `variables`. As for the layers, available variables values can be inspected by looking at the Python files.

While it is not mandatory, the usage of Dask is recommended.

For usage examples, please refer to the [demo notebook](https://github.com/wekeo/climetlab-wekeo-mercator/tree/main/notebooks/demo_main.ipynb)

## Datasets description

There are several datasets:

- wekeo-mercator-arctic-analysis-forecast-phys
- wekeo-mercator-arctic-analysis-forecast-wav
- wekeo-mercator-arctic-analysisforecast-bgc
- wekeo-mercator-arctic-analysisforecast-phy-ice
- wekeo-mercator-arctic-analysisforecast-phy-tide
- wekeo-mercator-arctic-multiyear-bgc
- wekeo-mercator-arctic-multiyear-phy
- wekeo-mercator-arctic-multiyear-wav
- wekeo-mercator-balticsea-analysisforecast-bgc
- wekeo-mercator-balticsea-analysisforecast-phy
- wekeo-mercator-balticsea-analysisforecast-wav
- wekeo-mercator-balticsea-multiyear-bgc
- wekeo-mercator-balticsea-multiyear-phy
- wekeo-mercator-balticsea-reanalysis-wav
- wekeo-mercator-blksea-analysisforecast-bgc
- wekeo-mercator-blksea-analysisforecast-phy
- wekeo-mercator-blksea-analysisforecast-wav
- wekeo-mercator-blksea-multiyear-phy
- wekeo-mercator-blksea-multiyear-wav
- wekeo-mercator-blksea-reanalysis-bio
- wekeo-mercator-global-analysis-forecast-bio
- wekeo-mercator-global-analysisforecast-phy
- wekeo-mercator-global-analysisforecast-wav
- wekeo-mercator-global-multiyear-bgc
- wekeo-mercator-global-multiyear-phy
- wekeo-mercator-global-multiyear-wav
- wekeo-mercator-global-reanalysis-phy
- wekeo-mercator-ibi-analysis-forecast-wav
- wekeo-mercator-ibi-analysisforecast-bgc
- wekeo-mercator-ibi-analysisforecast-phy
- wekeo-mercator-ibi-multiyear-bgc
- wekeo-mercator-ibi-multiyear-phy
- wekeo-mercator-ibi-multiyear-wav
- wekeo-mercator-insitu-arc-phybgcwav-discrete-mynrt
- wekeo-mercator-insitu-bal-phybgcwav-discrete-mynrt
- wekeo-mercator-insitu-blk-phybgcwav-discrete-mynrt
- wekeo-mercator-insitu-glo-bgc-carbon-discrete-my
- wekeo-mercator-insitu-glo-bgc-discrete-my
- wekeo-mercator-insitu-glo-phy-ts-oa-my
- wekeo-mercator-insitu-glo-phy-ts-oa-nrt
- wekeo-mercator-insitu-glo-phy-uv-discrete-my
- wekeo-mercator-insitu-glo-phy-uv-discrete-nrt
- wekeo-mercator-insitu-glo-phybgcwav-discrete-mynrt
- wekeo-mercator-insitu-ibi-phybgcwav-discrete-mynrt
- wekeo-mercator-insitu-med-phybgcwav-discrete-mynrt
- wekeo-mercator-insitu-nws-phybgcwav-discrete-mynrt
- wekeo-mercator-medsea-analysisforecast-bgc
- wekeo-mercator-medsea-analysisforecast-phy
- wekeo-mercator-medsea-analysisforecast-wav
- wekeo-mercator-medsea-multiyear-bgc
- wekeo-mercator-medsea-multiyear-phy
- wekeo-mercator-medsea-multiyear-wav
- wekeo-mercator-multiobs-glo-bio-bgc-3d-rep
- wekeo-mercator-multiobs-glo-bio-carbon-surface-rep
- wekeo-mercator-multiobs-glo-phy-nrt
- wekeo-mercator-multiobs-glo-phy-rep
- wekeo-mercator-multiobs-glo-phy-s-surface-mynrt
- wekeo-mercator-multiobs-glo-phy-sss-l3-mynrt
- wekeo-mercator-multiobs-glo-phy-sss-l4-my
- wekeo-mercator-multiobs-glo-phy-tsuv-3d-mynrt
- wekeo-mercator-multiobs-glo-phy-w-3d-rep
- wekeo-mercator-northwestshelf-analysis-forecast-phy
- wekeo-mercator-northwestshelf-analysis-forecast-wav
- wekeo-mercator-nwshelf-analysisforecast-bgc
- wekeo-mercator-nwshelf-analysisforecast-phy-lr
- wekeo-mercator-nwshelf-multiyear-bgc
- wekeo-mercator-nwshelf-multiyear-phy
- wekeo-mercator-nwshelf-reanalysis-wav
- wekeo-mercator-oceancolour-arc-bgc-hr-l3-nrt
- wekeo-mercator-oceancolour-arc-bgc-hr-l4-nrt
- wekeo-mercator-oceancolour-arc-bgc-l3-my
- wekeo-mercator-oceancolour-arc-bgc-l3-nrt
- wekeo-mercator-oceancolour-arc-bgc-l4-my
- wekeo-mercator-oceancolour-arc-bgc-l4-nrt
- wekeo-mercator-oceancolour-atl-bgc-l3-my
- wekeo-mercator-oceancolour-atl-bgc-l3-nrt
- wekeo-mercator-oceancolour-atl-bgc-l4-my
- wekeo-mercator-oceancolour-atl-bgc-l4-nrt
- wekeo-mercator-oceancolour-bal-bgc-hr-l3-nrt
- wekeo-mercator-oceancolour-bal-bgc-hr-l4-nrt
- wekeo-mercator-oceancolour-bal-bgc-l3-my
- wekeo-mercator-oceancolour-bal-bgc-l3-nrt
- wekeo-mercator-oceancolour-bal-bgc-l4-my
- wekeo-mercator-oceancolour-bal-bgc-l4-nrt
- wekeo-mercator-oceancolour-blk-bgc-hr-l3-nrt
- wekeo-mercator-oceancolour-blk-bgc-hr-l4-nrt
- wekeo-mercator-oceancolour-blk-bgc-l3-my
- wekeo-mercator-oceancolour-blk-bgc-l3-nrt
- wekeo-mercator-oceancolour-blk-bgc-l4-my
- wekeo-mercator-oceancolour-blk-bgc-l4-nrt
- wekeo-mercator-oceancolour-glo-bgc-l3-my
- wekeo-mercator-oceancolour-glo-bgc-l3-nrt
- wekeo-mercator-oceancolour-glo-bgc-l4-my
- wekeo-mercator-oceancolour-glo-bgc-l4-nrt
- wekeo-mercator-oceancolour-ibi-bgc-hr-l3-nrt
- wekeo-mercator-oceancolour-ibi-bgc-hr-l4-nrt
- wekeo-mercator-oceancolour-med-bgc-hr-l3-nrt
- wekeo-mercator-oceancolour-med-bgc-hr-l4-nrt
- wekeo-mercator-oceancolour-med-bgc-l3-my
- wekeo-mercator-oceancolour-med-bgc-l3-nrt
- wekeo-mercator-oceancolour-med-bgc-l4-my
- wekeo-mercator-oceancolour-med-bgc-l4-nrt
- wekeo-mercator-oceancolour-nws-bgc-hr-l3-nrt
- wekeo-mercator-oceancolour-nws-bgc-hr-l4-nrt
- wekeo-mercator-seaice-ant-phy-auto-l3-nrt
- wekeo-mercator-seaice-ant-phy-l3-my
- wekeo-mercator-seaice-arc-phy-auto-l4-nrt
- wekeo-mercator-seaice-arc-phy-climate-l3-my
- wekeo-mercator-seaice-arc-phy-climate-l4-my
- wekeo-mercator-seaice-arc-phy-l4-nrt
- wekeo-mercator-seaice-arc-seaice-l3-rep-observations
- wekeo-mercator-seaice-arc-seaice-l4-nrt-observations
- wekeo-mercator-seaice-bal-phy-l4-my
- wekeo-mercator-seaice-bal-seaice-l4-nrt-observations
- wekeo-mercator-seaice-glo-seaice-l4-nrt-observations
- wekeo-mercator-seaice-glo-seaice-l4-rep-observations
- wekeo-mercator-sealevel-atl-phy-hr-l3-my
- wekeo-mercator-sealevel-blk-phy-mdt-l4-static
- wekeo-mercator-sealevel-eur-phy-l3-my
- wekeo-mercator-sealevel-eur-phy-l3-nrt-observations
- wekeo-mercator-sealevel-eur-phy-l4-my
- wekeo-mercator-sealevel-eur-phy-l4-nrt-observations
- wekeo-mercator-sealevel-glo-phy-climate-l4-my
- wekeo-mercator-sealevel-glo-phy-l3-my
- wekeo-mercator-sealevel-glo-phy-l3-nrt-observations
- wekeo-mercator-sealevel-glo-phy-l4-my
- wekeo-mercator-sealevel-glo-phy-l4-nrt-observations
- wekeo-mercator-sealevel-glo-phy-mdt
- wekeo-mercator-sealevel-med-phy-mdt-l4-static
- wekeo-mercator-sst-atl-phy-l3s-my
- wekeo-mercator-sst-atl-phy-l3s-nrt
- wekeo-mercator-sst-atl-sst-l4-nrt-observations
- wekeo-mercator-sst-atl-sst-l4-rep-observations
- wekeo-mercator-sst-bal-phy-l3s-my
- wekeo-mercator-sst-bal-phy-subskin-l4-nrt
- wekeo-mercator-sst-bal-sst-l3s-nrt-observations
- wekeo-mercator-sst-bal-sst-l4-nrt-observations
- wekeo-mercator-sst-bal-sst-l4-rep-observations
- wekeo-mercator-sst-bs-phy-l3s-my
- wekeo-mercator-sst-bs-phy-subskin-l4-nrt
- wekeo-mercator-sst-bs-sst-l3s-nrt-observations
- wekeo-mercator-sst-bs-sst-l4-nrt-observations
- wekeo-mercator-sst-bs-sst-l4-rep-observations
- wekeo-mercator-sst-glo-sst-l3s-nrt-observations
- wekeo-mercator-sst-glo-sst-l4-nrt-observations
- wekeo-mercator-sst-glo-sst-l4-rep-observations
- wekeo-mercator-sst-med-phy-l3s-my
- wekeo-mercator-sst-med-phy-subskin-l4-nrt
- wekeo-mercator-sst-med-sst-l3s-nrt-observations
- wekeo-mercator-sst-med-sst-l4-nrt-observations
- wekeo-mercator-sst-med-sst-l4-rep-observations
- wekeo-mercator-wave-glo-phy-spc-l3-my
- wekeo-mercator-wave-glo-phy-spc-l4-nrt
- wekeo-mercator-wave-glo-phy-swh-l3-my
- wekeo-mercator-wave-glo-phy-swh-l3-nrt
- wekeo-mercator-wave-glo-phy-swh-l4-my
- wekeo-mercator-wave-glo-phy-swh-l4-nrt
- wekeo-mercator-wave-glo-wav-l3-spc-nrt-observations
- wekeo-mercator-wind-glo-phy-climate-l4-my
- wekeo-mercator-wind-glo-phy-l4-my
- wekeo-mercator-wind-glo-phy-l4-nrt
- wekeo-mercator-wind-glo-wind-l3-nrt-observations
- wekeo-mercator-wind-glo-wind-l3-rep-observations

The descriptions can be retrieved directly from [WEkEO](https://www.wekeo.eu/data)

## Using climetlab to access the data

See the [demo notebooks](https://github.com/wekeo/climetlab-wekeo-mercator/tree/main/notebooks)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/wekeo/climetlab-wekeo-mercator/main?urlpath=lab)


- [demo_main.ipynb](https://github.com/wekeo/climetlab-wekeo-mercator/tree/main/notebooks/demo_main.ipynb)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/wekeo/climetlab-wekeo-mercator/blob/main/notebooks/demo_main.ipynb)
[![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wekeo/climetlab-wekeo-mercator/blob/main/notebooks/demo_main.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/wekeo/climetlab-wekeo-mercator/main?filepath=notebooks/demo_main.ipynb)
[<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/wekeo/climetlab-wekeo-mercator/tree/main/notebooks/demo_main.ipynb)



The climetlab python package allows easy access to the data with a few lines of code such as:
``` python

!pip install climetlab climetlab-wekeo-mercator
import climetlab as cml
ds = cml.load_dataset(
    "wekeo-mercator-sst-glo-sst-l4-rep-observations",
    area=[30,-30,-30,-30],
    end="1981-11-01",
    variables="analysed_sst"
)
ds.to_xarray()
```


Support and contributing
------------------------

Please open a issue on github if this is a github repository.

LICENSE
-------

See the LICENSE file.
(C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
This software is licensed under the terms of the Apache Licence Version 2.0
which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
In applying this licence, ECMWF does not waive the privileges and immunities
granted to it by virtue of its status as an intergovernmental organisation
nor does it submit to any jurisdiction.

Authors
-------

Germano Guerrini and al.

See also the CONTRIBUTORS.md file.
