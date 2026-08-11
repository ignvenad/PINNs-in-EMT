from pathlib import Path
import sys

parent_folder = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_folder))

import numpy as np
from src.plotter_class import Sim_Plotter

def is_approx_integer(x, tol=1e-6):
    assert abs(x - round(x)) < tol, "Not an integer number"
    return round(x)

def compute_error(array1, array2, abs=False):
    if abs:
        return np.abs(array1 - array2)
    else:
        return array1 - array2

type_solve_sim1 = 'nr'
type_solve_sim2 = 'nn'
setup_name = 'sim_1'
path_sim1  = f'./Saved_trajectories/Sim_100events/{type_solve_sim1}_{setup_name}.npz'
path_sim2 = f'./Saved_trajectories/Sim_100events/{type_solve_sim2}_{setup_name}.npz'

data_sim1 = np.load(path_sim1, allow_pickle=True)
sim_step_sim1 = data_sim1["metadata"].tolist()["step_size_plot"]
sim_time_sim1 = data_sim1["metadata"].tolist()["sim_time"]
print(type_solve_sim1, data_sim1["metadata"].tolist()["compute_time"])

time_array_sim1     = data_sim1["time"]
ea_array_sim1       = data_sim1["ea"]
va_array_sim1       = data_sim1["va"]
ua_array_sim1       = data_sim1["ua"]
va_cap_array_sim1   = data_sim1["va_cap"]
ia1_array_sim1      = data_sim1["ia1"]
ia2_array_sim1      = data_sim1["ia2"]
ia3_array_sim1      = data_sim1["ia3"]
x1_array_sim1       = data_sim1["pll_vars"][:, 0]
theta_array_sim1    = data_sim1["pll_vars"][:, 1]
freq_array_sim1     = data_sim1["w_pll"]
ud_array_sim1       = data_sim1["udq"][:, 0]
vd_array_sim1       = data_sim1["vdq"][:, 0]
uq_array_sim1       = data_sim1["udq"][:, 1]
vq_array_sim1       = data_sim1["vdq"][:, 1]
valpha_array_sim1   = data_sim1["valpha_beta"][:, 0]
vbeta_array_sim1    = data_sim1["valpha_beta"][:, 1]
ialpha_array_sim1   = data_sim1["ialpha_beta"][:, 0]
ibeta_array_sim1    = data_sim1["ialpha_beta"][:, 1]
P1_array_sim1       = data_sim1["S1"][:, 0]
P2_array_sim1       = data_sim1["S2"][:, 0]
P3_array_sim1       = data_sim1["S3"][:, 0]
Q1_array_sim1       = data_sim1["S1"][:, 1]
Q2_array_sim1       = data_sim1["S2"][:, 1]
Q3_array_sim1       = data_sim1["S3"][:, 1]
Pstar_array_sim1    = data_sim1["Pref"][:]
Vstar_array_sim1    = data_sim1["Vref"][:]
id1_array_sim1      = data_sim1["idq1"][:, 0]
iq1_array_sim1      = data_sim1["idq1"][:, 1]
id2_array_sim1      = data_sim1["idq2"][:, 0]
iq2_array_sim1      = data_sim1["idq2"][:, 1]
id2_star_array_sim1 = data_sim1["idq2_star"][:, 0]
iq2_star_array_sim1 = data_sim1["idq2_star"][:, 1]
phi_p_pc_array_sim1 = data_sim1["phipq_pc"][:, 0]
phi_q_pc_array_sim1 = data_sim1["phipq_pc"][:, 1]
phi_d_cc_array_sim1 = data_sim1["phidq_cc"][:, 0]
phi_q_cc_array_sim1 = data_sim1["phidq_cc"][:, 1]

data_sim2 = np.load(path_sim2, allow_pickle=True)
sim_step_sim2 = data_sim2["metadata"].tolist()["step_size_plot"]
sim_time_sim2 = data_sim2["metadata"].tolist()["sim_time"]
print(type_solve_sim2, data_sim2["metadata"].tolist()["compute_time"])

