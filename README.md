# Problem description
1. The following exercise aims to discuss the orbital dynamic topic but also the
python implementation. When implementing the solution, please create scripts, functions and/or classes
as you see fit (favoring simplicity) as well as a few unit tests (pytest preferred).
If possible share the result in github. 

```
# Let's try to model the separation of an in-orbit satellite.
# We can assume the deploying satellite doesn't alter its orbit after deployment,
# and the deployed satellite, at the instant of deployment,
# has the same position of the deploying one but an additional
# velocity of value DV along the velocity direction.
#
# What's the minimum DV needed to obtain a 10 km separation after one revolution?
# Is there any difference between deploying at periapsis or apoapsis?
# Explain the necessary simplifications to reach your results.
# The bodies are orbiting the Moon, in an initial orbit of hp=100 km, ha=10,000km.
 ```
**Result:**

<img width="517" alt="Screenshot 2025-03-07 at 10 37 33 PM" src="https://github.com/user-attachments/assets/9b8f1b59-50a9-45ce-9b3c-2b5890b91360" />

**2.1 Given the latitude/longitude of the landing site, what are the conditions imposed on the orbit when preparing to land?**

The orbit must have an inclination greater than or equal to the latitude of the landing site. This is because the ground track will only span the latitudes between -i and i. For example, an equatorial orbit cannot land on a pole.

2.2 About the CR3BP: what is the most efficient method to move from a L1 Halo to a L2 Halo orbit?
