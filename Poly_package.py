import numpy as np
from numpy.polynomial import Polynomial


def remove_duplicates(arr, h=1e-5):
    newarr=[]
    for el in arr:
        if not any(np.isclose(newarr,el,h)):
            newarr.append(el)
    return np.asarray(newarr)
def permut_to_str(permut):

    n=len(permut)
    if all(permut[i]==i for i in range(n)):
        return(r"$\sigma=\smathrm{id}$")
    free =[True for _ in range(n)]
    ans =r"$\sigma="
    def get_free():#if none free returns -1
        for i in range(n):
            if free[i]:return i
        return -1
    while True:
        i = get_free()
        if i==-1:break
        free[i]=False
        next = permut[i]
        if permut[i] !=i:
            ans+=rf'({i}'
            while next!=i:
                free[next]=False
                ans+=rf'\,{next}'
                next =permut[next]
            ans+= r')'
    return ans+r'$'

class Poly_package:
    Generator_roots = [  # noqa: RUF012
                        [(0,3),(3j,2),(-1-2j,1)],[(1+2j,1),(3j,1),(1,2),(4,2)],
                        [(10,2),(-10,2),(10j,2),(-10j,2)],
                        [(0,1),(1+1j,4),(1-1j,3),(-1+1j,2)],
                        [(3j+1,3),(0.8,1),(-0.8,2),(-3j,4)]]
    def get_polynomial(i):
        P= 1
        for (r,n) in Poly_package.Generator_roots[i]:
            for _ in range(n):
                P =P * Polynomial([-r, 1])
        return P
    def get_representation(i):
        ans = r"$"
        for (r,n) in Poly_package.Generator_roots[i]:
            if r==0:
                ans+="X"
            elif abs(r.real)==0.0:

                if r.imag>0:
                    ans+=f'(X-{r.imag}i)'
                else:
                    ans+=f'(X+{-r.imag}i)'

            elif abs(r.imag)==0:
                if r.real>0:
                    ans+=f'(X-{r.real})'
                else:
                    ans+=f'(X+{-r.real})'
            else:
                ans+=f'(X-{r})'
            if n>1:
                ans+=f'^{n}'
        return ans+"$"


    def __init__(self,i):
        i=i%len(self.Generator_roots)
        self.P=Poly_package.get_polynomial(i)
        self.representation =Poly_package.get_representation(i)
        V = self.P(self.P.deriv().roots())
        self.V=remove_duplicates(V)

        self.r=self.get_r()

        self.x0 = max(np.abs(self.V)) + 10*self.r

        self.E = (self.P-self.x0).roots()
    def get_r(self):
        if len(self.V)==1:
            return 1
        else: 
            return min([np.abs(self.V[i]-self.V[j]) for i in range(len(self.V))  for j in range(i+1,len(self.V))])/5
    def dist_all(self,a0,u):
        """retourne la distance de la demi droite a0 +tv à V sans a0, ou quelques fois r si cette distance >=r"""
        def dist_droite(a0,u,z):
            z -=a0
            if u == 0:
                raise ValueError("Cannot determine a direction from u = 0.")
            else:
                u = u/np.abs(u)
            scalar_prod = u*z.conj().real
            if scalar_prod <0:
                return 2*self.r
            else:
                return np.sqrt(np.abs(z)**2 - ((u*z.conj()).real )**2 )
        return min(dist_droite(a0,u,z) for z in self.V if z!=a0)
    def find_vantage_point(self,a0,z,N=10):
        """Retour l'argument d'un bon vantage point"""
        best_t, best_score = 0, 0
        for n in range(2,N+1):
            for k in range(n):
                x1= a0*np.exp(2j*np.pi*k/n)
                u = x1-z
                dist = self.dist_all(z,u)

                if dist >=self.r*2: 
                    return k/n
                if dist>= best_score:
                    best_t,best_score=k/n,dist
        return 2*np.pi*best_t
    def visite_multiple(self,instructions,t0=0,t1=1):
        path_segments = [] #tous def sur [0,1]
        waypoint =self.x0
        arg_shift =0
        for (i,nb) in instructions:
            if nb==0:continue
            point=self.V[i]
            theta_vantage = 2*np.pi*self.find_vantage_point(waypoint,point)

            vantage_point = waypoint*np.exp(1j*theta_vantage)

            if theta_vantage !=0:
                
                path_segments.append(lambda t,w=waypoint,theta=theta_vantage   : w*np.exp(1j*theta *t))
            
            u= vantage_point-point
            impact_point = point + self.r*u/np.abs(u)

            path_segments.append(lambda t,v=vantage_point,i=impact_point:v+ (i -v)*t)
            
            
            path_segments.append(lambda t,v=point,i=impact_point,n=nb: v + (i-v)* np.exp(2j*n*np.pi*t))
            path_segments.append(lambda t,v=vantage_point,i=impact_point:v+ (i -v)*(1-t))
            waypoint = vantage_point
            arg_shift += theta_vantage


        if waypoint != self.x0:

            path_segments.append( lambda t: self.x0*np.exp(1j*(arg_shift) *(1-t)))

        delta = (t1-t0)/len(path_segments)
        subdivision=[t0+k*delta for k in range(len(path_segments)+1)]
        def path(t):
            if t==1:
                return self.x0
            else:
                i = int(np.floor((t-t0)/delta))
            return path_segments[i]((t-subdivision[i])/delta)

        return path
    def get_permutation(self,gamma, t0=0.0, t1=1.0, N=1000):
        """
        Compute the permutation of the roots of P induced by the path gamma.

        Parameters
        ----------
        P : Polynomial
        gamma : callable
        E : np.ndarray
        t0 : float
            Start of interval for gamma.
        t1 : float
            End of interval for gamma.
        N : int
            Number of steps for solving the ODE.

        Returns
        -------
        permutation : np.ndarray
        """
        def get_closest_root(z):
            closest_index, closest_value = len(self.E), np.inf
            for i, root in enumerate(self.E):
                if np.abs(z - root) < closest_value:
                    closest_index, closest_value = i, np.abs(z - root)
            return closest_index

        permutation = np.zeros(len(self.E), dtype=int)
        for i, root in enumerate(self.E):
            z_values =solve_z (self.P.deriv(),get_derivative(gamma,t0,t1),root,t0,t1,N)[1]
            permutation[i]= get_closest_root(z_values[-1])
        return permutation

    def get_permut_representation(self,instructions):
        if all((a[1]==0) for a in instructions):
            return "id"
        return permut_to_str(self.get_permutation(self.visite_multiple(instructions)))
    def curves(self,path_instructions,start_index):
        """
        Takes:
            path instructions : list of (index of element in V,nb tours)
            start_index:index of element in E
        Returns:
            path_curve,t_values,lifted_curve
        """
        path = self.visite_multiple(path_instructions)
        path_curve = get_curve(path,N=1000)

        t_values, lifted_curve =solve_z (self.P.deriv(),get_derivative(path,0,1),self.E[start_index],N=1000)
        return path_curve,t_values,lifted_curve
        