time_array_sim2     = data_sim2["time"]
ea_array_sim2       = data_sim2["ea"]
va_array_sim2       = data_sim2["va"]
ua_array_sim2       = data_sim2["ua"]
va_cap_array_sim2   = data_sim2["va_cap"]
ia1_array_sim2      = data_sim2["ia1"]
ia2_array_sim2      = data_sim2["ia2"]
ia3_array_sim2      = data_sim2["ia3"]
x1_array_sim2       = data_sim2["pll_vars"][:, 0]
theta_array_sim2    = data_sim2["pll_vars"][:, 1]
freq_array_sim2     = data_sim2["w_pll"]
ud_array_sim2       = data_sim2["udq"][:, 0]
vd_array_sim2       = data_sim2["vdq"][:, 0]
uq_array_sim2       = data_sim2["udq"][:, 1]
vq_array_sim2       = data_sim2["vdq"][:, 1]
valpha_array_sim2   = data_sim2["valpha_beta"][:, 0]
vbeta_array_sim2    = data_sim2["valpha_beta"][:, 1]
ialpha_array_sim2   = data_sim2["ialpha_beta"][:, 0]
ibeta_array_sim2    = data_sim2["ialpha_beta"][:, 1]
P1_array_sim2       = data_sim2["S1"][:, 0]
P2_array_sim2       = data_sim2["S2"][:, 0]
P3_array_sim2       = data_sim2["S3"][:, 0]
Q1_array_sim2       = data_sim2["S1"][:, 1]
Q2_array_sim2       = data_sim2["S2"][:, 1]
Q3_array_sim2       = data_sim2["S3"][:, 1]
Pstar_array_sim2    = data_sim2["Pref"][:]
Vstar_array_sim2    = data_sim2["Vref"][:]
id1_array_sim2      = data_sim2["idq1"][:, 0]
iq1_array_sim2      = data_sim2["idq1"][:, 1]
id2_array_sim2      = data_sim2["idq2"][:, 0]
iq2_array_sim2      = data_sim2["idq2"][:, 1]
id2_star_array_sim2 = data_sim2["idq2_star"][:, 0]
iq2_star_array_sim2 = data_sim2["idq2_star"][:, 1]
phi_p_pc_array_sim2 = data_sim2["phipq_pc"][:, 0]
phi_q_pc_array_sim2 = data_sim2["phipq_pc"][:, 1]
phi_d_cc_array_sim2 = data_sim2["phidq_cc"][:, 0]
phi_q_cc_array_sim2 = data_sim2["phidq_cc"][:, 1]

assert isinstance(sim_step_sim1, float)
assert isinstance(sim_time_sim1, float)
assert isinstance(sim_step_sim2,  float)
assert isinstance(sim_time_sim2,  float)
assert sim_step_sim1 == sim_step_sim2
assert sim_time_sim1 == sim_time_sim2 # can be changed if shorter sim
assert np.allclose(Pstar_array_sim1, Pstar_array_sim2)
assert np.allclose(Vstar_array_sim1, Vstar_array_sim2)

err_phi_p_pc = compute_error(phi_p_pc_array_sim1, phi_p_pc_array_sim2)
err_phi_q_pc = compute_error(phi_q_pc_array_sim1, phi_q_pc_array_sim2)
err_phi_d_cc = compute_error(phi_d_cc_array_sim1, phi_d_cc_array_sim2)
err_phi_q_cc = compute_error(phi_q_cc_array_sim1, phi_q_cc_array_sim2)
err_ua       = compute_error(ua_array_sim1[:, 0], ua_array_sim2[:, 0])
err_va       = compute_error(va_array_sim1[:, 0], va_array_sim2[:, 0])
err_va_cap   = compute_error(va_cap_array_sim1[:, 0], va_cap_array_sim2[:, 0])
err_ia1      = compute_error(ia1_array_sim1[:, 0], ia1_array_sim2[:, 0])
err_ia2      = compute_error(ia2_array_sim1[:, 0], ia2_array_sim2[:, 0])
err_ia3      = compute_error(ia3_array_sim1[:, 0], ia3_array_sim2[:, 0])
err_P1       = compute_error(P1_array_sim1, P1_array_sim2)
err_P2       = compute_error(P2_array_sim1, P2_array_sim2)
err_P3       = compute_error(P3_array_sim1, P3_array_sim2)
err_Q1       = compute_error(Q1_array_sim1, Q1_array_sim2)
err_Q2       = compute_error(Q2_array_sim1, Q2_array_sim2)
err_Q3       = compute_error(Q3_array_sim1, Q3_array_sim2)
err_ud       = compute_error(ud_array_sim1, ud_array_sim2)
err_uq       = compute_error(uq_array_sim1, uq_array_sim2)
err_vd       = compute_error(vd_array_sim1, vd_array_sim2)
err_vq       = compute_error(vq_array_sim1, vq_array_sim2)
err_id2      = compute_error(id2_array_sim1, id2_array_sim2)
err_iq2      = compute_error(iq2_array_sim1, iq2_array_sim2)
err_id2_star = compute_error(id2_star_array_sim1, id2_star_array_sim2)
err_iq2_star = compute_error(iq2_star_array_sim1, iq2_star_array_sim2)
err_x1 = x1_array_sim1 - x1_array_sim2
err_theta = theta_array_sim1 - theta_array_sim2
for i in range(len(err_theta)):
    if err_theta[i] > 6.2:
        err_theta[i] -= 2*np.pi
    elif err_theta[i] < -6.2:
        err_theta[i] += 2*np.pi
