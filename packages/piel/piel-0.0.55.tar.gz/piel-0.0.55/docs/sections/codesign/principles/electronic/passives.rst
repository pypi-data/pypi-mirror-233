Passives
----------

Read further in *Digital Integrated Electronics* by Jan Rabaey.

It is important to understand the relationship between electrical models of physical geometrical designs in relation to their photonic operation. Multiple photonic electronic-related layers have different resistive and inductive relationships. The interconnection mechanism has an effect on the propagation delay, power consumption, and noise.

Each wire has parasitic capacitance's, resistances, and inductance. We need to account these differential circuit elements as points within the lab. Note that the wire parasitic capacitance is three-dimensional. Ideally, we can extract this information through RCX of the circuit.

Simple Capacitive Modelling
^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO add figure

When electrical field lines are orthogonal, we can account for the width :math:`W`, length :math:`L`, dielectric constant :math:`\epsilon` between the metal plates, and the thickness of the dielectric :math:`t`.

.. math::

    \begin{equation}
        C_{int} = \frac{\epsilon WL }{t_{\text{dielectric}}}
    \end{equation}

This is coupled to the resistivity :math:`\rho` of the wire with the thickness of the metal :math:`H` and width :math:`W` to determine the its cross sectional area :math:`A`.

.. math::
    \begin{equation}
        R = \frac{\rho L}{A} = \frac{\rho L}{HW}
    \end{equation}

However, because we know the thickness for any particular metal :math:`H`, we can determine the resistance of a wire just from the geometry. Normally, these material parameters are determined in the form of a :math:`R_{\square}` resistance.

.. math::
    \begin{equation}
        R = R_{\square} \frac{\rho}{H} = \frac{\rho}{H}
    \end{equation}
