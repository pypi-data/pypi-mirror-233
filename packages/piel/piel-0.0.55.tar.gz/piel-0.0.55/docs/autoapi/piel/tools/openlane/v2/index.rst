:py:mod:`piel.tools.openlane.v2`
================================

.. py:module:: piel.tools.openlane.v2


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   piel.tools.openlane.v2.read_metrics_openlane_v2
   piel.tools.openlane.v2.run_openlane_flow



.. py:function:: read_metrics_openlane_v2(design_directory: piel.config.piel_path_types) -> dict

   Read design metrics from OpenLane v2 run files.

   :param design_directory: Design directory PATH.
   :type design_directory: piel_path_types

   :returns: Metrics dictionary.
   :rtype: dict


.. py:function:: run_openlane_flow(configuration: dict | None = None, design_directory: piel.config.piel_path_types = '.', parallel_asynchronous_run: bool = False, only_generate_flow_setup: bool = False)

   Runs the OpenLane v2 flow.

   :param configuration: OpenLane configuration dictionary. If none is present it will default to the config.json file on the design_directory.
   :type configuration: dict
   :param design_directory: Design directory PATH.
   :type design_directory: piel_path_types
   :param parallel_asynchronous_run: Run the flow in parallel.
   :type parallel_asynchronous_run: bool
   :param only_generate_flow_setup: Only generate the flow setup.
   :type only_generate_flow_setup: bool

   Returns:
