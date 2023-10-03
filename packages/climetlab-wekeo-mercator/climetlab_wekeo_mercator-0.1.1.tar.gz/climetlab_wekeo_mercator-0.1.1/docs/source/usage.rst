Usage
=====

Building a CliMetLab query
---------------------------------------------------------------

The WEkEO CliMetLab Plugin gives access to a wide range of WEkEO datasets. All WEkEO datasets can be explored in the  `WEkEO Viewer <https://www.wekeo.eu/data?view=viewer>`_. 

The CliMetLab WEkEO CMEMS Plugin supports the datasets of the Copernicus Marine Service. 


A dataset can be accessed using CliMatLab with the ``load_dataset`` function. The minimum required argument for the function ``load_dataset`` is the dataset id. 

The CliMetLab dataset id can be derived from the dataset id inside the WEkEO viewer. For example: 

- WEkEO dataset id: ``EO:MO:DAT:SST_MED_SST_L4_NRT_OBSERVATIONS_010_004``
- CliMetLab dataset id: ``wekeo-mercator-sst-med-sst-l4-nrt-observations``


.. note::
     The datasets of the Copernicus Marine Service are structured as datasets with one to many sub-datasets, also calles **layers**, that belong in the dataset group.
     Using the CliMetLab one layer can be downloaded at a time. 
     Therefore, the ``load_dataset`` function needs an additional argument ``layer`` for datasets which contain more than one layer. 

To find out which layers and variables are available for a dataset, there are two options: 

1. Explore layers and attributes in the `WEkEO Viewer <https://www.wekeo.eu/data?view=viewer>`_

The datasets are available in the WEkEO Catalogue. 

.. image:: ../images/mercator-wekeo-catalogue.png
    :width: 400

When klicking on "Add to map..." the available layers are shown.

.. image:: ../images/wekeo-layers.png
    :width: 400


The layer of choice can then be added to the WEkEO Viewer, where the availabe attributes for subsetting the dataset are shown as well. 
By examining the WEkEO API request, the exact names of the layers and attributes are shown as they are requires for the CliMetLab ``load_dataset`` request.


2. Explore attributes in the Plugin source code

Each dataset is described with its attributes in a separate python file in the `plugin source code <https://github.com/wekeo/climetlab-wekeo-mercator/tree/main>`_. 

The above-described ERA5 dataset can be found `here <https://github.com/wekeo/climetlab-wekeo-mercator/blob/main/climetlab_wekeo_mercator/sst_med_sst_l4_nrt_observations.py>`_.


Now, a CliMetLab query for WEkEO data can be created: 

.. code-block:: python

    ds = cml.load_dataset(
        "wekeo-mercator-sst-med-sst-l4-nrt-observations", 
        layer="SST_MED_SST_L4_NRT_OBSERVATIONS_010_004_a_V2", # Mediterranean sst analysis, l4, 1/16deg daily (sst med sst l4 NRT observations 010 004 a v2)
        start = "2020-01-01T00:00:00Z",
        end = "2020-01-31T00:00:00Z"
        )

Accessing a single dataset through CliMetLab
--------------------------------------------

This query triggers the download of a subset of a single dataset layer. 

.. code-block:: python

    import climetlab as cml
    ds = cml.load_dataset(
        "wekeo-mercator-sst-med-sst-l4-nrt-observations", 
        layer="SST_MED_SST_L4_NRT_OBSERVATIONS_010_004_a_V2", # Mediterranean sst analysis, l4, 1/16deg daily (sst med sst l4 NRT observations 010 004 a v2)
        start = "2020-01-01T00:00:00Z",
        end = "2020-01-31T00:00:00Z"
        )

The download result is stores in chache. Running again the `cml.load_dataset` for the same dataset and the identical parameters will not trigger a new download, but will use the cached data instead. 

After downloading, the dataset can be converted to xarray using the `to_xarray` function:

.. code-block:: python

    xarr = ds.to_xarray()
    xarr

Using the python `xarray` module, the dataset can be analyzed and plotted.

.. code-block:: python

    import matplotlib.pyplot as plt 

    xarr.analysed_sst.isel(time=0).plot(cbar_kwargs= {'orientation': 'horizontal'})
    plt.axis('scaled')

.. image:: ../images/wekeo-plot-sst.png
    :width: 600

Working with two or more datasets using CliMetLab
-------------------------------------------------

In many cases it is necessary to combine more datasets and variables for data analysis.
Using the WEkEO CliMetLab Plugin, datasets from different sources can be downloaded and combined. 
This example adds another layer from the ``EO:MO:DAT:SST_MED_SST_L4_NRT_OBSERVATIONS_010_004``, the sea surface temperature anomaly to the data created above.

.. code-block:: python

    import climetlab as cml
    ds_anomaly = cml.load_dataset(
        "wekeo-mercator-sst-med-sst-l4-nrt-observations", 
        layer="SST_MED_SSTA_L4_NRT_OBSERVATIONS_010_004_b", # Mediterranean sst anomaly, l4, 1/16deg daily (sst med ssta l4 NRT observations 010 004 b)
        start = "2020-01-01T00:00:00Z",
        end = "2020-01-31T00:00:00Z"
        )
    #convert the climetlab output to xarray
    xarr_anomaly = ds.to_xarray()

    # merge both xarrays to oe dataset 
    sst_med = xarr.merge(xarr_anomaly)

More examples on merging datasets using the CliMetLab access to the data can be found `here <https://climetlab-wekeo-ecmwf.readthedocs.io/en/latest/usage.html#working-with-two-or-more-datasets-using-climetlab>`_. 

Handling Merge errors
---------------------

The ``to_xarray`` function is not supported for all datasets depending of the datasets' shape and variable names. In such cases the following error will occur: 

.. error:: 
    MergeError: Cannot safely merge your data. Try to download a single variable or loop over the files and call `to_xarray` on each one.

For a dataset example on how to possibly handle this error, please refer to the `CliMetLab WEkEO ECMWF Documentation <https://climetlab-wekeo-ecmwf.readthedocs.io/en/latest/usage.html#handling-merge-errors>`_


Caching and Storage of CliMetLab datasets
-----------------------------------------

The CliMetLab source module works with caching instead of storing files in the local file system. 
This brings the advantage that the user does not have to clean up the local disk, but the files will be removed automatically when the cache is cleared. 

.. warning::

    When working with large datasets the files will fill up the computers cache, or the data cannot be fully downloaded if the queried volume does not fit fully in cache. 

For large volumes of data it is recommended to change the default location where CliMetLab stores the data from cache to a large disk or object storage. 
All benefits of the data management of CliMetLab remain, except the datasets are not deleted when the cache is cleared. They will be persistent on the drive instead. 

.. code-block:: python 

     import climetlab as cml

     cml.settings.get("cache-directory") # Find the current cache directory

     "/tmp/climetlab-$USER"
     
     # Change the value of the setting
     cml.settings.set("cache-directory", "/big-disk/climetlab-cache")

     # Python kernel restarted

     import climetlab as cml
     cml.settings.get("cache-directory") # Cache directory has been modified
     
     "/big-disk/climetlab-cache"


More information on caching can be found in the official documentation of CliMetLab (`Caching <https://climetlab.readthedocs.io/en/latest/guide/caching.html>`_).