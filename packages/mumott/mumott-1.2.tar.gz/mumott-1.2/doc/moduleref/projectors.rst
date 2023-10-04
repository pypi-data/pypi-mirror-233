.. _projectors:

Projectors
==========

:program:`mumott` provides four different implementations of projectors suitable for :term:`SAXS` tomography.
While they should yield approximately equivalent results, they differ with respect to the resources they require.

:class:`SAXSProjectorCUDA <mumott.methods.projectors.SAXSProjectorCUDA>` and :class:`SAXSProjectorBilinear <mumott.methods.projectors.SAXSProjectorBilinear>` implement an equivalent algorithm for GPU and CPU resources, respectively.
These two options are *recommended* in terms of speed and ease of use.

:class:`SAXSProjectorAstra <mumott.methods.projectors.SAXSProjectorAstra>` provides an interface to a GPU implementation in the `ASTRA toolbox <https://www.astra-toolbox.com/>`_.
Finally, :class:`SAXSProjectorNumba <mumott.methods.projectors.SAXSProjectorNumba>` provides a CPU implementation using the `numba <https://numba.pydata.org/>`_ library.


.. autoclass:: mumott.methods.projectors.SAXSProjectorBilinear
   :members:
   :inherited-members:

.. autoclass:: mumott.methods.projectors.SAXSProjectorCUDA
   :members:
   :inherited-members:

.. autoclass:: mumott.methods.projectors.SAXSProjectorAstra
   :members:
   :inherited-members:

.. autoclass:: mumott.methods.projectors.SAXSProjectorNumba
   :members:
   :inherited-members:
