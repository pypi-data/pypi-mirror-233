Quick start
===========

Once the plugin is installed, it can be used directly into a Jupyter notebook.


.. code-block:: python

    import climetlab as cml
    from dask.distributed import Client

    # Instantiate a default Dask distributed client to handle data
    client = Client()

    cmlds = cml.load_dataset(
        "wekeo-mercator-sst-glo-sst-l4-rep-observations",
        area=[30,-30,-30,-30],
        end="1981-11-01",
        variables="analysed_sst"
    )

    array = cmlds.to_xarray()
    array.analysed_sst.isel(time=1).plot(x="lon", y="lat", col_wrap=3)

    client.shutdown()

.. image:: ../images/plot.png
    :width: 400

.. note::
    When `to_xarray` gets called, it tries to combine all the downloaded files, assuming that they can be either
    concatenated by the time dimension or merged if they feature the same time span and non-overlapping variables.
    Therefore, depending on how the data are sliced through files, the default algorith cannot work or make sense.
    In those cases, it is up to the users to determine the best strategy relatively to their needs.