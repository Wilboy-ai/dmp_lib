from numpy import diff
import math

class dmp():

    def __init__(self, N, alpha=1, beta=1, tau=0.1):
        self.P = 0
        self.N = N
        self.Ci = []
        self.hi = []
        self.wi = []
        self.ft = []
        self.alpha = alpha
        self.beta = beta
        self.tau = tau
        self.alpha_x = -math.log(0.01)
        self._set_Ci()
        self._set_hi()

    # Define Ci center of gaussians
    def _set_Ci(self):
        for i in range(1, self.N+1):
            self.Ci.append(math.exp(-self.alpha_x * (i-1)/(self.N-1)))
    # Define hi variance for gaussians
    def _set_hi(self):
        for i in range(0, self.N-2):
            self.hi.append(1/pow((self.Ci[i+1] - self.Ci[i]),2))
        self.hi.append(1 / pow((self.Ci[self.N-1] - self.Ci[self.N-2]),2))

    # define basis function of gaussians
    def phi(self, x, i):
        return math.exp(-self.hi[i] * pow(x - self.Ci[i], 2))

    # Define x(t) the phase function x(0) = 1.0  converges to 0 when t = infinity
    def x(self, t):
        x0 = 1.0
        return x0 * math.exp(-self.alpha_x * (t/1))

    # get derivatives of 1D trajectory
    def _get_dT(self, T):
        self.P = len(T)

        dT = diff(T).tolist()
        dT.append(0)

        ddT = diff(dT)
        ddT = ddT.tolist()
        ddT.append(0)
        return dT, ddT

    # calculate the force targets
    def calc_ft(self, T):
        ft = []
        dT, ddT = self._get_dT(T)

        g = T[len(T) - 1]
        for i in range(0, len(T)):
            f_target = ddT[i] - (self.alpha * (self.beta * (g - T[i]) - dT[i]))
            ft.append(f_target)

        return ft

    # Calculate the weights for the gaussians
    def calc_w(self, y0, g, ft, P):

        deltaT = 1 / P
        S = []
        for t in range(0, P):
            S.append(self.x(deltaT*t) * (g - y0))

        for i in range(0, self.N-1):

            SGFT = []
            SGS = []

            for t in range(0, P):
                SGFT.append(S[t] * self.phi(self.x(deltaT*t), i) * ft[t])
                SGS.append(S[t] * self.phi(self.x(deltaT*t), i) * S[t])
            self.wi.append(sum(SGFT)/sum(SGS))

    # Forcing term function
    def fd(self, X, y0, g):
        suma = []
        sumb = []

        for i in range(0, self.N-1):
            suma.append(self.phi(X, i) * self.wi[i])
            sumb.append(self.phi(X, i))

        return sum(suma)/sum(sumb) * X * (g - y0)

    # Calculate the dmp trajectory w/ forcing term
    def _get_T(self, g, T0, P):
        Trajectory = []
        dT = 0
        T = T0

        deltaT = 1/P*2

        for i in range(0, P*2):
            ddT = (self.alpha * (self.beta * (g - T) - dT)) + self.fd(self.x(i*deltaT), T0, g)
            dT = dT + self.tau * ddT
            T = T + self.tau * dT
            Trajectory.append(T)


        return Trajectory





    def train_dmp(self, T):
        #self.Ci, self.hi = calc_gaus()
        #self.ft = calc_ft()
        #self.wi = calc_w(Ci, hi, ft)
        return 0







