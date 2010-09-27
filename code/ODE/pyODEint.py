

"""
A general inderface for solving ODEs


"""

def linear_combination(*args):
    """
    Returns a linear combination of the arguements.
    
    >>>print bar(4, 'a', 2, 'b', 3,  'c', 6)
    aaaabbccc
    """
    
    if len(args)>1:
        R = args[1]*0
        for k in range(len(args)/2):
            R += args[k+k]*args[k+k+1]
        return R
    return None




class ode(object):
    """
    Solving y'(t) = RHS(t,y); y(t0) = y0
    
    parameters:
        RHS the right hand side of the equation
        t0 the initial point (start)
        y0 the initial condition
    
    """
    
    def __init__(self, **kwargs):
        """
        parameters:
        [rhs, solver, step_control, output, terminator]
        [step_size, stop]
        """
        
        self.rhs = None
        self.solver = None
        self.step_control = None
        self.output = None
        self.terminator = None
        
        self.step_size = 1.0
        self.stop = 1.0
        
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    def run(self, initial_condition ):
        """
        Solve the ode.
        
        initial_condition is a pair, (start, initial_value)
        
        """
        
        if self.terminator is None:
            self.terminator = fixedTerminator(self )
        
        t = initial_condition[0]
        y=None
        try:
            y = initial_condition[1].copy()
        except:
            y = initial_condition[1]
        
        dt = self.step_size
        
        if self.output is not None:
            self.output.output(t, y, start=True, end=False)
        
        continue_flag=True
        
        while continue_flag:
            #print x,y, dx
            
            if self.step_control is not None:
                dt = self.step_control.get_step_size(t, y)
            else:
                t = round((t-initial_condition[0])/dt)*dt + initial_condition[0]
            
            dt, continue_flag, kill_flag = self.terminator.terminate(t, y, dt)
            
            if kill_flag:
                break
            
            if not continue_flag and self.step_control is not None:
                self.step_control.set_step_size(dt, t, y)
            
            t, y = self.solver.step(self.rhs, t, dt, y )
            
            if self.output is not None:
                self.output.output(t, y, start=False, end=not continue_flag)
        
        return t, y
    
    def solve(self, initial_condition):
        return self.run(initial_condition)
    
    def __call__(self, initial_condition):
        return self.run(initial_condition )


class fixedTerminator:
    
    def __init__(self, ode_instance ):
        self.ode_instance = ode_instance
    
    def terminate(self, t, y, dt):
        if t+dt > self.ode_instance.stop:
            dt = self.ode_instance.stop-t
            return dt, False, False
        return dt, True, False


class RK4solver:
    
    def step(self, rhs, t, dt, y):
        
        K1 = rhs(t, y)
        K2 = rhs(t + dt/2.0, y+K1*(dt/2.0))
        K3 = rhs(t + dt/2.0, y+K2*(dt/2.0))
        K4 = rhs(t+dt, y+K3*dt)
        
        y += (K1/6.0 + K2/3.0 + K3/3.0 + K4/6.0)*dt
        t += dt
        
        return t, y