err_freq  = freq_array_sim1 - freq_array_sim2

arrays_review = {
    "freq": err_freq,
    "P2": err_P2,
    "Q2": err_Q2,
    "id2": err_id2,
    "id2_star": err_id2_star,
    "ud": err_ud,
    "uq": err_uq,
    "vd": err_vd,
    "vq": err_vq,
    "phi_p_pc": err_phi_p_pc,
    "phi_q_pc": err_phi_q_pc,
    "phi_d_cc": err_phi_d_cc,
    "phi_q_cc": err_phi_q_pc
}

steady_state_time = 0.5
iteration_raw = steady_state_time/sim_step_sim1
iter_start = is_approx_integer(iteration_raw)

for name, arr in arrays_review.items():
    counter_above1 = 0
    counter_above05 = 0
    avg_error          = np.mean(np.abs(arr[iter_start:]))
    maximum_error      = np.max(np.abs(arr[iter_start:]))
    for elem in arr[:-1]:
        if np.abs(elem) > 0.01:
            counter_above1 += 1
        if np.abs(elem) > 0.005:
            counter_above05 += 1
    print(f"{name} -> absMaximum: {maximum_error} / mean: {avg_error}", counter_above05*sim_step_sim1, counter_above1*sim_step_sim1)


plotter = Sim_Plotter()
plotter_ones = np.ones_like(P1_array_sim1[iter_start:])
y_plotting = [
                [(P1_array_sim1[iter_start:], rf"$P2_{{{type_solve_sim1}}}$", "k", "--"), (P1_array_sim2[iter_start:], rf"$P2_{{{type_solve_sim2}}}$", "darkgreen", "-")],
                [(Q1_array_sim1[iter_start:], rf"$Q2_{{{type_solve_sim1}}}$", "k", "--"), (Q1_array_sim2[iter_start:], rf"$Q2_{{{type_solve_sim2}}}$", "darkgreen", "-")],
                [(ud_array_sim1[iter_start:], rf"$ud_{{{type_solve_sim1}}}$", "k", "--"), (ud_array_sim2[iter_start:], rf"$ud_{{{type_solve_sim2}}}$", "darkgreen", "-"), 
                 (vd_array_sim1[iter_start:], rf"$vd_{{{type_solve_sim1}}}$", "k", "--"), (vd_array_sim2[iter_start:], rf"$vd_{{{type_solve_sim2}}}$", "darkgreen", "-")],
                 [(uq_array_sim1[iter_start:], rf"$uq_{{{type_solve_sim1}}}$", "k", "--"), (uq_array_sim2[iter_start:], rf"$uq_{{{type_solve_sim2}}}$", "darkgreen", "-"), 
                 (vq_array_sim1[iter_start:], rf"$vq_{{{type_solve_sim1}}}$", "k", "--"), (vq_array_sim2[iter_start:], rf"$vq_{{{type_solve_sim2}}}$", "darkgreen", "-")],
                [(id2_array_sim1[iter_start:], rf"$id_{{{type_solve_sim1}}}$", "k", "--"),(id2_array_sim2[iter_start:], rf"$id_{{{type_solve_sim2}}}$", "darkgreen", "-")],
                [ (iq2_array_sim1[iter_start:], rf"$iq_{{{type_solve_sim1}}}$", "k", "--"), (iq2_array_sim2[iter_start:], rf"$iq_{{{type_solve_sim2}}}$", "darkgreen", "-")],
                [(id2_star_array_sim1[iter_start:], rf"$id^*_{{{type_solve_sim1}}}$", "k", "--"),(id2_star_array_sim2[iter_start:], rf"$id^*_{{{type_solve_sim2}}}$", "darkgreen", "-")],
                [ (iq2_star_array_sim1[iter_start:], rf"$iq^*_{{{type_solve_sim1}}}$", "k", "--"), (iq2_star_array_sim2[iter_start:], rf"$iq^*_{{{type_solve_sim2}}}$", "darkgreen", "-")]
            ]

