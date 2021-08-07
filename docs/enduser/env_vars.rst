Environment Variables
=====================

Piano Video supports a few environment variables. To set an environment
variable in bash, run:

.. code-block:: bash

    export VARIABLE="value"

Piano Video will just check if the variable exists, so you don't have to worry
about the value.

.. list-table:: Environment Variables
    :widths: 25 75
    :header-rows: 1

    * - Variable
      - Description
    * - ``PV_USE_CPP``
      - Use C++ libraries. Will compile at import.
    * - ``PV_USE_CUDA``
      - Use cuda libraries. Will compile at import.
