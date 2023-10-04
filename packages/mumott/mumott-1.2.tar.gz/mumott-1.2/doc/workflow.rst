.. _workflow:
.. index:: Workflow

.. raw:: html

    <style> .orange {color:orange} </style>
    <style> .blue {color:CornflowerBlue} </style>
    <style> .green {color:darkgreen} </style>

.. role:: orange
.. role:: blue
.. role:: green


Workflow
********

The following figure illustrates the :program:`mumott` workflow.
Here, classes are shown in :blue:`blue`, input parameters and data in :orange:`orange`, and output data in :green:`green`.

.. graphviz:: _static/workflow.dot

A typical workflow involves the following steps:

#. First the :orange:`measured data along with its metadata` is loaded into a :class:`DataContainer <mumott.data_handling.DataContainer>` object.
   The latter allows one to access, inspect, and modify the data in various ways as shown in the
   `tutorial on loading and inspecting data tutorial <tutorials/inspect_data.html>`_.
   Note that it is possible to skip the full data when instantiating a :class:`DataContainer <mumott.data_handling.DataContainer>` object.
   In that case only geometry and diode data are read, which is much faster and sufficient for alignment.

#. The :class:`DataContainer <mumott.data_handling.DataContainer>` object holds the information pertaining to the geometry of the data.
   The latter is stored in the :attr:`geometry <mumott.data_handling.DataContainer.geometry>` property of the
   :class:`DataContainer <mumott.data_handling.DataContainer>` object in the form of a :class:`Geometry <mumott.core.geometry.Geometry>` object.

#. The geometry information is then used to set up a :ref:`projector object <projectors>`,
   e.g., :attr:`SAXSProjectorBilinear <mumott.methods.projectors.SAXSProjectorBilinear>`.
   Projector objects allow one to transform tensor fields from three-dimensional space to projection space.

#. Next a :ref:`basis set object <basis_sets>` such as, e.g., :class:`SphericalHarmonics <mumott.methods.basis_sets.SphericalHarmonics>`, is set up.

#. One can then combine the :ref:`projector object <projectors>`, the :ref:`basis set <basis_sets>`, and the data from
   the :class:`DataContainer <mumott.data_handling.DataContainer>` object to set up a :ref:`residual calculator object <residual_calculators>`.
   :ref:`Residual calculator objects <residual_calculators>` hold the coefficients that need to be optimized and allow one to compute the residuals of the current representation.

#. To find the optimal coefficients a :ref:`loss function object <loss_functions>` is set up, using, e.g., the :class:`SquaredLoss <mumott.optimization.loss_functions.SquaredLoss>` or :class:`HuberLoss <mumott.optimization.loss_functions.HuberLoss>` classes.
   The :ref:`loss function <loss_functions>` can include one or several regularization terms, which are defined by :ref:`regularizer objects <regularizers>` such as :class:`L1Norm <mumott.optimization.regularizers.L1Norm>`, :class:`L2Norm <mumott.optimization.regularizers.L2Norm>` or :class:`TotalVariation <mumott.optimization.regularizers.TotalVariation>`.

#. The :ref:`loss function object <loss_functions>` is then handed over to an :ref:`optimizer object <optimizers>`,
   such as :class:`LBFGS <mumott.optimization.optimizers.LBFGS>` or :class:`GradientDescent <mumott.optimization.optimizers.GradientDescent>`,
   which updates the coefficients of the :ref:`residual calculator object <residual_calculators>`.

#. The optimized coefficients can then be processed via the :ref:`basis set object <basis_sets>`
   to generate :green:`tensor field properties` such as the anisotropy or the orientation distribution, returned as a ``dict``.

#. The function :func:`dict_to_h5 <mumott.output_handling.dict_to_h5>` can be used to convert this dictionary of properties into an ``h5`` file, to be further processed or visualized.


Pipelines
=========

Reconstruction workflows can be greatly abstracted via :ref:`reconstruction pipelines <reconstruction_pipelines>`.
A pipeline contains a typical series of objects linked together, and it is possible to replace some of the components in the pipeline with others preferred by the user.

.. graphviz:: _static/pipeline.dot

The user interaction with the pipeline can be understood as follows:

#. A :class:`DataContainer <mumott.data_handling.DataContainer>` instance is created from input, as in a standard workflow.

#. The :class:`DataContainer <mumott.data_handling.DataContainer>` is passed to a :ref:`pipeline <reconstruction_pipelines>` function, e.g., the :func:`SIGTT pipeline function <mumott.pipelines.reconstruction.run_sigtt>`, along with user-specified parameters as keyword arguments.

#. For example, one might want to set the regularization weight for the :class:`Laplacian <mumott.optimization.regularizers.Laplacian>` regularizer (using the ``regularization_weight`` keyword argument), or one might want to replace the default :class:`SAXSProjectorBilinear <mumott.methods.projectors.SAXSProjectorBilinear>` with the GPU-based :class:`SAXSProjectorCUDA <mumott.methods.projectors.SAXSProjectorCUDA>` (using the ``Projector`` keyword argument).

#. The :func:`SIGTT pipeline <mumott.pipelines.reconstruction.run_sigtt>` executes, and returns a ``dict`` which contains the entry ``'result'`` with the optimization coefficients.
   In addition, it contains the entries ``optimizer``, ``loss_function``, ``residual_calculator``, ``basis_set``, and ``projector``, all containing the instances of the respective objects used in the pipeline.

#. The ``get_output`` method of the :ref:`basis set <basis_sets>` can then be used to generate tensor field properties, as in the standard workflow.
