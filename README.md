# Problem description
**1. The following exercise aims to discuss the orbital dynamic topic but also the
python implementation. When implementing the solution, please create scripts, functions and/or classes
as you see fit (favoring simplicity) as well as a few unit tests (pytest preferred).
If possible share the result in github.**

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
<img width="1059" alt="image" src="https://github.com/user-attachments/assets/7a72ad27-3c21-435e-a9a3-46117b1cbc89" />

Minimum delta v required to achieve desired separation occurs at periapsis. Burning at periapsis requires less fuel usage than burning at apoapsis. This is supported by unit test:

https://github.com/isaaccharcos/Orbit-Problem/blob/d0397dd34356b62cea967c4677c88287007ed1fa/test_separation_study.py#L36C1-L47C1

**2.1 Given the latitude/longitude of the landing site, what are the conditions imposed on the orbit when preparing to land?**

The orbit must have an inclination greater than or equal to the latitude of the landing site. This is because the ground track will only span the latitudes between -i and i. For example, an equatorial orbit cannot land on a pole.

**2.2 About the CR3BP: what is the most efficient method to move from a L1 Halo to a L2 Halo orbit?**

The most efficient method to move from a L1 Halo to an L2 Halo is to utilize a heteroclinic transfer between an L1 Halo unstable manifold and an L2 Halo stable manifold. Minimal delta v is required to perform course corrections if the manifolds do not already intersect.