## Errors
# y_plotting = [
#                 [(err_phi_p_pc[iter_start:], r"$\phi_{pc}$", "darkgreen", "-")],
#                 [(err_phi_d_cc[iter_start:], r"$\phi_{cc}$", "darkgreen", "-")], 
#                 [(err_id2[iter_start:], r"$i_{d,2}$", "darkgreen", "-")], 
#                 [(err_id2_star[iter_start:], r"$i_{d}^*$", "darkgreen", "-")],
#                 [(err_ud[iter_start:], r"$u_{d}^*$", "darkgreen", "-")],
#                 [(err_P2[iter_start:], r"$P^*-P_2$", "darkgreen", "-")],
#                 [(err_Q2[iter_start:], r"$i_{d}^*-i_{d,2}$", "darkgreen", "-")]
#                 ]

# y_plotting = [
#                 [(valpha_array_sim2[iter_start:], r"$v_{\alpha}$", "darkgreen", "-"), (vbeta_array_sim2[iter_start:], r"$v_{\beta}$", "darkgreen", "-"), 
#                  (plotter_ones*1.1, "", "black", "--"), (plotter_ones*(-1.1), "", "black", "--")],
#                 [(x1_array_sim2[iter_start:], r"$x_{1}$", "darkgreen", "-"), 
#                  (plotter_ones*0.1, "", "black", "--"), (plotter_ones*(-0.1), "", "black", "--")],
#                 [(vq_array_sim2[iter_start:], r"$v_{q}$", "darkgreen", "-"), 
#                  (plotter_ones*0.2, "", "black", "--"), (plotter_ones*(-0.2), "", "black", "--")],
#                  [(theta_array_sim2[iter_start:], r"$\theta_{pll}$", "darkgreen", "-"), 
#                  (plotter_ones*(2*np.pi+0.005), "", "black", "--"), (plotter_ones*(-0.005), "", "black", "--")],
#                 ]

# y_plotting = [
#                 [(phi_p_pc_array_sim1[iter_start:], r"$\phi_{pc}$", "darkgreen", "-"), (base_ones*0.075, "", "black", "--"), (base_ones*(-0.02), "", "black", "--")],
#                 [(phi_d_cc_array_sim1[iter_start:], r"$\phi_{cc}$", "darkgreen", "-"), (base_ones*0.075, "", "black", "--"), (base_ones*(-0.02), "", "black", "--")], 
#                 [(id2_array_sim1[iter_start:], r"$i_{d,2}$", "darkgreen", "-"), (base_ones*1.75, "", "black", "--"), (base_ones*(-0.1), "", "black", "--")], 
#                 [(id2_star_array_sim1[iter_start:], r"$i_{d}^*$", "darkgreen", "-"), (base_ones*1.8, "", "black", "--"), (base_ones*(-0.05), "", "black", "--")],
#                 [(ud_array_sim1[iter_start:], r"$u_{d}^*$", "darkgreen", "-"), (base_ones*1.3, "", "black", "--"), (base_ones*(0.7), "", "black", "--")],
#                 [(Pstar_array_sim1[iter_start:]-P1_array_sim1[iter_start:], r"$P^*-P_2$", "darkgreen", "-"), (base_ones*1.5, "", "black", "--"), (base_ones*(-0.25), "", "black", "--")],
#                 [(id2_star_array_sim1[iter_start:]-id2_array_sim1[iter_start:], r"$i_{d}^*-i_{d,2}$", "darkgreen", "-"), (base_ones*0.75, "", "black", "--"), (base_ones*(-0.5), "", "black", "--")],
#                 ]
                
x_plotting = [time_array_sim1[iter_start:].copy() for _ in range(len(y_plotting))]
plotter.plot_arrays(x_plotting, y_plotting)

