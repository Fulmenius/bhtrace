import torch
import torch.linalg as LA
from .spacetime import Spacetime


class MinkowskiCart(Spacetime):

    def __init__(self):
        pass

    def g(self, X):

        outp = torch.zeros([4, 4])

        outp[0, 0] = -1
        outp[1, 1] = 1
        outp[2, 2] = 1
        outp[3, 3] = 1

        return outp

    def ginv(self, X):

        outp = torch.zeros([4, 4])

        outp[0, 0] = -1
        outp[1, 1] = 1
        outp[2, 2] = 1
        outp[3, 3] = 1

        return outp

    def conn(self, X):

        pass


class KerrSchild(Spacetime):

    def __init__(self, a=0.6, m=1, Q=0):

        self.a = a
        self.a2 = a*a
        self.m = m
        self.Q = Q

        self.cr_r = 0.0


    def g(self, X):

        # X: [bm]
        # Kerr-Newman metric
        a = self.a
        a2 = self.a2
        m = self.m
        Q = self.Q

        p = X[1:]
        rho = p@p - a2
        r2 = 0.5*(rho + torch.sqrt(rho**2 + 4.0*a2*p[2]**2))
        r = torch.sqrt(r2)
        self.r = r
        r2a2 = r2 + a2

        k = torch.zeros(4)
        k[0] = 1
        k[1] = (r*p[0]+a*p[1])/r2a2
        k[2] = (r*p[1]-a*p[0])/r2a2
        k[3] = p[2]/r

        f = r2*(2.0*m*r - Q*Q)/(r2*r2+(a*p[2])**2)

        return f*torch.outer(k, k) + torch.diag(torch.Tensor([-1, 1, 1, 1]))


    def ginv(self, X):  

        return torch.inverse(self.g(X))


    def crit(self, X):

        p = X[1:]
        rho = p@p - a2
        r2 = 0.5*(rho + torch.sqrt(rho**2 + 4.0*a2*p[2]**2))
        r = torch.sqrt(r2)

        return r
        

    def conn(self, X):

        pass


class SchwSchild(Spacetime):

    def __init__(self, m=1.0, Q=0.0):

        self.a = a
        self.a2 = a*a
        self.m = m
        self.Q = Q
        self.Q2 = Q*Q

        self.cr_r = 0.0


    def g(self, X):

        m = self.m
        Q = self.Q

        p = X[1:]
        rho = p@p
        r2 = 0.5*(rho + torch.sqrt(rho**2))
        r = torch.sqrt(r2)
        self.r = r

        k = torch.zeros(4)
        k[0] = 1
        k[1] = p[0]/r
        k[2] = p[1]/r
        k[3] = p[2]/r

        f = (2.0*m/r - self.Q2/r2)

        return f*torch.outer(k, k) + torch.diag(torch.Tensor([-1, 1, 1, 1]))


    def ginv(self, X):  

        return torch.inverse(self.g(X))


    def crit(self, X):

        p = X[1:]
        rho = p@p - a2
        r2 = 0.5*(rho + torch.sqrt(rho**2 + 4.0*a2*p[2]**2))
        r = torch.sqrt(r2)

        return r
        

    def conn(self, X):

        pass