class DP54(ode):
    
    """
    solver:
    def step(self, rhs, t, dt, y):
        return t, y
    
    step_control:
    def get_step_size(self, t, y):
        return dt
    def set_step_size(self, dt):
    
    output:
    sef output(self, t, y, start=True, end=False)
    
    terminator:
    def terminate(t, y, dt):
        return dt, continue_flag, kill_flag
    
    """
    
    def __init__(self, **kwargs):
        super(DP54, self).__init__()
        self.solver = self
        self.step_control = self
        self.dt_next = self.step_size
        self.min_dt = 0.001
        self.max_dt = 1.0
        self.eps = 0.001
        self.debug = False
        
        self.norm = abs
        self.linear_combination = linear_combination
    
    
    def step(self, rhs, t, dt, y):
        
        dy = self.linear_combination( \
            self.K0, dt*5179.0/57600.0, \
            self.K2, dt*7571.0/16695.0, \
            self.K3, dt*393.0/640.0, \
            self.K4, -dt*92097.0/339200.0, \
            self.K5, dt*187.0/2100.0, \
            self.K6, dt*1.0/40.0 )
        
        return t+dt, y+dy
    
    
    def eval_rhs(self, t, y):
        
        self.K0 = self.rhs(t, y)
        temp = self.linear_combination( \
            y, 1.0,  self.K0, self.dt/5.0)
        self.K1 = self.rhs(t + self.dt/5.0, temp)
        
        temp = self.linear_combination( \
            y, 1.0, self.K0,  self.dt*3.0/40.0,  self.K1, self.dt*9.0/40.0)
        self.K2 = self.rhs(t + self.dt*3.0/10.0, temp)
        
        temp = self.linear_combination( \
            y, 1.0,  self.K0, self.dt*44.0/45.0, \
            self.K1, self.dt*56.0/15.0,  self.K2, self.dt*32.0/9.0 )
        self.K3 = self.rhs(t+ self.dt*4.0/5.0, temp)
        
        temp = self.linear_combination( \
            y, 1.0,  self.K0, self.dt*19372.0/6561.0, \
            self.K1, -self.dt*25360.0/2187.0,  self.K2, self.dt*64448.0/6561.0, \
            self.K3, -self.dt*212.0/729.0)
        self.K4 = self.rhs(t+ self.dt*8.0/9.0, temp)
        
        temp = self.linear_combination( \
            y, 1.0,  self.K0, self.dt*9017.0/3168.0,  self.K1, -self.dt*355.0/33.0, \
            self.K2, self.dt*46732.0/5247.0,  self.K3, self.dt*49.0/176.0, \
            self.K4, -self.dt*5103.0/18656.0)
        self.K5 = self.rhs(t+ self.dt, temp)
        
        temp = self.linear_combination( \
            y, 1.0,  self.K0, self.dt*35.0/384.0,  self.K2, self.dt*500.0/1113.0, \
            self.K3, self.dt*125.0/192.0,  self.K4, -self.dt*2187.0/6784.0, \
            self.K5, self.dt*11.0/84.0)
        self.K6 = self.rhs(t+ self.dt, temp)
    
    
    def get_step_size(self, t, y):
        
        self.dt = self.dt_next
        if self.dt < self.min_dt:
            self.dt = self.min_dt
        if self.dt > self.max_dt:
            self.dt = self.max_dt
        
        error = (self.eps+1)*2
        
        while error > self.eps:
            
            self.eval_rhs(t, y)
            
            temp = self.linear_combination( \
                (35.0/384.0-5179.0/57600.0), self.K0, \
                (500.0/1113.0-7571.0/16695.0), self.K2, \
                (125.0/192.0-393.0/640.0), self.K3, \
                (-2187.0/6784.0+92097.0/339200.0), self.K4, \
                (11.0/84.0-187.0/2100.0), self.K5, \
                (-1.0/40.0), self.K6 )
                
            mag = self.norm(temp)
            error = mag*self.dt
            
            if self.debug is True:
                print(t, self.dt)
            
            if error > self.eps:
                self.dt /= 2.0
                if self.dt < self.min_dt:
                    self.dt = self.min_dt
                    
                    self.eval_rhs(t, y)
                    
                    temp = self.linear_combination( \
                        (35.0/384.0-5179.0/57600.0), self.K0, \
                        (500.0/1113.0-7571.0/16695.0), self.K2, \
                        (125.0/192.0-393.0/640.0), self.K3, \
                        (-2187.0/6784.0+92097.0/339200.0), self.K4, \
                        (11.0/84.0-187.0/2100.0), self.K5, \
                        (-1.0/40.0), self.K6 )
                    
                    mag = self.norm(temp)
                    error = mag*self.dt
                    
                    if self.debug is True:
                        print(t, self.dt)
                    
                    break
        
        self.dt_next = 0.9*self.dt*abs(self.eps/mag)**0.25;
        
        return self.dt
    
    def set_step_size(self, dt, t, y):
        self.dt = dt
        self.next_dt = dt
        self.eval_rhs(t, y)
    
    
    def interpolate(self, y, phi):
        
        temp = self.linear_combination( \
            y, 1.0, 
			self.K0, self.dt*phi*(1.0+phi*(-1337.0/480.0+phi*(1039.0/360.0+phi*(-1163.0/1152.0)))), \
			self.K2, self.dt*100.0*phi*phi*(1054.0/9275.0+phi*(-4682.0/27825.0+phi*(379.0/5565.0)))/3.0, \
			self.K3, self.dt*-5.0*phi*phi*(27.0/40.0+phi*(-9.0/5.0+phi*(83.0/96.0)))/2.0, \
			self.K4, self.dt*18225.0*phi*phi*(-3.0/250.0+phi*(22.0/375.0+phi*(-37.0/600.0)))/848.0, \
			self.K5, self.dt*-22.0*phi*phi*(-3.0/10.0+phi*(29.0/30.0+phi*(-17.0/24.0)))/7.0 )
        
        return temp














# Unit Tests:

import unittest
import math




class TestSequenceFunctions(unittest.TestCase):
    
    
    def test_DP54(self):
        
        solver = DP54()
        solver.debug = True
        solver.step_size = 0.01
        solver.eps = 1E-5
        solver.min_dt = 1E-16
        solver.max_dt = 1
        solver.stop = 10.0
        solver.rhs = lambda t,y: -3.0*y + 6.0*t + 5.0
        
        t, y = solver.run((0.0,3.0))
        print y
    """
    def test_RK4solver_simple(self):
        foo = ode()
        foo.solver = RK4solver()
        foo.step_size = 0.01
        foo.stop = 10.0
        foo.rhs = lambda t,y: -3.0*y + 6.0*t + 5.0
        solution = lambda t: 2.0*math.exp(-3.0*t) + 2.0*t + 1.0
        
        xy = (0.0, 3.0)
        acc_err = 0
        acc_mag = 0
        
        while xy[0] < 10.0:
            foo.stop = xy[0] + 0.1
            xy = foo(xy)
            acc_err += abs(xy[1] - solution(xy[0]))
            acc_mag += abs(solution(xy[0]))
        
        err = acc_err/acc_mag
        self.assertTrue(err < 1E-9)
"""
        




if __name__ == '__main__':
    unittest.main()



