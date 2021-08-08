Environment Variables
=====================

Piano Video supports a few environment variables. To set an environment
variable in bash, run:

.. code-block:: bash

    export VARIABLE="value"

.. list-table:: Environment Variables
    :widths: 25 75
    :header-rows: 1

    * - Variable
      - Description
    * - ``PV_USE_CPP``
      - If present, use C++ libraries. Will compile at import.
    * - ``PV_USE_CUDA``
      - If present, use cuda libraries. Will compile at import.
    * - ``PV_MAX_THREADS``
      - Max number of threads to use when compiling. Defaults to 1.
