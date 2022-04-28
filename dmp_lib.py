from numpy import diff
import math



class dmp():

    def __init__(self, N, alpha=1, beta=1, tau=0.1):
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

    def _set_Ci(self):
        for i in range(1, self.N+1):
            self.Ci.append(math.exp(-self.alpha_x * (i-1)/(self.N-1)))

    def _set_hi(self):
        for i in range(0, self.N-2):
            self.hi.append(1/pow((self.Ci[i+1] - self.Ci[i]),2))
        self.hi.append(1 / pow((self.Ci[self.N-1] - self.Ci[self.N-2]),2))


    def _get_dT(self, T):
        dT = diff(T).tolist()
        dT.append(0)

        ddT = diff(dT)
        ddT = ddT.tolist()
        ddT.append(0)
        return dT, ddT


    def phi(self, x, i):
        return math.exp(-self.hi[i] * pow(x - self.Ci[i], 2))

    def x(self, t):
        x0 = 1.0
        return x0 * math.exp(-self.alpha_x * t/self.tau)

    def fd(self, x, y0, g):
        suma = []
        sumb = []

        for i in range(0, self.N-1):
            suma.append(self.phi(self.x(i), i) * self.wi[i])
            sumb.append(self.phi(self.x(i), i))

        return sum(suma)/sum(sumb) * x * (g - y0)

    def calc_ft(self, T):
        ft = []
        dT, ddT = self._get_dT(T)

        g = T[len(T)-1]
        for i in range(0, len(T)):
            f_target = ddT[i] - (self.alpha * (self.beta * (g - T[i]) - dT[i]))
            ft.append(f_target)
        return ft

    def _get_T(self, g, T0, P):
        Trajectory = []
        dT = 0
        T = T0

        for i in range(0, P):
            ddT = (self.alpha * (self.beta * (g - T) - dT)) + self.fd(self.x(i), T0, g)
            dT = dT + self.tau * ddT
            T = T + self.tau * dT
            Trajectory.append(T)

        return Trajectory




    def calc_w(self, y0, g, ft, P):

        S = []
        for t in range(0, P):
            S.append(self.x(t) * (g - y0))

        for i in range(0, self.N-1):

            SGFT = []
            SGS = []
            for t in range(0, P):
                SGFT.append(S[t] * self.phi(self.x(t), i) * ft[t])
                SGS.append(S[t] * self.phi(self.x(t), i) * S[t])

            #print(sum(SGFT)/sum(SGS))
            self.wi.append(sum(SGFT)/sum(SGS))



    def train_dmp(self, T):
        #self.Ci, self.hi = calc_gaus()
        #self.ft = calc_ft()
        #self.wi = calc_w(Ci, hi, ft)
        return 0







