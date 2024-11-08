import torch
import os
import pickle

from ..geometry import Spacetime, Particle
from ..functional import RKF23


class PTracer():

    def __init__(self, r_max=40, e_tol=0.1, method='irk2'):

        self.solv = 'PTracer'
        self.m_param = None
        self.s_param = {'':}

        self.Ni = 0
        self.Nt = 0
        self.t = 0

        self.X = None
        self.P = None
        self.X0 = None
        self.P0 = None
        self.r_max = r_max
        self.e_tol = e_tol

        if method=='rkf23b':
            self.ode = RKF23()
        elif method=='rkf45':
            self.ode = None
        else:
            'O'
    
        pass


    def particle_set(self, particle: Particle):
        '''
        Attach class of particles to be traced

        ## Input:
        particle: Particle        
        '''

        self.particle = particle
        self.spc = particle.spacetime
        

    def evnt_check(self, X, P):

        fwd0 = torch.greater(abs(self.spc.r-self.spc.cr_r), self.e_tol)
        fwd1 = torch.less(self.spc.r, self.r_max)
        fwd2 = torch.all(torch.less(abs(P[1:]), 3))

        return fwd0*fwd1*fwd2


    def evnt(self, t, XP):

        cr1 = self.particle.crit(XP[:4], XP[4:])
        cr2 = torch.heaviside(self.r_max-XP[1], torch.Tensor([0.0]))

        return cr1*cr2
    

    def __term__(self, t, XP):
    
        dX = self.spc.ginv(XP[:4]) @ XP[4: ]
        dP = - self.particle.dHmlt(XP[:4], XP[4: ], self.eps)


        return torch.cat((dX, dP))


    def trace(self, X0, P0, eps=1e-3, nsteps=128, T=40):
        '''
        
        '''
        self.X0 = X0
        self.P0 = P0
        self.Nt = nsteps
        self.Ni = X0.shape[0]
        self.eps = eps

        self.X = torch.zeros(nsteps, self.Ni, 4)
        self.P = torch.zeros(nsteps, self.Ni, 4)

        self.X[0, :, :] = X0
        self.P[0, :, :] = P0

        T0 = torch.Tensor([0.0])

        for n in range(self.Ni):

            # X, P = X0[n, :], P0[n, :]

            # for i in range(nsteps-1):

            #     X, P = self.__step__(X, P, dt=dt, eps=eps)

            #     if self.evnt_check(X, P):
            #         self.X[i+1, n, :] = X
            #         self.P[i+1, n, :] = P
            #     else:
            #         self.X[i+1, n:, :] = X
            #         self.P[i+1, n:, :] = P
            #         break

            XP0 = torch.cat((X0[n], P0[n]))

            event_t, sol = odeint(
                self.__term__, 
                XP0, 
                T0, 
                # event_fn=self.evnt,
                atol=1e-6,
                rtol=1e-6,
                method="adaptive_heun"
                )

            self.X


        return self.X, self.P
