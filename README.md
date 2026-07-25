# PINNs in EMT simulation solvers
This library provides an Electromagnetic Transients (EMT) simulation solver for a type-4 wind turbine model connected through an LCL filter to an external source. The wind turbine model represents the grid-side converter as a voltage source and assumes a constant DC voltage. The control system is implemented in vector form using a dq frame, consisting of a synchronous reference frame, a Phase-Locked Loop (PLL), and cascaded PI controls that control active power injected into the external source and voltage magnitude at the PCC. The modulation block is assumed ideal. The system is based on the CIGRE benchmark model C4.49, as described in the "Multi-frequency stability of converter-based modern power systems" brochure.
The simulation solver integrates Neural Networks (NNs) and Physics-Informed Neural Networks (PINNs) to enhance the black-boxing capabilities of solvers with IP-protected control systems and to accelerate simulations when avoiding iterative solutions.

## Details in the associated paper
The motivation, methodology, and applications are discussed in the following paper under review:

## Installation

To install the latest on GitHub:

```
pip install git+https://github.com/ignvenad/PINNs-in-EMT
```
