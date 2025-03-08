import pytest
import numpy as np
from OrbitObject import OrbitObject

"""
Unit test script of methods in OrbitObject class.
"""

# Constants
R_MOON = 1737.4  # Moon radius in km
MU_MOON = 4902.8  # Moon gravitational parameter in km^3/s^2

@pytest.fixture
def orbit():
    return OrbitObject(a=10000, e=0.1, mu=MU_MOON)

def test_orbit_initialization(orbit):
    assert orbit.a == 10000
    assert orbit.e == 0.1
    assert orbit.mu == MU_MOON
    assert np.isclose(orbit.T, 2 * np.pi * np.sqrt(10000**3 / MU_MOON))
    assert np.isclose(orbit.rp, 10000 * (1 - 0.1))
    assert np.isclose(orbit.ra, 10000 * (1 + 0.1))

def test_get_radius(orbit):
    nu = np.radians(0)  # Periapsis
    assert np.isclose(orbit.get_radius(nu), orbit.rp)
    
    nu = np.radians(180)  # Apoapsis
    assert np.isclose(orbit.get_radius(nu), orbit.ra)

def test_get_speed(orbit):
    nu = np.radians(0)  # Periapsis
    v = orbit.get_speed(nu)
    expected_v = np.sqrt(MU_MOON * (2 / orbit.rp - 1 / orbit.a))
    assert np.isclose(v, expected_v)

def test_get_escape_velocity(orbit):
    nu = np.radians(0)  # Periapsis
    v_esc = orbit.get_escape_velocity(nu)
    expected_v_esc = np.sqrt(2 * orbit.mu / orbit.rp)
    assert np.isclose(v_esc, expected_v_esc)

def test_apply_delta_v(orbit):
    nu = np.radians(0)  # Periapsis
    delta_v = 0.125  # Valid delta_v
    orbit.apply_delta_v(delta_v, nu)
    
    assert orbit.a != 10000  # Semimajor axis should change
    assert orbit.e >= 0  # Eccentricity should be valid

def test_apply_delta_v_too_big(orbit):
    nu = np.radians(0)  # Periapsis
    delta_v = orbit.get_escape_velocity(nu) - orbit.get_speed(nu) + 1  # Exceeding escape velocity
    with pytest.raises(AssertionError, match="delta v is greater than"):
        orbit.apply_delta_v(delta_v, nu)

def test_apply_delta_v_too_small(orbit):
    nu = np.radians(0)  # Periapsis
    delta_v = -abs(orbit.get_speed(nu)) - 1  # Reducing speed to below zero
    with pytest.raises(AssertionError, match="delta v is less than"):
        orbit.apply_delta_v(delta_v, nu)

def test_apply_delta_v_wrong_nu(orbit):
    nu = np.radians(90)  # Non periapsis/apoapsis point
    delta_v = 0.125 # Valid delta_v
    with pytest.raises(AssertionError, match="Burn can only happen"):
        orbit.apply_delta_v(delta_v, nu)

def test_get_2D_position_vector(orbit):
    nu = np.radians(0)  # Periapsis
    position = orbit.get_2D_position_vector(nu)
    r = orbit.get_radius(nu)
    expected_position = np.array([r, 0])
    assert np.allclose(position, expected_position)

def test_get_true_anomaly_after_time(orbit):
    nu_0 = np.radians(0)  # Periapsis
    t = orbit.T / 2  # Half period
    nu_t = orbit.get_true_anomaly_after_time(t, nu_0)
    expected_nu_t = np.pi  # Apoapsis
    assert np.isclose(nu_t, expected_nu_t, atol=1e-2)

if __name__ == "__main__":
    pytest.main()
