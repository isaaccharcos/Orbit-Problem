import numpy as np
from OrbitObject import OrbitObject

def separation_study(reference_orbit, target_separation, nu_initial):
    # Study parameters
    delta_v_low = 0.0
    delta_v_high = 5.0
    tolerance = 0.01
    max_iterations = 100

    # Instantiate two satellites using reference orbit
    satellite1 = reference_orbit.copy()
    satellite2 = reference_orbit.copy()

    # Get time elapsed after one revolution
    time_elapsed = satellite1.get_period()

    # Bisection method to find delta_v corresponding to target separation after time_elapsed
    for iteration in range(max_iterations):
        delta_v = (delta_v_low + delta_v_high) / 2  # delta_v midpoint
        
        # Reset satellite2
        satellite2.reset(satellite1.a, satellite1.e, satellite1.mu)  # consider adding setter method uncoupled from these arguments to increase modularity

        # Apply delta-v to satellite2
        satellite2.apply_delta_v(delta_v, nu_initial)

        # Calculate true anomaly of satellite2 after time_elapsed
        nu2_final = satellite2.get_true_anomaly_after_time(time_elapsed, nu_0=nu_initial)
        
        # Get positions in Cartesian coordinates
        pos1 = satellite1.get_2D_position_vector(nu_initial)  # Same as nu1_final
        pos2 = satellite2.get_2D_position_vector(nu2_final)

        # Calculate separation distance
        separation = np.linalg.norm(pos1 - pos2)

        # Check if the separation is close enough to the target
        if abs(separation - target_separation) < tolerance:
            break  # Found the delta_v that gives the desired separation

        # Adjust the delta_v bounds for the next iteration
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

    # Create a reference orbit object
    reference_orbit = OrbitObject(a, e, MU_MOON)

    # Perform the separation study at periapsis
    target_separation = 10  # km
    nu_initial = 0  # rad
    delta_v, separation = separation_study(reference_orbit, target_separation, nu_initial)
    print(f"Required delta v to achieve separation distance of {target_separation} km: {delta_v:.4f} km/s")
    print(f"Separation distance achieved: {separation:.4f} km")
    print(f"Orbital period (satellite 1): {reference_orbit.get_period():.2f} seconds")

    # Perform the separation study at apoapsis
    target_separation = 10  # km
    nu_initial = np.pi  # rad
    delta_v, separation = separation_study(reference_orbit, target_separation, nu_initial)
    print(f"Required delta v to achieve separation distance of {target_separation} km: {delta_v:.4f} km/s")
    print(f"Separation distance achieved: {separation:.4f} km")
    print(f"Orbital period (satellite 1): {reference_orbit.get_period():.2f} seconds")
