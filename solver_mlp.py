import numpy as np
import time
import yaml
from datetime import datetime
from src.plotter_class import Sim_Plotter
from src.nnet_eval_routine import explicit_inference_f

class EMT_simulator:
    def __init__(self, sim_time, sim_step):      
        self.sim_time = float(sim_time)
        self.sim_step = float(sim_step)
        self.ponder_trapz = self.sim_step / 2
        np.set_printoptions(precision=17, suppress=False)
        self.initialize_time_array()

    def initialize_time_array(self):
        no_steps_raw = self.sim_time / self.sim_step
        boolean_steps, no_steps_round = self.is_approx_integer(no_steps_raw)
        assert boolean_steps
        self.no_steps = no_steps_round + 1
        self.time_array  = np.arange(self.no_steps) * self.sim_step

    def upload_parameters(self, plot_step, config_file):
        with open(f"./sim_setups/{config_file}.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.establish_per_unit_system(config["system_base"])
        self.establish_parameters(config["system_params"])
        self.establish_control_gains(config["control_params"])
        self.establish_imposed_source(config["external_grid"])
        self.init_sim_saver(plot_step)
        self.initialize_converter_setpoints(config["init_setpoints"])
        self.upload_converter_setpoints_changes(config["events"])

    def initialize_converter_setpoints(self, init_values):
        P_ini = init_values["P"]
        V_ini = init_values["V"]
        self.Pref = np.full((self.no_steps, ), P_ini, dtype=np.float64)
        self.Vref = np.full((self.no_steps, ), V_ini, dtype=np.float64)
        self.Pref_plot = np.full((self.no_steps_plot, ), P_ini, dtype=np.float64)
        self.Vref_plot = np.full((self.no_steps_plot, ), V_ini, dtype=np.float64)
        assert self.time_array.shape[0] == self.Pref.shape[0]

    def upload_converter_setpoints_changes(self, setpoint_steps):
        setpoint_steps_list = list(setpoint_steps.keys())
        for i in setpoint_steps_list[:]:
            if setpoint_steps[i]["type"] == "P":
                success_boolean = False
                step_time = setpoint_steps[i]["time"] - 1e-8 # eps to make sure the comparison does not get 0.00520000001 as bigger than 0.0052
                step_value = setpoint_steps[i]["new_setpoint"]
                for elem_plot in range(self.time_array_plot.shape[0]):
                    if self.time_array_plot[elem_plot] > step_time:
                        self.Pref_plot[elem_plot:] = step_value
                        break
                for elem in range(self.time_array.shape[0]):
                    if self.time_array[elem] > step_time:
                        self.Pref[elem:] = step_value
                        success_boolean = True
                        break
                if not success_boolean:
                    raise Exception(f"Something went wrong in {i}!")
            elif setpoint_steps[i]["type"] == "V":
                success_boolean = False
                step_time = setpoint_steps[i]["time"] - 1e-8 # eps to make sure the comparison does not get 0.00520000001 as bigger than 0.0052
                step_value = setpoint_steps[i]["new_setpoint"]
                for elem_plot in range(self.time_array_plot.shape[0]):
                    if self.time_array_plot[elem_plot] > step_time:
                        self.Vref_plot[elem_plot:] = step_value
                        break
                for elem in range(self.time_array.shape[0]):
                    if self.time_array[elem] > step_time:
                        self.Vref[elem:] = step_value
                        success_boolean = True
                        break
                if not success_boolean:
                    raise Exception(f"Something went wrong in {i}!")
            elif setpoint_steps[i]["type"] == "CC":
                success_boolean = False
                step_time = setpoint_steps[i]["time"] - 1e-8
                if "fault_time" in setpoint_steps[i]:
                    end_time  = setpoint_steps[i]["time"] + setpoint_steps[i]["fault_time"] - 1e-8
                elif "end_time" in setpoint_steps[i]:
                    end_time = setpoint_steps[i]["end_time"]
                step_value = setpoint_steps[i]["new_setpoint"]
                for elem in range(self.time_array.shape[0]):
                    if self.time_array[elem] > step_time and self.time_array[elem] < end_time:
                        self.ea_array[elem, :] *= step_value
                for elem_plot in range(self.time_array_plot.shape[0]):
                    if self.time_array_plot[elem_plot] > step_time and self.time_array_plot[elem_plot] < end_time:
                        self.ea_array_plot[elem_plot, :] *= step_value
            elif setpoint_steps[i]["type"] == "PJ":
                success_boolean = False
                step_time = setpoint_steps[i]["time"] - 1e-8 # eps to make sure the comparison does not get 0.00520000001 as bigger than 0.0052
                phase_jump = setpoint_steps[i]["new_setpoint"]*np.pi/180
                for elem_plot in range(self.time_array_plot.shape[0]):
                    if self.time_array_plot[elem_plot] > step_time:
                        self.ea_array_plot[elem_plot:, :] = self.return_imposed_source(self.time_array_plot[elem_plot:], phase_jump)
                        break
                for elem in range(self.time_array.shape[0]):
                    if self.time_array[elem] > step_time:
                        self.ea_array[elem:, :] = self.return_imposed_source(self.time_array[elem:], phase_jump)
                        success_boolean = True
                        break
                if not success_boolean:
                    raise Exception(f"Something went wrong in {i}!")
        self.setpoint_vehicle = np.column_stack([self.Pref, self.Vref])

    def establish_parameters(self, system_params):
        self.wN = system_params["freq"]*2*np.pi
        self.wfs_shift = 2*np.pi/3
        self.L1 = system_params["L1"]
        self.R1 = system_params["R1"]
        self.L2 = system_params["L2"]
        self.R2 = system_params["R2"]
        self.C3 = system_params["C3"]
        self.R3 = system_params["R3"]
        self.micro_calculations_lib()

    def micro_calculations_lib(self):
        self.twothirds = 2/3
        self.sqrtthree_two = np.sqrt(3)/2
        self.angle_twopi = 2*np.pi

    def establish_per_unit_system(self, system_base):
        # V_base L-L rms
        self.V_base = system_base["Vbase"]
        self.S_base = system_base["Sbase"]
        self.I_base = self.S_base / (np.sqrt(3) * self.V_base)
        self.rmsLN_peakLN = np.sqrt(2)
        self.peakLN_rmsLN = 1 / np.sqrt(2)
        self.rmsLL_peakLN = np.sqrt(2) / np.sqrt(3)
        self.peakLN_rmsLL = np.sqrt(3) / np.sqrt(2)

    def establish_imposed_source(self, external_grid):
        self.E_rms_LL  = external_grid["V_nom"]
        self.E_peak_LN = external_grid["V_nom"] * np.sqrt(2) / np.sqrt(3)
        self.E_angl_ini = self.degrees_to_radians(external_grid["Angle_ini"])

    def establish_park_rotating_ref(self, park_angle):
        self.angl_pk = self.degrees_to_radians(park_angle)

    def establish_control_gains(self, control_params):
        self.Kp_cci = control_params["Kp_cci"]
        self.Ki_cci = control_params["Ki_cci"]
        self.Kp_pco = control_params["Kp_pco"]
        self.Ki_pco = control_params["Ki_pco"]
        self.Kp_pll = control_params["Kp_pll"]
        self.Ki_pll = control_params["Ki_pll"]

    def init_sim_saver(self, sim_plot_step:float):
        self.sim_step_plot = sim_plot_step
        assert sim_step <= sim_plot_step
        saving_it_raw = self.sim_step_plot / self.sim_step
        int_verification, self.saving_it = self.is_approx_integer(saving_it_raw)
        assert int_verification
        self.initialize_saving_arrays()
    
    def initialize_saving_arrays(self):
        no_steps_plot_raw = self.sim_time / self.sim_step_plot
        boolean_steps_plot, no_steps_plot_round = self.is_approx_integer(no_steps_plot_raw)
        assert boolean_steps_plot
        self.no_steps_plot = no_steps_plot_round + 1
        self.time_array_plot  = np.arange(self.no_steps_plot) * self.sim_step_plot

        assert self.time_array[0] == self.time_array_plot[0]

        self.ea_array = self.return_imposed_source(self.time_array[:])
        self.ea_array_plot = self.return_imposed_source(self.time_array_plot[:])

        self.elec_vars_plot = np.zeros((self.no_steps_plot, 21))
        
        self.control_vars_plot = np.zeros((self.no_steps_plot, 21))

    def is_approx_integer(self, x, tol=1e-6):
        return abs(x - round(x)) < tol, round(x)
    
    def degrees_to_radians(self, degrees_v):
        return degrees_v * np.pi / 180
    
    def init_neural_net(self, model_name):
        model_location = f'./NN_models/{model_name}'
        self.pinn_eval = explicit_inference_f(model_location, self.sim_step)
        self.pinn_eval_container = np.empty((5,), dtype=np.float64)
        self.mlp_name = model_name
    
    def return_imposed_source(self, t, phase_extra=0.):
        ea = self.E_peak_LN * np.cos(self.wN*t + self.E_angl_ini + phase_extra)
        eb = self.E_peak_LN * np.cos(self.wN*t + self.E_angl_ini - self.wfs_shift + phase_extra)
        ec = self.E_peak_LN * np.cos(self.wN*t + self.E_angl_ini + self.wfs_shift + phase_extra)
        return np.column_stack([ea, eb, ec])
    
    def create_state_matrix(self):
        state_matrix = np.zeros((4, 4))
        state_matrix[0, 0] = -1/self.R1
        state_matrix[0, 1] = (1/self.R1 + self.sim_step/(2*self.L1))
        state_matrix[0, 2] = 0.
        state_matrix[0, 3] = 0.
        state_matrix[1, 0] = -self.sim_step/(2*self.L2) - 1/self.R1 - 1/self.R3
        state_matrix[1, 1] = 1/self.R2
        state_matrix[1, 2] = self.sim_step/(2*self.L2)
        state_matrix[1, 3] = 1/self.R3
        state_matrix[2, 0] = 1/self.R3
        state_matrix[2, 1] = 0.
        state_matrix[2, 2] = 0.
        state_matrix[2, 3] = -1/self.R3 - 2*self.C3/self.sim_step
        state_matrix[3, 0] = self.sim_step/(2*self.L2)
        state_matrix[3, 1] = 0.
        state_matrix[3, 2] = -1/self.R2 - self.sim_step/(2*self.L2)
        state_matrix[3, 3] = 0.

        return state_matrix
    
    def calculate_pll_solution(self, x1_xn, x2_xn, vq_xn, valphabeta_xn1):
        self.pinn_eval_container[0] = x1_xn
        self.pinn_eval_container[1] = x2_xn
        self.pinn_eval_container[2] = vq_xn
        self.pinn_eval_container[3] = valphabeta_xn1[0]
        self.pinn_eval_container[4] = valphabeta_xn1[1]
        y = self.pinn_eval.run(self.pinn_eval_container)
        # y = self.pinn_eval.run(x1_xn, x2_xn, vq_xn, valphabeta_xn1[0], valphabeta_xn1[1])
        return y
    
    def park_transformation_xabc(self, theta_pll, xalphabeta):
        xalpha, xbeta = xalphabeta
        x_d =  np.cos(theta_pll)*xalpha + np.sin(theta_pll)*xbeta
        x_q =  -np.sin(theta_pll)*xalpha + np.cos(theta_pll)*xbeta

        return np.stack([x_d, x_q])
    
    def inverse_park_transformation_uabc(self, theta_pll, udq):
        ud, uq = udq
        ua = (np.cos(theta_pll)*ud                - np.sin(theta_pll)*uq)*self.rmsLL_peakLN*self.V_base
        ub = (np.cos(theta_pll-self.wfs_shift)*ud - np.sin(theta_pll-self.wfs_shift)*uq)*self.rmsLL_peakLN*self.V_base
        uc = (np.cos(theta_pll+self.wfs_shift)*ud - np.sin(theta_pll+self.wfs_shift)*uq)*self.rmsLL_peakLN*self.V_base

        return np.stack([ua, ub, uc])
    
    def clarke_transformation_xabc(self, xabc, base, transfer):
        xa, xb, xc = xabc
        x_alpha =  self.twothirds * (xa - 0.5*xb - 0.5*xc)/base*transfer
        x_beta  =  self.twothirds * (self.sqrtthree_two*xb - self.sqrtthree_two*xc)/base*transfer

        return np.stack([x_alpha, x_beta])
    
    def solver_elec(self, iteration, states_xn, uabc_xn, uabc_xn1):
        e_voltage_xn1 = self.ea_array[iteration]
        iabc1_xn    = states_xn[0:3]
        iabc2_xn    = states_xn[3:6]
        iabc3_xn    = states_xn[6:9]
        vabc_xn     = states_xn[9:12]
        vabc_c_xn   = states_xn[12:15]
        vabc_g_xn   = states_xn[15:18]
        vabc_cap_xn = states_xn[18:21]
        hist_lc = iabc1_xn + self.sim_step/(2*self.L1)*(uabc_xn - vabc_c_xn)
        hist_lg = iabc2_xn + self.sim_step/(2*self.L2)*(vabc_xn - vabc_g_xn)
        hist_cap = -iabc3_xn - (2*self.C3)/self.sim_step*(vabc_cap_xn)
        rhs_array = np.stack([self.sim_step/(2*self.L1)*uabc_xn1 + hist_lc, hist_lg, hist_cap, -hist_lg-e_voltage_xn1/self.R2])
        computed_voltages = np.linalg.solve(self.state_matrix, rhs_array)
        
        states_xn[9:12] = computed_voltages[0]
        states_xn[12:15] = computed_voltages[1]
        states_xn[15:18] = computed_voltages[2]
        states_xn[18:21] = computed_voltages[3]
        states_xn[0:3]  = self.sim_step/(2*self.L1)*(uabc_xn1-states_xn[12:15]) + hist_lc
        states_xn[3:6]  = self.sim_step/(2*self.L2)*(states_xn[9:12]-states_xn[15:18]) + hist_lg
        states_xn[6:9]  = (2*self.C3)/self.sim_step*(states_xn[18:21]) + hist_cap
        return states_xn
    
    def solver_control(self, iteration, states_xn, i2_elec, v_elec):
        S_base = self.setpoint_vehicle[iteration-1]
        S_next = self.setpoint_vehicle[iteration]
        valbe_xn1  = self.clarke_transformation_xabc(v_elec, self.V_base, self.peakLN_rmsLL)
        ialbe2_xn1 = self.clarke_transformation_xabc(i2_elec, self.I_base, self.peakLN_rmsLN)
        states_xn[0:2] = self.calculate_pll_solution(states_xn[0], states_xn[1], states_xn[9], valbe_xn1)
        vdq_xn1 = self.park_transformation_xabc(states_xn[1], valbe_xn1)
        idq2_xn1 = self.park_transformation_xabc(states_xn[1], ialbe2_xn1)
        states_control = self.compute_control(states_xn, S_base, S_next, vdq_xn1, idq2_xn1)
        states_xn[6:8] = valbe_xn1
        states_xn[8:10] = vdq_xn1
        states_xn[10:12] = ialbe2_xn1
        states_xn[12:14] = idq2_xn1
        states_xn[2:6] = states_control[:4]
        states_xn[14:18] = states_control[4:]        
        states_xn[18:21] = self.inverse_park_transformation_uabc(states_xn[1], states_control[6:8])
        return states_xn

    def compute_control(self, states_xn, S_base, S_next, vdq, idq2):
        P_base, V_base = S_base
        P_next, V_next = S_next
        vd, vq = vdq
        id, iq = idq2
        phi_p = states_xn[2] + self.ponder_trapz * (P_next - (vd*id+vq*iq) + P_base - (states_xn[8]*states_xn[12]+states_xn[9]*states_xn[13]))
        id_star = self.Kp_pco * (P_next - (vd*id+vq*iq)) + self.Ki_pco * phi_p
        phi_id = states_xn[4] + self.ponder_trapz * (id_star - id + states_xn[14] - states_xn[12])
        ud = self.Kp_cci * (id_star - id) + self.Ki_cci * phi_id

        phi_q = states_xn[3] + self.ponder_trapz * (np.sqrt(vd**2+vq**2) - V_next + np.sqrt(states_xn[8]**2+states_xn[9]**2) - V_base)
        iq_star = self.Kp_pco * (np.sqrt(vd**2+vq**2) - V_next) + self.Ki_pco * phi_q
        phi_iq = states_xn[5] + self.ponder_trapz * (iq_star - iq + states_xn[15] - states_xn[13])
        uq = self.Kp_cci * (iq_star - iq) + self.Ki_cci * phi_iq

        return np.stack([phi_p, phi_q, phi_id, phi_iq, id_star, iq_star, ud, uq])
    
    def load_initial_conditions(self):
        ini_conds = np.load(f"./sim_setups/init_sim.npz")
        states_elec = ini_conds["elec_states"]
        states_ctrl = ini_conds["ctrl_states"]
        self.elec_vars_plot[0, :] = states_elec
        self.control_vars_plot[0, :] = states_ctrl
        return states_elec, states_ctrl

    def run_algorithm(self):
        print("Simulation start")
        time_control = 0.
        self.state_matrix = self.create_state_matrix()
        state_iteration_elec, state_iteration_control = self.load_initial_conditions()
        state_prev_control = state_iteration_control[-3:]
        save_idx = 1
        for i in range(1, self.no_steps):
            state_iteration_elec = self.solver_elec(i, state_iteration_elec, state_prev_control, state_iteration_control[-3:])
            state_prev_control = state_iteration_control[-3:]
            start_timer = time.perf_counter()
            state_iteration_control = self.solver_control(i, state_iteration_control, state_iteration_elec[3:6], state_iteration_elec[9:12])
            state_iteration_control[1] %= 2*np.pi # clip theta_pll
            time_control += time.perf_counter() - start_timer
            if i % self.saving_it == 0:
                self.elec_vars_plot[save_idx, :] = state_iteration_elec[:]
                self.control_vars_plot[save_idx, :] = state_iteration_control[:]
                save_idx += 1
        # end_timer = time.time()
        self.compute_time = time_control
        print("Simulation end")
        print("Runtime", self.compute_time, " seconds")
        self.process_saved_data()

    def park_transfo_current_postprocess(self, theta, ia, ib, ic):
        id =  2/3 * (np.cos(theta)*ia + np.cos(theta-self.wfs_shift)*ib + np.cos(theta+self.wfs_shift)*ic)/self.I_base*self.peakLN_rmsLN
        iq =  -2/3 * (np.sin(theta)*ia + np.sin(theta-self.wfs_shift)*ib + np.sin(theta+self.wfs_shift)*ic)/self.I_base*self.peakLN_rmsLN

        return np.column_stack([id, iq])
    
    def park_transfo_voltage_postprocess(self, theta, va, vb, vc):
        id =  2/3 * (np.cos(theta)*va + np.cos(theta-self.wfs_shift)*vb + np.cos(theta+self.wfs_shift)*vc)/self.V_base*self.peakLN_rmsLL
        iq =  -2/3 * (np.sin(theta)*va + np.sin(theta-self.wfs_shift)*vb + np.sin(theta+self.wfs_shift)*vc)/self.V_base*self.peakLN_rmsLL

        return np.column_stack([id, iq])
    
    def compute_power_transfer(self, vd, vq, id, iq):
        P_trans = (id*vd + iq*vq) #* self.S_base # in pu
        Q_trans = (id*vq - iq*vd) #* self.S_base # in pu
        return np.column_stack([P_trans, Q_trans])
    
    def process_saved_data(self):
        self.ia1_array    = self.elec_vars_plot[:, 0:3]
        self.ia2_array    = self.elec_vars_plot[:, 3:6]
        self.ia3_array    = self.elec_vars_plot[:, 6:9]
        self.va_array     = self.elec_vars_plot[:, 9:12]
        self.va_cap_array = self.elec_vars_plot[:, 18:21]

        self.pll_vars_array = self.control_vars_plot[:, 0:2]
        self.phipq_pc_array = self.control_vars_plot[:, 2:4]
        self.phidq_cc_array = self.control_vars_plot[:, 4:6]
        self.valbe_array    = self.control_vars_plot[:, 6:8]
        self.vdq_array      = self.control_vars_plot[:, 8:10]
        self.ialbe_array    = self.control_vars_plot[:, 10:12]
        self.idq2_array     = self.control_vars_plot[:, 12:14]
        self.idq_star_array = self.control_vars_plot[:, 14:16]
        self.udq_array      = self.control_vars_plot[:, 16:18]
        self.ua_array       = self.control_vars_plot[:, 18:21]
    
    def compute_extra_arrays(self):
        self.idq1_array = self.park_transfo_current_postprocess(self.pll_vars_array[:, 1], self.ia1_array[:, 0], self.ia1_array[:, 1], self.ia1_array[:, 2])
        self.idq3_array = self.park_transfo_current_postprocess(self.pll_vars_array[:, 1], self.ia3_array[:, 0], self.ia3_array[:, 1], self.ia3_array[:, 2])
        self.S1_array = self.compute_power_transfer(self.vdq_array[:, 0], self.vdq_array[:, 1], self.idq1_array[:, 0], self.idq1_array[:, 1])
        self.S2_array = self.compute_power_transfer(self.vdq_array[:, 0], self.vdq_array[:, 1], self.idq2_array[:, 0], self.idq2_array[:, 1])
        self.S3_array = self.compute_power_transfer(self.vdq_array[:, 0], self.vdq_array[:, 1], self.idq3_array[:, 0], self.idq3_array[:, 1])
        self.w_pll_array = self.vdq_array[:, 1]*self.Kp_pll + self.pll_vars_array[:, 0]*self.Ki_pll + self.wN

    def save_arrays(self, file_name):
        metadata = {
                "step_size": self.sim_step,
                "sim_time": self.sim_time,
                "step_size_plot": self.sim_step_plot,
                "date": datetime.now(),
                "compute_time": self.compute_time
            }
        
        assert isinstance(self.time_array_plot, np.ndarray), f"Expected type numpy.ndarray, got {type(self.time_array)}"
        
        np.savez(
            f'./Saved_trajectories/Sim_100events/nn_{file_name}.npz',
            time=self.time_array_plot,
            ea=self.ea_array,
            va=self.va_array,
            ua=self.ua_array,
            va_cap=self.va_cap_array,
            ia1=self.ia1_array,
            ia2=self.ia2_array,
            ia3=self.ia3_array,
            udq=self.udq_array,
            pll_vars=self.pll_vars_array,
            phipq_pc=self.phipq_pc_array,
            phidq_cc=self.phidq_cc_array,
            valpha_beta=self.valbe_array,
            vdq=self.vdq_array,
            ialpha_beta=self.valbe_array,
            idq2=self.idq2_array,
            idq1=self.idq1_array,
            idq3=self.idq3_array,
            idq2_star=self.idq_star_array,
            S1=self.S1_array,
            S2=self.S2_array,
            S3=self.S3_array,
            Pref=self.Pref_plot,
            Vref=self.Vref_plot,
            w_pll=self.w_pll_array,
            metadata=metadata
        )

if __name__ == "__main__":

    sim_time = 120
    sim_step = 50e-6
    plot_step = 500e-6
    parameters_model = "params_pv_100events"

    simulator = EMT_simulator(sim_time, sim_step)
    simulator.upload_parameters(plot_step, parameters_model)
    simulator.init_neural_net("version1")

    simulator.run_algorithm()
    simulator.compute_extra_arrays()
    simulator.save_arrays("sim_1")
    show_plot = True

    if show_plot:

        plotter = Sim_Plotter()
        plotter_ones = np.ones_like(simulator.time_array_plot[:])
        y_plotting = [
                [(simulator.valbe_array[:, 0], r"$v_{\alpha}$", "darkgreen", "-"), (simulator.valbe_array[:, 1], r"$v_{\beta}$", "darkgreen", "-"), 
                 (plotter_ones*1.1, "", "black", "--"), (plotter_ones*(-1.1), "", "black", "--")],
                [(simulator.pll_vars_array[:, 0], r"$x_{1}$", "darkgreen", "-"), 
                 (plotter_ones*0.1, "", "black", "--"), (plotter_ones*(-0.1), "", "black", "--")],
                [(simulator.vdq_array[:, 1], r"$v_{q}$", "darkgreen", "-"), 
                 (plotter_ones*0.2, "", "black", "--"), (plotter_ones*(-0.2), "", "black", "--")],
                 [(simulator.pll_vars_array[:, 1], r"$\theta_{pll}$", "darkgreen", "-"), 
                 (plotter_ones*(2*np.pi+0.005), "", "black", "--"), (plotter_ones*(-0.005), "", "black", "--")],
                ]
        
        x_plotting = [simulator.time_array_plot.copy() for _ in range(len(y_plotting))]
        plotter.plot_arrays(x_plotting, y_plotting)