import numpy as np
from OrbitObject import OrbitObject

"""
Script to determine minimum delta v required to achieve a specified separation distance after one revolution.

Assumptions:
- 2D Keplerian orbit
- Prograde tangential burn only at periapsis or apoapsis
"""

# Study parameters
STUDY_TOLERANCE = 0.001  # km
MAX_ITER = 100

def separation_study(reference_orbit, target_separation, nu_initial):
    """
    Use bisection method on delta_v using target_separation as passing criterion
    """

    # Instantiate two satellites using reference orbit
    satellite1 = reference_orbit.copy()
    satellite2 = reference_orbit.copy()

    # Get time elapsed after one revolution
    time_elapsed = satellite1.get_period()

    # Bisection method bounds
    delta_v_low = 0.0
    delta_v_high = reference_orbit.get_escape_velocity(nu_initial) - reference_orbit.get_speed(nu_initial)

    # Bisection method to find delta_v corresponding to target separation after time_elapsed
    for iteration in range(MAX_ITER):
        delta_v = (delta_v_low + delta_v_high) / 2  # delta_v midpoint
        
        # Reset satellite2
        satellite2.reset(satellite1.a, satellite1.e, satellite1.mu)  # TODO: consider adding setter method uncoupled from these arguments to increase modularity

        # Apply delta-v to satellite2
        satellite2.apply_delta_v(delta_v, nu_initial)

        # Calculate true anomaly of satellite2 after time_elapsed
        nu2_final = satellite2.get_true_anomaly_after_time(time_elapsed, nu_0=nu_initial)
        
        # Get positions in Cartesian coordinates
        pos1 = satellite1.get_2D_position_vector(nu_initial)  # Same as nu1_final
        pos2 = satellite2.get_2D_position_vector(nu2_final)

        # Calculate separation distance
        separation = np.linalg.norm(pos1 - pos2)

        # Check if separation within tolerance of target
        if abs(separation - target_separation) < STUDY_TOLERANCE:
            break  # Found the delta_v that gives the desired separation

        # Adjust delta_v bounds for next iteration
        if separation < target_separation:
            delta_v_low = delta_v
        else:
            delta_v_high = delta_v

    return delta_v, separation

# Constants
R_MOON = 1737.4  # Moon radius in km
MU_MOON = 4902.8  # Moon gravitational parameter in km^3/s^2

if __name__ == "__main__":
    h_periapsis = 100  # km
    h_apoapsis = 10000  # km
    r_periapsis = R_MOON + h_periapsis
    r_apoapsis = R_MOON + h_apoapsis

    a = (r_periapsis + r_apoapsis) / 2
    e = (r_apoapsis - r_periapsis) / (r_apoapsis + r_periapsis)

    # Create reference orbit object
    reference_orbit = OrbitObject(a, e, MU_MOON)

    # Perform separation study at periapsis
    target_separation = 10  # km
    nu_initial = 0  # rad
    delta_v, separation = separation_study(reference_orbit, target_separation, nu_initial)
    delta_v *= 1000
    print(f"Periapsis burn:")
    print(f"Required delta v to achieve separation distance of {target_separation} km: {delta_v:.4f} m/s")
    print(f"Separation distance achieved: {separation:.4f} km")
    print(f"")
  
    # Perform separation study at apoapsis
    target_separation = 10  # km
    nu_initial = np.pi  # rad
    delta_v, separation = separation_study(reference_orbit, target_separation, nu_initial)
    delta_v *= 1000
    print(f"Apoapsis burn:")
    print(f"Required delta v to achieve separation distance of {target_separation} km: {delta_v:.4f} m/s")
    print(f"Separation distance achieved: {separation:.4f} km")
    print(f"")
