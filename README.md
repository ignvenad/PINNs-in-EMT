# PINNs in EMT simulation solvers
This library provides an Electromagnetic Transients (EMT) simulation solver for a type-4 wind turbine model connected through an LCL filter to an external source. The wind turbine model represents the grid-side converter as a voltage source and assumes a constant DC voltage. The control system is implemented in vector form using a dq frame, consisting of a synchronous reference frame, a Phase-Locked Loop (PLL), and cascaded PI controls that control active power injected into the external source and voltage magnitude at the PCC. The modulation block is assumed ideal. The system is based on the CIGRE benchmark model C4.49, as described in the "Multi-frequency stability of converter-based modern power systems" brochure.
The simulation solver integrates Neural Networks (NNs) and Physics-Informed Neural Networks (PINNs) to enhance the black-boxing capabilities of solvers with IP-protected control systems and to accelerate simulations when avoiding iterative solutions.

## Details in the associated paper
The motivation, methodology, and applications are discussed in the following paper under review:
I. Ventura, N. Darii, P. Aristidou, M. K. Bakhshizadeh, R. Nellikkath, B. Vilmann, and S. Chatzivasileiadis, "Physics-Informed Neural Network Models for EMT Simulators", 2026.

#### System parameters
The default system parameters are the following.
| **Variable**  | **Value** (%)  | **Variable**  |
|-----------|--------|-----------|
|$S_{b}$ | Rated power      |100 MW|
|$V_{g}$ | Nominal grid voltage      | 100 kV |
|$f_{0}$ | Rated frequency      |50 Hz|
|$T_{s}$ | Simulation time step size | {1-100} $\mu s$ |
|$K_{pll}$ | SRF PLL gains (kp, ki) | 25, 300 |
|$K_{pc}$ | Power controller gains (kp, ki) | 0.5, 30 |
|$K_{cc}$ | Current controller gains (kp, ki) | 0.1, 20 |
|$r_{c}, L_{c}$ | Converter-side inductor (pu) | 0.005, 0.1 |
|$r_{f}, C_{f}$ | Filter capacitor (pu) | 0.0757, 0.00184 |
|$r_{Lg}, L_{g}$ | Grid-side inductor (pu) | 0.005, 0.1 |

## Installation

To install the latest on GitHub:

```
pip install git+https://github.com/ignvenad/PINNs-in-EMT
```

## Vision
As explained in the paper, we envision a modular PINN integration, where the user can decide if they want to incorporate NN-based surrogate models in the simulation and which components to replace. We define and implement accurate NNs and PINNs that capture the most computationally intensive components of the simulation or models which need to remain confidential. PINNs provide faster and explicit evaluations of these components, thereby accelerating the underlying simulation algorithm when closed-loops are captured. We envision a library of accurately trained PINN models that can significantly accelerate time-domain simulations. See the following figure.
<p align="center">
<img align="middle" src="./Assets/fig_modular_approach.jpg" alt="Vision demo" width="800" height="450" />
</p>