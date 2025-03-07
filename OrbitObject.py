import numpy as np
from scipy.optimize import fsolve

"""
Orbit object class intended to store, modify, and return orbital elements and parameters.

Assumptions:
- 2D Keplerian orbit
- Prograde tangential burn only at periapsis or apoapsis
"""

class OrbitObject:
    def __init__(self, a, e, mu):
        self.reset(a, e, mu)

    def reset(self, a, e, mu):
        self.a = a  # Semimajor axis
        self.e = e  # Eccentricity
        self.mu = mu # Gravitational parameter
        self.T = 2 * np.pi * np.sqrt(self.a**3 / mu)  # Orbital period
        self.rp = self.a * (1 - self.e)  # Periapsis radius
        self.ra = self.a * (1 + self.e)  # Apoapsis radius

    def copy(self):
        return OrbitObject(self.a, self.e, self.mu)
        
    def get_radius(self, nu):
        """
        Return radius at given true anomaly
        """
        r = self.a * (1 - self.e**2) / (1 + self.e * np.cos(nu))
        return r

    def get_speed(self, nu):
        """
        Return speed at given true anomaly
        """
        r = self.get_radius(nu)
        v = np.sqrt(self.mu * (2 / r - 1 / self.a))  # Vis-viva equation
        return v

    def get_escape_velocity(self, nu):
        """
        Return escape velocity at given true anomaly
        """
        r = self.get_radius(nu)
        v_esc = np.sqrt(2 * self.mu / r)
        return v_esc

    def get_period(self):
        """
        Return orbital period
        """
        return self.T

    def get_true_anomaly_after_time(self, t, nu_0=0):
        """
        Return true anomaly after time elapsed starting at given initial true anomaly
        """
        # Calculate initial eccentric anomaly
        E_0 = 2 * np.arctan(np.sqrt((1 - self.e) / (1 + self.e)) * np.tan(nu_0 / 2))
        
        # Calculate initial mean anomaly
        M_0 = E_0 - self.e * np.sin(E_0)
        
        # Propagate mean anomaly
        M_t = M_0 + 2 * np.pi * (t / self.T)
        
        # Solve for new eccentric anomaly
        def kepler_equation(E):
            return E - self.e * np.sin(E) - M_t
        E_initial_guess = M_t
        E_t = fsolve(kepler_equation, E_initial_guess)[0]

        # Calculate new true anomaly
        nu_t = 2 * np.arctan(np.sqrt((1 + self.e) / (1 - self.e)) * np.tan(E_t / 2))
        
        return nu_t

    def get_2D_position_vector(self, nu):
        """
        Return 2d position vector at given true anomaly
        """
        r = self.get_radius(nu)
        x = r * np.cos(nu)
        y = r * np.sin(nu)
        return np.array([x, y])

    def apply_delta_v(self, delta_v, nu):
        """
        Apply delta v at a given true anomaly and update member orbital elements
        NOTE: This funciton is currently only valid for periapsis and apoapsis burns
        TODO: Generalize for arbitrary true anomaly
        """
        # Assert burn is at periapsis or apoapsis
        assert abs(nu % np.pi) <= 1E-9, "Burn can only happen at periapsis or apoapsis."

        # Bound velocity between zero and escape velocity
        max_delta_v = self.get_escape_velocity(nu) - self.get_speed(nu)  # delta_v required to escape
        min_delta_v = -abs(self.get_speed(nu))
        assert delta_v < max_delta_v, f"delta v is greater than {max_delta_v:.4f} km/s resulting in escape."
        assert delta_v > min_delta_v, f"delta v is less than {min_delta_v:.4f} km/s resulting in zero speed."

        # Get current position and velocity at given true anomaly
        r = self.get_radius(nu)
        v_initial = self.get_speed(nu)

        # New velocity after applying delta v
        v_new = v_initial + delta_v

        # Calculate new semimajor axis
        a_new = 1 / (2 / r - v_new**2 / self.mu)

        # Calculate new eccentricity
        e_new = np.sqrt(max(0, 1 - ((r * v_new)**2) / (a_new * self.mu)))  # only valid for periapsis and apoapsis

        # Reinitialize with new elements
        self.reset(a_new, e_new, self.mu)
