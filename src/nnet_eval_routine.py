import numpy as np

class explicit_inference_f():
    def __init__(self, model_name, step_size_sim):

        params_model = np.load(model_name+".npz")

        self.step = step_size_sim
        self.Scaler  = params_model["scaler"].reshape(-1)
        self.Shifter = params_model["shifter"].reshape(-1)
        if "W2_in" in params_model:
            self.W1 = params_model["W1"]
            self.B1 = params_model["B1"].reshape(-1)
            self.W2_in  = params_model["W2_in"]
            self.B2_in  = params_model["B2_in"].reshape(-1)
            self.W2_out = params_model["W2_out"]
            self.B2_out = params_model["B2_out"].reshape(-1)
            self.W3 = params_model["W3"]
            self.B3 = params_model["B3"].reshape(-1)
            self.no_neurons = self.B1.shape[0]

            self.run = self.inference_manual_deeper
            
            self.a1 = np.empty(self.no_neurons, dtype=np.float64)
            self.z2 = np.empty(self.no_neurons, dtype=np.float64)
            self.a2 = np.empty(self.no_neurons, dtype=np.float64)

        else:
            self.W1 = params_model["W1"]
            self.B1 = params_model["B1"].reshape(-1)
            self.W2 = params_model["W2"]
            self.B2 = params_model["B2"].reshape(-1)
            self.no_neurons = self.B1.shape[0]

            self.run = self.inference_manual_basic

            self.a1 = np.empty(self.no_neurons, dtype=np.float64)

        self.W1eff = self.W1 * self.Scaler.T
        self.B1eff = self.W1 @ self.Shifter + self.B1
        self.preds = np.empty(2, dtype=np.float64)
        self.y_out = np.empty(2, dtype=np.float64)

    def inference_manual_deeper(self, x_raw):
        a1 = self.a1
        z2 = self.z2
        a2 = self.a2
        preds = self.preds
        y_out = self.y_out

        np.dot(self.W1eff, x_raw, out=a1)
        a1 += self.B1eff
        np.tanh(a1, out=a1)

        np.dot(self.W2_in, a1, out=z2)
        z2 += self.B2_in
        np.tanh(z2, out=z2)

        np.dot(self.W2_out, z2, out=a2)
        a2 += self.B2_out
        a2 += a1
        np.tanh(a2, out=a2)

        np.dot(self.W3, a2, out=preds)
        preds += self.B3

        y_out[0] = preds[0] * self.step + x_raw[0]
        y_out[1] = preds[1] * self.step + x_raw[1]

        return y_out
    
    def inference_manual_basic(self, x_raw):
        a1 = self.a1
        preds = self.preds
        y_out = self.y_out

        np.dot(self.W1eff, x_raw, out=a1)
        a1 += self.B1eff
        np.tanh(a1, out=a1)

        np.dot(self.W2, a1, out=preds)
        preds += self.B2

        y_out[0] = preds[0] * self.step + x_raw[0]
        y_out[1] = preds[1] * self.step + x_raw[1]

        return y_out
