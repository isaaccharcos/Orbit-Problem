import pytest
import numpy as np
from OrbitObject import OrbitObject
from separation_study import separation_study, STUDY_TOLERANCE

"""
Unit test script of separation study function.
"""

# Constants
R_MOON = 1737.4  # Moon radius in km
MU_MOON = 4902.8  # Moon gravitational parameter in km^3/s^2

@pytest.fixture
def orbit():
    # Initialize same orbit as in the problem
    h_periapsis = 100  # km
    h_apoapsis = 10000  # km
    r_periapsis = R_MOON + h_periapsis
    r_apoapsis = R_MOON + h_apoapsis

    a = (r_periapsis + r_apoapsis) / 2
    e = (r_apoapsis - r_periapsis) / (r_apoapsis + r_periapsis)

    return OrbitObject(a, e, MU_MOON)

def test_achieved_separation(orbit):
    target_separation = 10  # km
    nu_initial = 0  # rad
    # Test various orbits
    for e in np.linspace(0.0,0.99,10):
        orbit.e = e
        _, separation = separation_study(orbit, target_separation, nu_initial)
        assert np.isclose(separation, target_separation, STUDY_TOLERANCE)

# More of a hypothesis test than an implementation test
def test_achieved_delta_v(orbit):
    target_separation = 10  # km
    nu_initial_periapsis = 0  # rad
    nu_initial_apoapsis = np.pi  # rad
    # Test various orbits
    for e in np.linspace(0.1,0.99,100):
        orbit.e = e
        delta_v_periapsis, _ = separation_study(orbit, target_separation, nu_initial_periapsis)
        delta_v_apoapsis, _ = separation_study(orbit, target_separation, nu_initial_apoapsis)
        assert delta_v_apoapsis > delta_v_periapsis

if __name__ == "__main__":
    pytest.main()