def get_derivative(f, t0,t1,h=1e-5):
    """ Returns callable f' """
    def f_prime(t):
        a = max(t0, t - h)
        b = min(t1,t+h)
        return (f(b) - f(a)) / (b-a)
    return f_prime
def solve_z(P_prime, f_prime, z0, t0=0.0, t1=1.0, N=10000):

    """
    Solve the complex ODE:
        z'(t) = f'(t) / P'(z(t))
    using Runge-Kutta 4.

    Parameters
    ----------
    P_prime : callable
        Function P'(z) : complex -> complex
    f_prime : callable
        Function f'(t) : float -> complex
    z0 : complex
        Initial condition z(t0)
    t0 : float
        Start of interval
    t1 : float
        End of interval
    N : int
        Number of steps

    Returns
    -------
    t_values : np.ndarray
    z_values : np.ndarray (complex)
    """

    h = (t1 - t0) / N
    t_values = np.linspace(t0, t1, N+1)
    z_values = np.zeros(N+1, dtype=complex)

    z = z0
    z_values[0] = z

    for k in range(N):
        t = t_values[k]

        
        def F(t, z):
            return f_prime(t) / P_prime(z)

        k1 = F(t, z)
        k2 = F(t + h/2, z + h*k1/2)
        k3 = F(t + h/2, z + h*k2/2)
        k4 = F(t + h,   z + h*k3)

        z = z + h*(k1 + 2*k2 + 2*k3 + k4)/6
        z_values[k+1] = z

    return t_values, z_values


def get_curve(path,t0=0,t1=1,N=10000):
    return np.array([path(t) for t in np.linspace(t0,t1,N)])
