Time Domain
--------------------

It is important to note that optical time may not be in sync to
electronic time. This means that optical signals vary and change
independently of electronic signals. Fundamentally, this means that
electronic-photonic systems are interconnected but can be operating at
different clock rates, and both electronic and photonic functions depend
on both the inputs of both electronic and photonic systems.

Actual operations are combined and need to be treated as mixed systems,
they can not be considered independently because on its own that does
not represent a *useful* output.

We can now simulate SPICE-based circuits alongside ourdefined layout
electrical models. This allows us the power to implement our own
sources, and our own components in a more complete manner. However, this
does not fundamentally solve the problem we have on multiple time domain
simulations. We have timing data from digital sources and analog
electronic sources. If you have delayed photonic signals, then we also
have timing data independently in the photonic domain. This leads to a
major time-synchronisation issue. It is in this type of problem
structure that a microservice implementation again comes to the rescue.

For example, digital signals are particularly valuable and useful when
considering steady-state signal propagation. Analogue signals are
particularly interesting in the transition between electronic states, as
the rise-times and signal-shapes will be determined by RC constants
primarily. In the midst of all of this, photonic signals can change
independently. There is a direct control from the electronics to the
unitary of the component, and at discretised points in time the unitary
can be computed. For the period of discrete time this signal is valid,
the unitary can be computed. The accuracy desired is just determined by
the discretization time. In that period of time, there is a linear
relationship between optical signal inputs, and outputs.

As an approximation, if the signals are switching between logic levels,
then it is reasonable to compute the analog rise-time and fall-time
signals accordingly and operate on them linearly if the digital clock
period is high. However, if the logic levels in which the signal is
switching is
