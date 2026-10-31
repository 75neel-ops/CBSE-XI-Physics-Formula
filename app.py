"""
CBSE Class XI Physics (NCERT) - Learning Game  (Streamlit version)
Created by NilanjanC

Part 1: Key words of each chapter
Part 2: Chapter-wise practice questions (1, 2, 3 and 5 marks) with answers
Part 3: AI question generator (uses Gemini; the key is read from Streamlit Secrets)

All built-in questions are original practice material written to follow the NCERT
(rationalised) Class XI Physics syllabus - they are not copied from the book.
"""
import json
import os
import random
import time

import requests
import streamlit as st

AUTHOR = "NilanjanC"

CHAPTERS = {
    1: {
        "name": "Units and Measurements",
        "keywords": [
            ("SI system", "International system of units with 7 base units: metre, kilogram, second, ampere, kelvin, mole, candela."),
            ("Base and derived units", "Base units are independent; derived units are combinations of them (e.g. newton = kg m s^-2)."),
            ("Dimensions", "Powers to which base quantities are raised to represent a physical quantity, e.g. force = [M L T^-2]."),
            ("Dimensional analysis", "Method to check homogeneity of equations, convert units and derive relations."),
            ("Significant figures", "Reliable digits of a measurement plus the first uncertain digit."),
            ("Accuracy and precision", "Accuracy: closeness to the true value. Precision: closeness of repeated readings to each other."),
            ("Errors", "Absolute error = |measured - true|; relative error = absolute / true; percentage error = relative x 100."),
            ("Least count", "Smallest value an instrument can measure (vernier: 1 MSD - 1 VSD; screw gauge: pitch / divisions)."),
            ("Order of magnitude", "Power of ten nearest to a number (e.g. 4.5 x 10^3 is of order 10^3)."),
        ],
        "practice": [
            (1, "Write the dimensional formula of force.", "[M L T^-2]."),
            (1, "How many significant figures are in 0.007020?", "Four (7, 0, 2, 0)."),
            (1, "Which is more accurate: a measurement 5.00 cm or 5 cm?", "5.00 cm, since it has more significant figures and so a smaller uncertainty."),
            (2, "Check the dimensional correctness of v = u + at.", "[v] = [u] = [at] = [L T^-1]. All terms have the same dimensions, so the equation is dimensionally correct."),
            (2, "The side of a cube is measured with a 2 % error. Find the percentage error in its volume.", "V = a^3, so percentage error = 3 x 2 = 6 %."),
            (2, "Distinguish between accuracy and precision.", "Accuracy tells how close a reading is to the true value; precision tells how close repeated readings are to one another. Readings can be precise but not accurate."),
            (3, "Find the dimensional formula of Planck's constant h using E = h x frequency.", "[h] = [E] / [frequency] = [M L^2 T^-2] / [T^-1] = [M L^2 T^-1]."),
            (3, "Using dimensional analysis, derive the period T of a simple pendulum in terms of l, g and m.", "Let T = k l^a g^b m^c. Dimensions: T = L^a (L T^-2)^b M^c. So c = 0, -2b = 1 gives b = -1/2, and a + b = 0 gives a = 1/2. Thus T = k sqrt(l / g)."),
            (3, "State three limitations of dimensional analysis.", "(1) It cannot give dimensionless constants (like 2 pi or 1/2). (2) It cannot be used for trigonometric, exponential or logarithmic functions. (3) It cannot decide between quantities with the same dimensions, and it fails when a quantity depends on a sum of terms."),
            (3, "Add 12.5 cm and 3.76 cm and report the answer with the correct number of significant figures.", "12.5 + 3.76 = 16.26. In addition, round to the least number of decimal places (one), so the answer is 16.3 cm."),
        ],
    },
    2: {
        "name": "Motion in a Straight Line",
        "keywords": [
            ("Displacement", "Shortest change in position of a body; a vector."),
            ("Average and instantaneous velocity", "Average = total displacement / time. Instantaneous = limit of x/t as t tends to 0, i.e. dx/dt."),
            ("Acceleration", "Rate of change of velocity: a = dv/dt."),
            ("Equations of motion", "For constant acceleration: v = u + at, s = ut + (1/2)at^2, v^2 = u^2 + 2as."),
            ("Position-time graph", "Slope gives velocity."),
            ("Velocity-time graph", "Slope gives acceleration; area under the graph gives displacement."),
            ("Relative velocity", "Velocity of A with respect to B: vAB = vA - vB."),
            ("Free fall", "Motion under gravity alone with a = g (9.8 m/s^2) downwards."),
            ("Uniform motion", "Equal displacements in equal time intervals; acceleration is zero."),
        ],
        "practice": [
            (1, "What does the slope of a position-time graph represent?", "The velocity of the body."),
            (1, "Can the average speed of a body be zero in a finite time interval?", "No. Speed is the total path length divided by time, so it is zero only if the body does not move."),
            (2, "A car covers the first half of a distance at 40 km/h and the second half at 60 km/h. Find the average speed.", "Average speed = 2 v1 v2 / (v1 + v2) = 2 x 40 x 60 / 100 = 48 km/h."),
            (2, "A ball is thrown vertically upward at 20 m/s (g = 10 m/s^2). Find the maximum height and time of flight.", "H = u^2 / 2g = 400 / 20 = 20 m. Time of flight = 2u/g = 4 s."),
            (2, "Distinguish between distance and displacement.", "Distance is the length of the actual path (scalar, never negative). Displacement is the shortest straight-line change in position (vector, can be zero or negative)."),
            (3, "Derive s = ut + (1/2) a t^2 using a velocity-time graph.", "The v-t graph is a straight line from u to v = u + at. Area under it = rectangle (u x t) + triangle ((1/2) x t x at) = ut + (1/2) a t^2, which equals the displacement s."),
            (3, "A body starts from rest and accelerates at 2 m/s^2 for 5 s, then moves uniformly for 10 s, then decelerates uniformly to rest in 4 s. Find the total distance.", "Phase 1: v = 10 m/s, s1 = (1/2)(2)(25) = 25 m. Phase 2: s2 = 10 x 10 = 100 m. Phase 3: s3 = (10/2) x 4 = 20 m. Total = 145 m."),
            (3, "A stone is dropped from the top of an 80 m tower (g = 10 m/s^2). Find the time to reach the ground and the final speed.", "80 = (1/2)(10)t^2 gives t = 4 s. v = gt = 40 m/s."),
            (3, "Car A moves at 20 m/s and car B at 15 m/s in the same direction; A is 100 m behind B. When does A overtake B?", "Relative speed = 20 - 15 = 5 m/s. Time = 100 / 5 = 20 s."),
            (5, "Derive the three equations of motion for uniform acceleration using the velocity-time graph.", "Let velocity change from u to v in time t. (1) Slope = a = (v - u)/t, so v = u + at. (2) Area under the graph = ut + (1/2)(v - u)t, so s = ut + (1/2)at^2. (3) Area as a trapezium = (u + v)t/2 = (u + v)(v - u)/2a, so v^2 = u^2 + 2as."),
        ],
    },
    3: {
        "name": "Motion in a Plane",
        "keywords": [
            ("Scalar and vector", "A scalar has only magnitude; a vector has magnitude and direction."),
            ("Triangle and parallelogram law", "Resultant R = sqrt(A^2 + B^2 + 2AB cos theta)."),
            ("Resolution of vectors", "A vector splits into components A cos theta and A sin theta."),
            ("Unit vector", "A vector of magnitude 1 giving direction: A-hat = A / |A|."),
            ("Projectile motion", "Motion under gravity with horizontal velocity constant and vertical motion uniformly accelerated."),
            ("Range, height, time of flight", "R = u^2 sin2theta / g; H = u^2 sin^2 theta / 2g; T = 2u sin theta / g."),
            ("Relative velocity in a plane", "vAB = vA - vB (vector subtraction)."),
            ("Uniform circular motion", "Motion in a circle at constant speed; velocity direction changes continuously."),
            ("Centripetal acceleration", "a = v^2 / r = omega^2 r, directed towards the centre."),
        ],
        "practice": [
            (1, "Define a unit vector.", "A vector of magnitude one that points in the direction of a given vector."),
            (1, "Write the expression for the horizontal range of a projectile.", "R = u^2 sin 2 theta / g."),
            (2, "Two forces of 3 N and 4 N act at right angles. Find the resultant and its direction.", "R = sqrt(9 + 16) = 5 N. tan(alpha) = 4/3, so alpha = 53 degrees with the 3 N force."),
            (2, "Show that the range of a projectile is maximum at 45 degrees.", "R = u^2 sin 2 theta / g is maximum when sin 2 theta = 1, i.e. 2 theta = 90 degrees, so theta = 45 degrees."),
            (2, "Find the centripetal acceleration of a particle moving at 4 m/s in a circle of radius 2 m.", "a = v^2 / r = 16 / 2 = 8 m/s^2 towards the centre."),
            (3, "Derive the equation of the trajectory of a projectile.", "x = (u cos theta) t and y = (u sin theta) t - (1/2) g t^2. Eliminating t: y = x tan theta - g x^2 / (2 u^2 cos^2 theta), which is a parabola."),
            (3, "A projectile is fired at 30 degrees with speed 40 m/s (g = 10 m/s^2). Find maximum height, time of flight and range.", "H = u^2 sin^2 theta / 2g = 1600 x 0.25 / 20 = 20 m. T = 2u sin theta / g = 4 s. R = u^2 sin 2 theta / g = 1600 x 0.866 / 10 = 138.6 m."),
            (3, "Show that projection angles theta and (90 - theta) give the same range.", "R(90 - theta) = u^2 sin(180 - 2 theta) / g = u^2 sin 2 theta / g = R(theta)."),
            (3, "A swimmer can swim at 5 km/h in still water and wants to cross a river flowing at 3 km/h by the shortest path. In what direction should he swim and what is his effective speed?", "He must aim upstream at angle theta with the perpendicular such that sin theta = 3/5, so theta = 37 degrees. Effective speed across = sqrt(25 - 9) = 4 km/h."),
        ],
    },
    4: {
        "name": "Laws of Motion",
        "keywords": [
            ("Inertia", "Tendency of a body to resist a change in its state of rest or motion."),
            ("Newton's first law", "A body stays at rest or in uniform motion unless acted on by an external force."),
            ("Momentum", "p = mv; Newton's second law: F = dp/dt = ma."),
            ("Newton's third law", "To every action there is an equal and opposite reaction (acting on different bodies)."),
            ("Impulse", "J = F x t = change in momentum; unit N s."),
            ("Conservation of momentum", "Total momentum of an isolated system stays constant."),
            ("Friction", "Force opposing relative motion: static, kinetic and rolling; f = mu N."),
            ("Angle of repose", "Maximum angle of an incline at which a body just stays at rest: tan(theta) = mu."),
            ("Centripetal force", "Net force toward the centre in circular motion: F = mv^2 / r."),
            ("Banking of roads", "Tilting the road so that v^2 = r g tan(theta) with no need for friction."),
        ],
        "practice": [
            (1, "State Newton's first law of motion.", "Every body continues in its state of rest or of uniform motion in a straight line unless a net external force acts on it."),
            (1, "Define impulse and give its SI unit.", "Impulse is the product of force and the time for which it acts (equal to the change in momentum). SI unit: N s."),
            (2, "A 5 kg body at rest is acted on by a 20 N force. Find its acceleration and velocity after 3 s.", "a = F/m = 4 m/s^2. v = at = 12 m/s."),
            (2, "Why does a passenger lurch forward when a moving bus stops suddenly?", "Due to inertia of motion: the lower part of the body stops with the bus but the upper part tends to keep moving forward."),
            (2, "Define angle of repose and relate it to the coefficient of friction.", "It is the angle of an inclined plane at which a body placed on it just begins to slide. tan(theta) = mu."),
            (3, "Prove the law of conservation of momentum using Newton's laws.", "For two colliding bodies, F12 = -F21 (third law). Thus dp1/dt = -dp2/dt, so d(p1 + p2)/dt = 0, i.e. total momentum is constant."),
            (3, "A gun of mass 3 kg fires a 30 g bullet at 500 m/s. Find the recoil speed of the gun.", "0 = (0.03)(500) - 3 V, so V = 15 / 3 = 5 m/s opposite to the bullet."),
            (3, "A 10 kg block lies on a rough floor with mu = 0.3 (g = 10 m/s^2). Find the force needed to just move it, and the acceleration under a 40 N force.", "Limiting friction = 0.3 x 100 = 30 N. With 40 N: a = (40 - 30)/10 = 1 m/s^2."),
            (3, "Find the maximum safe speed of a car on a level circular road of radius 50 m with mu = 0.5 (g = 10 m/s^2).", "v = sqrt(mu r g) = sqrt(0.5 x 50 x 10) = sqrt(250) = 15.8 m/s."),
            (3, "A 60 kg person stands in a lift. Find the apparent weight when the lift accelerates up at 2 m/s^2, down at 2 m/s^2, and in free fall (g = 10 m/s^2).", "Up: m(g + a) = 60 x 12 = 720 N. Down: m(g - a) = 60 x 8 = 480 N. Free fall: 0 (weightlessness)."),
        ],
    },
    5: {
        "name": "Work, Energy and Power",
        "keywords": [
            ("Work", "W = F d cos(theta); a scalar; unit joule."),
            ("Kinetic energy", "K = (1/2) m v^2."),
            ("Work-energy theorem", "Net work done equals the change in kinetic energy."),
            ("Potential energy", "Gravitational: mgh; elastic: (1/2) k x^2."),
            ("Conservative force", "Work done depends only on end points, not the path (gravity, spring)."),
            ("Conservation of mechanical energy", "For conservative forces, kinetic + potential energy is constant."),
            ("Power", "Rate of doing work: P = W/t = F.v; unit watt."),
            ("Elastic and inelastic collisions", "Elastic: KE conserved. Inelastic: only momentum is conserved."),
            ("Coefficient of restitution", "e = relative speed of separation / relative speed of approach."),
        ],
        "practice": [
            (1, "Define work and state its SI unit.", "Work is the product of force and the displacement in the direction of the force. SI unit: joule."),
            (1, "What is the work done by the centripetal force on a body in uniform circular motion?", "Zero, because the force is always perpendicular to the displacement."),
            (2, "A 2 kg body moves at 10 m/s. Find its kinetic energy and the work needed to stop it.", "K = (1/2)(2)(100) = 100 J. Work done = -100 J (by the stopping force)."),
            (2, "Distinguish between conservative and non-conservative forces.", "A conservative force does path-independent work (zero over a closed loop), e.g. gravity. A non-conservative force does path-dependent work, e.g. friction."),
            (2, "A pump raises 1000 kg of water per minute through 30 m (g = 10 m/s^2). Find its power.", "P = mgh / t = 1000 x 10 x 30 / 60 = 5000 W = 5 kW."),
            (3, "State and prove the work-energy theorem for a constant force.", "Statement: net work equals change in KE. Proof: v^2 - u^2 = 2as. Multiply by m/2: (1/2)mv^2 - (1/2)mu^2 = m a s = F s = W."),
            (3, "Show that in a head-on elastic collision of two equal masses, the velocities are exchanged.", "Conservation of momentum: u1 + u2 = v1 + v2. Conservation of KE: u1^2 + u2^2 = v1^2 + v2^2. Solving gives v1 = u2 and v2 = u1."),
            (3, "A ball dropped from 10 m rebounds to 6.4 m. Find the coefficient of restitution and the fraction of KE lost.", "e = sqrt(h2/h1) = sqrt(0.64) = 0.8. Fraction of energy lost = 1 - 0.64 = 0.36, i.e. 36 %."),
            (3, "A spring (k = 200 N/m) is compressed by 10 cm. Find the stored energy and the speed given to a 0.5 kg block it releases.", "PE = (1/2)(200)(0.1)^2 = 1 J. (1/2)(0.5)v^2 = 1 gives v = 2 m/s."),
            (3, "Derive the expression for the potential energy of a stretched spring.", "Force F = kx. Work for a small extension dx is kx dx. Total W = integral from 0 to x of kx dx = (1/2) k x^2, which is stored as elastic potential energy."),
        ],
    },
    6: {
        "name": "System of Particles and Rotational Motion",
        "keywords": [
            ("Centre of mass", "Point where the whole mass can be taken as concentrated: R = sum(m r) / sum(m)."),
            ("Torque", "Turning effect of a force: tau = r x F."),
            ("Angular momentum", "L = r x p = I omega for a rigid body."),
            ("Conservation of angular momentum", "If net external torque is zero, L stays constant."),
            ("Moment of inertia", "I = sum(m r^2); rotational analogue of mass."),
            ("Radius of gyration", "Distance k such that I = M k^2."),
            ("Parallel axis theorem", "I = I_cm + M d^2."),
            ("Perpendicular axis theorem", "For a planar body, I_z = I_x + I_y."),
            ("Rolling motion", "Combination of translation of the centre of mass and rotation about it."),
        ],
        "practice": [
            (1, "Define torque.", "Torque is the moment of a force about a point: tau = r x F, with magnitude r F sin(theta)."),
            (1, "State the law of conservation of angular momentum.", "If the net external torque on a system is zero, its total angular momentum remains constant."),
            (2, "Find the centre of mass of a 2 kg mass at x = 0 and a 3 kg mass at x = 5 m.", "x_cm = (2 x 0 + 3 x 5) / 5 = 3 m from the first mass."),
            (2, "Why does a skater spin faster on pulling her arms in?", "Angular momentum L = I omega is conserved. Pulling arms in reduces I, so omega increases."),
            (2, "State the perpendicular axis theorem.", "For a plane lamina, the moment of inertia about an axis perpendicular to its plane equals the sum of the moments about two perpendicular axes in its plane meeting at the same point: I_z = I_x + I_y."),
            (3, "Using the parallel axis theorem, find the moment of inertia of a uniform disc about an axis through its rim perpendicular to its plane.", "I_cm = (1/2) M R^2. I = I_cm + M R^2 = (3/2) M R^2."),
            (3, "Derive the relation tau = I alpha for a rigid body rotating about a fixed axis.", "For a particle, tangential force F = m a = m r alpha, torque = r F = m r^2 alpha. Summing for all particles: tau = (sum m r^2) alpha = I alpha."),
            (3, "A wheel of moment of inertia 2 kg m^2 rotates at 10 rad/s. A retarding torque of 4 N m acts. Find the time to stop.", "alpha = tau / I = 2 rad/s^2. t = omega / alpha = 10 / 2 = 5 s."),
            (3, "Find the acceleration of a solid sphere rolling without slipping down an incline of angle theta.", "a = g sin(theta) / (1 + k^2/R^2) with k^2 = (2/5) R^2 gives a = (5/7) g sin(theta)."),
            (3, "State the conditions of equilibrium of a rigid body.", "(1) The net external force is zero (translational equilibrium). (2) The net external torque about any point is zero (rotational equilibrium)."),
        ],
    },
    7: {
        "name": "Gravitation",
        "keywords": [
            ("Law of gravitation", "F = G m1 m2 / r^2; G = 6.67 x 10^-11 N m^2 kg^-2."),
            ("Acceleration due to gravity", "g = G M / R^2 = 9.8 m/s^2 on the Earth's surface."),
            ("Variation of g", "With height: g' = g (1 - 2h/R) for small h. With depth: g' = g (1 - d/R)."),
            ("Gravitational potential energy", "U = -G M m / r."),
            ("Escape speed", "v_e = sqrt(2 G M / R) = sqrt(2 g R) = 11.2 km/s for the Earth."),
            ("Orbital speed", "v_o = sqrt(G M / r); near the surface sqrt(gR) = 7.9 km/s."),
            ("Kepler's laws", "Orbits are ellipses; equal areas in equal times; T^2 is proportional to a^3."),
            ("Geostationary satellite", "Period 24 h, in the equatorial plane, height about 36,000 km."),
            ("Gravitational field and potential", "Field I = F/m; potential V = -G M / r."),
        ],
        "practice": [
            (1, "State Kepler's third law.", "The square of the period of revolution of a planet is proportional to the cube of the semi-major axis of its orbit."),
            (1, "What is the escape speed of the Earth?", "About 11.2 km/s."),
            (2, "Find the value of g at a height equal to the Earth's radius above the surface (g = 9.8 m/s^2 at the surface).", "g' = g (R / (R + h))^2 = g / 4 = 2.45 m/s^2."),
            (2, "Why does g decrease with depth below the Earth's surface?", "Only the mass inside the sphere of radius (R - d) attracts the body. g' = g (1 - d/R), which becomes zero at the centre."),
            (2, "What is a geostationary satellite? Give two conditions for it.", "A satellite that appears fixed over one point on Earth. It must revolve in the equatorial plane from west to east, with a period of 24 hours (height about 36,000 km)."),
            (3, "Derive the expression for the escape speed from the Earth.", "To escape, total energy must be at least zero: (1/2) m v^2 - G M m / R = 0. So v_e = sqrt(2 G M / R) = sqrt(2 g R) = 11.2 km/s."),
            (3, "Derive the orbital speed of a satellite near the Earth's surface and its time period.", "G M m / R^2 = m v^2 / R gives v = sqrt(g R) = about 7.9 km/s. T = 2 pi R / v = 2 pi sqrt(R/g), which is about 84 minutes."),
            (3, "A planet has 1/10 of the Earth's mass and half of its radius. Find g on it (g_earth = 9.8 m/s^2).", "g' = g x (1/10) / (1/2)^2 = 0.4 g = 3.92 m/s^2."),
            (3, "Prove Kepler's third law for a circular orbit.", "G M m / r^2 = m omega^2 r with omega = 2 pi / T. So T^2 = (4 pi^2 / G M) r^3, i.e. T^2 is proportional to r^3."),
            (3, "Why does the weight of a body vary between the equator and the poles?", "The Earth rotates and is bulged at the equator. At latitude lambda, g' = g - omega^2 R cos^2(lambda), so g is lowest at the equator and highest at the poles."),
        ],
    },
}

CHAPTERS_B = {
    8: {
        "name": "Mechanical Properties of Solids",
        "keywords": [
            ("Stress", "Restoring force per unit area; unit N/m^2 (pascal)."),
            ("Strain", "Fractional change: longitudinal, shear or volumetric; dimensionless."),
            ("Hooke's law", "Within the elastic limit, stress is proportional to strain."),
            ("Young's modulus", "Y = longitudinal stress / longitudinal strain = F L / (A dL)."),
            ("Bulk modulus", "B = -p / (dV / V); its reciprocal is compressibility."),
            ("Shear modulus", "G = shear stress / shear strain."),
            ("Poisson's ratio", "Lateral strain divided by longitudinal strain."),
            ("Elastic limit", "Maximum stress up to which a body regains its original shape."),
            ("Stress-strain curve", "Proportional limit, elastic limit, yield point, ultimate strength and fracture point."),
            ("Elastic potential energy", "Energy per unit volume = (1/2) x stress x strain."),
        ],
        "practice": [
            (1, "State Hooke's law.", "Within the elastic limit, the stress developed in a body is directly proportional to the strain produced."),
            (1, "What is Poisson's ratio?", "The ratio of lateral strain to longitudinal strain; it is dimensionless."),
            (2, "A wire of length 2 m and cross-section 1 mm^2 stretches by 1 mm under a load of 100 N. Find Young's modulus.", "Y = F L / (A dL) = 100 x 2 / (10^-6 x 10^-3) = 2 x 10^11 N/m^2."),
            (2, "Why is steel considered more elastic than rubber?", "For the same stress, steel shows much less strain, so its Young's modulus is larger and it returns to its shape more effectively."),
            (2, "Define bulk modulus and compressibility.", "Bulk modulus is the ratio of hydraulic pressure to the volumetric strain. Compressibility is its reciprocal."),
            (3, "Derive the elastic potential energy stored per unit volume in a stretched wire.", "W = (1/2) F dL = (1/2)(stress x A)(strain x L) = (1/2) x stress x strain x (A L). Energy per unit volume = (1/2) x stress x strain."),
            (3, "Draw and explain the stress-strain curve for a metal wire.", "Stress rises linearly up to the proportional limit (Hooke's law), then non-linearly up to the elastic limit. Beyond the yield point the wire shows plastic flow. The curve peaks at the ultimate tensile strength and the wire finally breaks at the fracture point."),
            (3, "Two wires of the same material have lengths in the ratio 1 : 2 and radii in the ratio 1 : 2. They carry the same load. Find the ratio of their extensions.", "Extension = F L / (Y pi r^2), so dL1 / dL2 = (L1 / L2)(r2 / r1)^2 = (1/2)(4) = 2 : 1."),
            (3, "A steel cable of radius 1.5 cm supports a load of 800 kg (g = 10 m/s^2). Find the stress.", "F = 8000 N, A = pi (0.015)^2 = 7.07 x 10^-4 m^2. Stress = 8000 / 7.07 x 10^-4 = 1.13 x 10^7 N/m^2."),
            (3, "Why are girders in bridges and heavy machines made with an I-shaped cross-section?", "A beam bends less when it is deep and broad. An I-section gives high resistance to bending with the least material, since material near the middle contributes little."),
        ],
    },
    9: {
        "name": "Mechanical Properties of Fluids",
        "keywords": [
            ("Pressure", "Force per unit area; P = P0 + rho g h in a fluid at depth h."),
            ("Pascal's law", "Pressure applied to an enclosed fluid is transmitted undiminished to every part."),
            ("Archimedes' principle", "Buoyant force equals the weight of fluid displaced."),
            ("Equation of continuity", "A1 v1 = A2 v2 for an incompressible fluid."),
            ("Bernoulli's principle", "P + (1/2) rho v^2 + rho g h = constant along a streamline."),
            ("Viscosity", "Internal friction of a fluid; F = eta A (dv/dx)."),
            ("Stokes' law", "Viscous drag on a small sphere: F = 6 pi eta r v."),
            ("Terminal velocity", "Constant velocity when weight balances buoyancy plus viscous drag."),
            ("Reynolds number", "Re = rho v d / eta; decides laminar (low) or turbulent (high) flow."),
            ("Surface tension", "Force per unit length on a line in the surface; S = F/l."),
            ("Capillary rise", "h = 2 S cos(theta) / (r rho g)."),
        ],
        "practice": [
            (1, "State Pascal's law.", "Pressure applied to an enclosed incompressible fluid is transmitted equally and undiminished to every part of the fluid and the walls of the container."),
            (1, "Define surface tension and give its SI unit.", "The force per unit length acting along a line drawn on a liquid surface. SI unit: N/m."),
            (2, "Find the absolute pressure at a depth of 10 m in water (P0 = 10^5 Pa, g = 10 m/s^2, rho = 1000 kg/m^3).", "P = P0 + rho g h = 10^5 + 1000 x 10 x 10 = 2 x 10^5 Pa."),
            (2, "Why do raindrops fall with a constant terminal velocity?", "As speed grows, the viscous drag of air grows. When drag plus buoyancy balances the weight, net force is zero and the drop falls at constant speed."),
            (2, "State the equation of continuity and what it means.", "A1 v1 = A2 v2: for an incompressible fluid the volume flowing per second is the same at every cross-section, so the fluid moves faster in narrower parts."),
            (3, "State Bernoulli's principle and give two applications.", "For steady, incompressible, non-viscous flow, P + (1/2) rho v^2 + rho g h is constant along a streamline. Applications: lift on an aerofoil, a spray gun/atomiser, a Venturi meter."),
            (3, "Derive the expression for the capillary rise of a liquid in a tube.", "Upward pull = 2 pi r S cos(theta). Weight of column = pi r^2 h rho g. Equating: h = 2 S cos(theta) / (r rho g)."),
            (3, "Water flows at 2 m/s in a pipe of radius 2 cm. Find its speed where the pipe narrows to radius 1 cm.", "A1 v1 = A2 v2, so v2 = v1 (r1 / r2)^2 = 2 x 4 = 8 m/s."),
            (3, "Derive the terminal velocity of a sphere of radius r and density rho falling in a fluid of density sigma and viscosity eta.", "At terminal speed: weight = buoyancy + drag. (4/3) pi r^3 rho g = (4/3) pi r^3 sigma g + 6 pi eta r v. So v_t = 2 r^2 (rho - sigma) g / (9 eta)."),
            (3, "In a hydraulic lift the small piston has area 5 cm^2 and the large piston 500 cm^2. What load can be lifted by a 100 N force on the small piston?", "F2 = F1 (A2 / A1) = 100 x 100 = 10^4 N."),
        ],
    },
    10: {
        "name": "Thermal Properties of Matter",
        "keywords": [
            ("Temperature and heat", "Temperature measures hotness; heat is energy transferred because of a temperature difference."),
            ("Thermal expansion", "Linear, area and volume expansion with coefficients alpha, beta = 2 alpha, gamma = 3 alpha."),
            ("Specific heat capacity", "Heat per unit mass per degree: Q = m c dT."),
            ("Calorimetry", "Heat lost by the hot body equals heat gained by the cold body."),
            ("Latent heat", "Heat absorbed or released during a change of state at constant temperature: Q = m L."),
            ("Conduction", "Heat transfer through matter without its motion: Q/t = K A dT / L."),
            ("Convection", "Heat transfer by the actual movement of the fluid."),
            ("Radiation", "Heat transfer by electromagnetic waves; needs no medium."),
            ("Newton's law of cooling", "Rate of cooling is proportional to the temperature excess over the surroundings."),
            ("Stefan-Boltzmann law", "Power radiated by a black body: P = sigma A T^4."),
            ("Wien's displacement law", "lambda_max x T = constant = 2.9 x 10^-3 m K."),
        ],
        "practice": [
            (1, "Write the relation between the Celsius and Fahrenheit scales.", "F = (9/5) C + 32."),
            (1, "Define latent heat of fusion.", "The heat required to change unit mass of a solid to liquid at its melting point without a change in temperature."),
            (2, "At what temperature are the Celsius and Fahrenheit readings equal?", "C = F gives C = (9/5) C + 32, so C = -40. At -40 degrees both scales read the same."),
            (2, "Find the heat needed to convert 10 g of ice at 0 C to steam at 100 C (L_f = 80 cal/g, c = 1 cal/g C, L_v = 540 cal/g).", "Melting: 10 x 80 = 800 cal. Heating water: 10 x 1 x 100 = 1000 cal. Vaporising: 10 x 540 = 5400 cal. Total = 7200 cal."),
            (2, "Distinguish between conduction, convection and radiation.", "Conduction: heat passes from particle to particle in solids with no bulk motion. Convection: heat is carried by moving fluid. Radiation: heat travels as electromagnetic waves and needs no medium."),
            (3, "Show that the coefficient of area expansion is twice and of volume expansion three times the coefficient of linear expansion.", "L' = L(1 + alpha dT). Area = L'^2 = L^2 (1 + 2 alpha dT) so beta = 2 alpha. Volume = L'^3 = L^3 (1 + 3 alpha dT) so gamma = 3 alpha (neglecting higher powers of alpha)."),
            (3, "State Stefan's law. By what factor does the radiated power change if the absolute temperature of a black body is doubled?", "Power radiated is proportional to T^4. If T is doubled the power becomes 2^4 = 16 times."),
            (3, "A body cools from 80 C to 70 C in 5 minutes in surroundings at 20 C. Estimate the time to cool from 70 C to 60 C.", "k = (10/5)/(75 - 20) = 2/55 per min. Next 10 degrees: t = 10 / [(2/55)(65 - 20)] = 10 / 1.636 = about 6.1 minutes."),
            (3, "The Sun's spectrum has its peak at 500 nm. Estimate its surface temperature using Wien's law.", "T = b / lambda_max = 2.9 x 10^-3 / 5 x 10^-7 = 5800 K."),
            (3, "A metal rod 1 m long and area 10^-4 m^2 (K = 400 W/m K) has its ends at 100 C and 0 C. Find the rate of heat flow.", "Q/t = K A dT / L = 400 x 10^-4 x 100 / 1 = 4 W."),
        ],
    },
    11: {
        "name": "Thermodynamics",
        "keywords": [
            ("Thermal equilibrium", "Two systems with no net heat flow between them have the same temperature."),
            ("Zeroth law", "If A and B are each in equilibrium with C, then A and B are in equilibrium with each other."),
            ("Internal energy", "Sum of the molecular kinetic and potential energies; a state function."),
            ("First law", "dQ = dU + dW: heat supplied = increase in internal energy + work done by the system."),
            ("Thermodynamic processes", "Isothermal (T constant), adiabatic (Q = 0), isochoric (V constant), isobaric (P constant)."),
            ("Specific heats of a gas", "Cp - Cv = R; gamma = Cp / Cv."),
            ("Second law", "Kelvin-Planck: no engine can convert heat completely to work. Clausius: heat cannot flow by itself from cold to hot."),
            ("Carnot engine", "Reversible engine between two temperatures with efficiency 1 - T2/T1."),
            ("Reversible and irreversible processes", "A reversible process can be exactly retraced; real processes are irreversible."),
            ("Refrigerator", "Reversed heat engine with coefficient of performance COP = T2 / (T1 - T2)."),
        ],
        "practice": [
            (1, "State the zeroth law of thermodynamics.", "If two systems are separately in thermal equilibrium with a third system, they are in thermal equilibrium with each other."),
            (1, "What is an adiabatic process?", "A process in which no heat enters or leaves the system (dQ = 0)."),
            (2, "A gas absorbs 500 J of heat and does 200 J of work. Find the change in internal energy.", "dU = dQ - dW = 500 - 200 = 300 J."),
            (2, "Show that Cp - Cv = R for an ideal gas.", "At constant volume dQ = dU = Cv dT. At constant pressure dQ = dU + P dV = Cv dT + R dT (since PV = RT gives P dV = R dT). So Cp = Cv + R."),
            (2, "Find the efficiency of a Carnot engine working between 500 K and 300 K.", "Efficiency = 1 - T2/T1 = 1 - 300/500 = 0.4 = 40 %."),
            (3, "Derive the work done by an ideal gas in an isothermal expansion from V1 to V2.", "W = integral of P dV = integral of (nRT / V) dV = nRT ln(V2 / V1)."),
            (3, "State the Kelvin-Planck and Clausius statements of the second law.", "Kelvin-Planck: it is impossible to take heat from a single reservoir and convert it completely into work without other changes. Clausius: it is impossible for heat to flow from a colder to a hotter body by itself, without work."),
            (3, "A Carnot engine takes 1000 J from a source at 600 K and rejects heat to a sink at 300 K. Find the efficiency, work done and heat rejected.", "Efficiency = 1 - 300/600 = 50 %. Work = 500 J. Heat rejected = 1000 - 500 = 500 J."),
            (3, "Can a room be cooled by leaving a refrigerator door open? Explain.", "No. The refrigerator removes heat from the room's air but also rejects that heat plus the electrical work done into the same room, so the room warms slightly."),
            (5, "Derive the work done in an adiabatic expansion of an ideal gas.", "For an adiabatic process P V^gamma = constant = K. W = integral from V1 to V2 of K V^(-gamma) dV = K (V2^(1-gamma) - V1^(1-gamma)) / (1 - gamma) = (P1 V1 - P2 V2) / (gamma - 1). The gas does work at the cost of its internal energy, so it cools."),
        ],
    },
    12: {
        "name": "Kinetic Theory",
        "keywords": [
            ("Ideal gas equation", "PV = n R T = N k T."),
            ("Boyle's and Charles' laws", "At constant T, PV is constant. At constant P, V / T is constant."),
            ("Assumptions of kinetic theory", "Point-like molecules, random motion, elastic collisions, no intermolecular forces, negligible molecular volume."),
            ("Pressure of a gas", "P = (1/3) rho v_rms^2."),
            ("RMS speed", "v_rms = sqrt(3 R T / M) = sqrt(3 k T / m)."),
            ("Kinetic meaning of temperature", "Average translational KE per molecule = (3/2) k T."),
            ("Degrees of freedom", "Independent ways a molecule can store energy: monatomic 3, diatomic 5, non-linear polyatomic 6."),
            ("Law of equipartition of energy", "Each degree of freedom carries (1/2) k T of energy per molecule."),
            ("Mean free path", "Average distance between collisions: lambda = 1 / (sqrt(2) pi d^2 n)."),
            ("Avogadro's number", "6.022 x 10^23 per mole; k = R / N_A = 1.38 x 10^-23 J/K."),
        ],
        "practice": [
            (1, "Write the ideal gas equation.", "PV = n R T, where n is the number of moles."),
            (1, "State the law of equipartition of energy.", "In thermal equilibrium, the total energy of a gas is equally distributed among all its degrees of freedom, each getting (1/2) k T per molecule."),
            (2, "Find the rms speed of hydrogen molecules at 300 K (M = 2 g/mol, R = 8.31 J/mol K).", "v_rms = sqrt(3 R T / M) = sqrt(3 x 8.31 x 300 / 0.002) = sqrt(3.74 x 10^6) = about 1.93 x 10^3 m/s."),
            (2, "Find the average translational kinetic energy of a gas molecule at 300 K (k = 1.38 x 10^-23 J/K).", "KE = (3/2) k T = 1.5 x 1.38 x 10^-23 x 300 = 6.2 x 10^-21 J."),
            (2, "Define mean free path and write its expression.", "The average distance travelled by a molecule between two successive collisions: lambda = 1 / (sqrt(2) pi d^2 n), n = number density, d = molecular diameter."),
            (3, "Derive the expression for the pressure exerted by an ideal gas.", "A molecule of velocity component v_x bounces off a wall with change of momentum 2 m v_x. Over time, force from all molecules gives P = (1/3)(N/V) m v_rms^2 = (1/3) rho v_rms^2."),
            (3, "Using the equipartition law, find Cv, Cp and gamma for a diatomic gas at ordinary temperature.", "f = 5. Cv = (5/2) R. Cp = Cv + R = (7/2) R. gamma = 7/5 = 1.4."),
            (3, "Find the ratio of the rms speeds of oxygen and hydrogen molecules at the same temperature.", "v_rms is proportional to 1 / sqrt(M). Ratio = sqrt(2 / 32) = 1/4."),
            (3, "Calculate the number of molecules in 1 cm^3 of a gas at STP.", "1 mole (22400 cm^3) has 6.022 x 10^23 molecules. In 1 cm^3: 6.022 x 10^23 / 22400 = 2.69 x 10^19."),
            (3, "Show that the average kinetic energy of a molecule depends only on temperature.", "From PV = (1/3) N m v_rms^2 and PV = N k T we get (1/2) m v_rms^2 = (3/2) k T, which depends only on T, not on the gas."),
        ],
    },
    13: {
        "name": "Oscillations",
        "keywords": [
            ("Periodic and oscillatory motion", "Motion that repeats after equal time intervals; back and forth about a mean position."),
            ("Simple harmonic motion", "Restoring force proportional to displacement: F = -k x."),
            ("Amplitude, period, frequency", "A = maximum displacement; T = time for one oscillation; f = 1/T; omega = 2 pi f."),
            ("SHM equations", "x = A cos(omega t + phi); v = -A omega sin(...); a = -omega^2 x."),
            ("Phase", "The argument (omega t + phi) of the sine/cosine; phi is the initial phase."),
            ("Energy of SHM", "Total energy = (1/2) k A^2, constant; KE and PE interchange."),
            ("Spring-mass system", "T = 2 pi sqrt(m / k)."),
            ("Simple pendulum", "T = 2 pi sqrt(l / g) for small angles."),
            ("Damped oscillations", "Amplitude decreases with time due to resistive forces."),
            ("Resonance", "Large amplitude when the driving frequency equals the natural frequency."),
        ],
        "practice": [
            (1, "Define simple harmonic motion.", "Motion in which the restoring force on a particle is directly proportional to its displacement from the mean position and is directed towards it."),
            (1, "What is resonance?", "The condition in which a system driven at its natural frequency oscillates with maximum amplitude."),
            (2, "Find the time period of a simple pendulum of length 1 m (g = 9.8 m/s^2).", "T = 2 pi sqrt(1 / 9.8) = 2.007 s, about 2 s."),
            (2, "A 0.5 kg mass is attached to a spring of constant 200 N/m. Find the period of oscillation.", "T = 2 pi sqrt(m/k) = 2 pi sqrt(0.5 / 200) = 0.314 s."),
            (2, "Write expressions for the velocity and acceleration in SHM and their maximum values.", "v = -A omega sin(omega t + phi), maximum A omega. a = -omega^2 x, maximum omega^2 A."),
            (3, "Show that the total energy of a particle in SHM is (1/2) k A^2.", "At displacement x: KE = (1/2) m omega^2 (A^2 - x^2), PE = (1/2) m omega^2 x^2. Sum = (1/2) m omega^2 A^2 = (1/2) k A^2, independent of x."),
            (3, "Derive the time period of a simple pendulum.", "For a small angle theta, restoring torque gives m l^2 alpha = -m g l theta, so alpha = -(g/l) theta. This is SHM with omega^2 = g/l, so T = 2 pi sqrt(l / g)."),
            (3, "A particle in SHM has amplitude 5 cm and period 2 s. Find the maximum speed and the speed at x = 3 cm.", "omega = 2 pi / T = pi rad/s. v_max = A omega = 5 pi = 15.7 cm/s. v = omega sqrt(A^2 - x^2) = pi x 4 = 12.6 cm/s."),
            (3, "Find the effective spring constant for two springs of 100 N/m each connected in (i) series and (ii) parallel.", "Series: k = k1 k2 / (k1 + k2) = 50 N/m. Parallel: k = k1 + k2 = 200 N/m."),
            (3, "Why does a pendulum clock lose time in summer?", "Heating increases the length of the pendulum, so T = 2 pi sqrt(l/g) increases. Each swing takes longer and the clock runs slow."),
        ],
    },
    14: {
        "name": "Waves",
        "keywords": [
            ("Transverse and longitudinal waves", "Particles vibrate perpendicular to, or along, the direction of wave travel."),
            ("Wave equation", "y = A sin(k x - omega t); v = f lambda = omega / k."),
            ("Speed of waves", "On a string v = sqrt(T / mu); in a gas v = sqrt(gamma P / rho)."),
            ("Newton-Laplace formula", "Sound travels adiabatically in air; Laplace's correction replaces P/rho with gamma P/rho."),
            ("Superposition principle", "The resultant displacement is the vector sum of the individual displacements."),
            ("Reflection of waves", "Phase change of pi at a fixed end (rigid boundary); none at a free end."),
            ("Standing waves", "Formed by two identical waves travelling in opposite directions; nodes and antinodes."),
            ("Normal modes", "String fixed at both ends: f_n = n v / 2L. Closed pipe: f = (2n - 1) v / 4L."),
            ("Beats", "Periodic variation in loudness; beat frequency = |f1 - f2|."),
            ("Doppler effect", "Apparent change in frequency due to relative motion of source and observer."),
        ],
        "practice": [
            (1, "Define wavelength.", "The distance between two consecutive points in the same phase (e.g. two crests) of a wave."),
            (1, "Write the expression for the speed of a transverse wave on a stretched string.", "v = sqrt(T / mu), where T is tension and mu is mass per unit length."),
            (2, "The speed of sound in air at 0 C is 332 m/s. Find it at 27 C.", "v is proportional to sqrt(T). v = 332 x sqrt(300 / 273) = about 348 m/s."),
            (2, "What are beats? Two tuning forks of 256 Hz and 260 Hz are sounded together. Find the beat frequency.", "Beats are periodic rises and falls in loudness when two sound waves of slightly different frequency superpose. Beat frequency = 260 - 256 = 4 per second."),
            (2, "Distinguish between progressive and stationary waves.", "A progressive wave carries energy forward and all particles have the same amplitude. A stationary wave does not transfer energy, with fixed nodes (zero amplitude) and antinodes (maximum amplitude)."),
            (3, "A string of length 1 m is fixed at both ends and the wave speed on it is 200 m/s. Find the frequencies of the first three harmonics.", "f_n = n v / 2L = n x 100 Hz. So 100 Hz, 200 Hz and 300 Hz."),
            (3, "A closed organ pipe is 0.5 m long (v = 340 m/s). Find its fundamental frequency and the next two harmonics.", "f1 = v / 4L = 340 / 2 = 170 Hz. A closed pipe has only odd harmonics: 3 f1 = 510 Hz and 5 f1 = 850 Hz."),
            (3, "A source of 400 Hz moves towards a stationary observer at 20 m/s (v = 340 m/s). Find the frequency heard.", "f' = f v / (v - v_s) = 400 x 340 / 320 = 425 Hz."),
            (3, "Explain Newton's formula for the speed of sound and Laplace's correction.", "Newton assumed isothermal changes: v = sqrt(P / rho) = 280 m/s, which is too low. Laplace showed the changes are adiabatic: v = sqrt(gamma P / rho) = about 331 m/s, matching experiment."),
            (5, "Explain the formation of standing waves on a string fixed at both ends and derive the normal modes.", "A wave reflected at the fixed ends superposes with the incident wave to give y = 2A sin(kx) cos(omega t). Nodes occur where sin(kx) = 0. Since both ends are nodes, L = n (lambda / 2), so lambda = 2L / n and f_n = n v / (2L), n = 1, 2, 3, ... The mode n = 1 is the fundamental and n = 2, 3, ... are overtones."),
        ],
    },
}
CHAPTERS.update(CHAPTERS_B)


for _c in CHAPTERS.values():
    _c.setdefault("ai", [])

# AI-generated questions saved in the repo (file: ai_bank.json), if present
_ai_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_bank.json")
if os.path.exists(_ai_path):
    try:
        with open(_ai_path, encoding="utf-8") as _f:
            for _k, _rows in json.load(_f).items():
                if int(_k) in CHAPTERS:
                    CHAPTERS[int(_k)]["ai"].extend(tuple(r) for r in _rows)
    except (OSError, ValueError, TypeError):
        pass

st.set_page_config(page_title="CBSE XI Physics", page_icon="⚛️")

MARKS_CHOICES = [1, 2, 3, 5]


def show_questions(items, label_ai=False):
    for n, row in enumerate(items, 1):
        marks, q, ans = row[0], row[1], row[2]
        tag = " (AI)" if label_ai else ""
        st.markdown(f"**Q{n}. [{marks} mark{'s' if marks > 1 else ''}]{tag}** {q}")
        with st.expander("Try it yourself, then click to see the answer"):
            st.write(ans)


# --------------------------------------------------------------------- parts
def keywords_view(ch_id):
    st.header("Key words")
    for term, meaning in CHAPTERS[ch_id]["keywords"]:
        st.markdown(f"**{term}**  \n{meaning}")


def practice_view(ch_id):
    st.header("Practice questions")
    c1, c2 = st.columns([3, 2])
    pick = c1.radio("Marks", ["All"] + MARKS_CHOICES, horizontal=True)
    use_ai = c2.checkbox("Include AI-generated questions", value=True)
    ch = CHAPTERS[ch_id]
    built = [p for p in ch["practice"] if pick == "All" or p[0] == pick]
    ai_rows = []
    if use_ai:
        session_bank = st.session_state.get("ai_bank", {}).get(ch_id, [])
        ai_rows = [p for p in list(ch["ai"]) + list(session_bank) if pick == "All" or p[0] == pick]
    st.caption(f"{len(built)} built-in questions" + (f" + {len(ai_rows)} AI questions" if use_ai else ""))
    if not built and not ai_rows:
        st.write("No questions with those marks in this chapter.")
    show_questions(built)
    if ai_rows:
        st.subheader("AI-generated questions")
        st.caption("Written by Gemini AI. These can contain mistakes: check with your NCERT textbook.")
        show_questions(ai_rows, label_ai=True)


# ---------------------------------------------------------- AI generator part
MODELS = ["gemini-flash-latest", "gemini-2.5-flash"]  # used only if auto-discovery fails
BASE = "https://generativelanguage.googleapis.com/v1beta"


def get_secret(name):
    try:
        return st.secrets.get(name)
    except Exception:
        return None


@st.cache_data(ttl=600, show_spinner=False)
def discover_models(key):
    """Ask Gemini which models this key can use, best-looking 'flash' models first."""
    try:
        r = requests.get(f"{BASE}/models", params={"pageSize": 200},
                         headers={"x-goog-api-key": key}, timeout=30)
        if r.status_code != 200:
            return []
        names = []
        for m in r.json().get("models", []):
            if "generateContent" not in m.get("supportedGenerationMethods", []):
                continue
            name = m["name"].split("/")[-1]
            low = name.lower()
            if "flash" not in low or any(x in low for x in
                                         ("image", "tts", "live", "audio", "thinking", "robotics", "vision")):
                continue
            names.append(name)
    except (requests.RequestException, ValueError, KeyError):
        return []

    def rank(n):
        low = n.lower()
        unstable = any(x in low for x in ("preview", "exp"))
        lite = "lite" in low
        return (unstable, lite, "latest" not in low, tuple(-int(c) for c in
                "".join(ch if ch.isdigit() or ch == "." else " " for ch in low).replace(".", " ").split()[:3]))
    ordered = sorted(names, key=rank)
    # Fast "lite" models (no long thinking) first, then the others.
    stable_lite = [n for n in ordered if "lite" in n.lower() and not any(x in n.lower() for x in ("preview", "exp"))]
    return stable_lite + [n for n in ordered if n not in stable_lite]




ANGLES = [
    "numerical problems with a short calculation",
    "derivations and proofs asked in board-exam style",
    "'why' questions that test the physical reason",
    "conceptual questions that expose common misconceptions",
    "comparison of two related quantities or laws",
    "application questions from everyday life or technology",
    "graph-based questions described in words",
    "questions about dimensions, units and limiting cases",
    "short statement/definition questions with a twist",
]


def build_prompt(ch_id, difficulty, n, marks="Mixed", focus=None, angles=None, avoid=None):
    ch = CHAPTERS[ch_id]
    terms = ", ".join(t for t, _ in ch["keywords"])
    styles = {
        "Easy": "straightforward recall and direct application",
        "Medium": "conceptual questions needing one or two steps of reasoning",
        "Hard": "multi-step problems and common-misconception traps",
        "Tricky": "very tricky questions where a common wrong approach looks attractive "
                  "(special cases, units, limiting cases, sign conventions)",
    }
    marks_line = ("Mix 1, 2, 3 and 5 mark questions (1 mark: one-line answer; 2 marks: short answer; "
                  "3 marks: short derivation or numerical; 5 marks: long derivation or explanation)."
                  if marks == "Mixed" else f"Every question must carry exactly {marks} mark(s).")
    extra = ""
    if focus:
        extra += f"For variety, focus mainly on these topics this time: {', '.join(focus)}.\n"
    if angles:
        extra += f"Question styles to use this time: {'; '.join(angles)}.\n"
    if avoid:
        extra += ("Do NOT repeat or rephrase any of these earlier questions:\n- "
                  + "\n- ".join(avoid) + "\n")
    return (
        "You are an expert CBSE Class XI Physics teacher following the NCERT syllabus.\n"
        f"Write {n} NEW and DIFFERENT written (not multiple-choice) questions for Chapter {ch_id}: {ch['name']}.\n"
        f"All topics of the chapter: {terms}.\n"
        f"{extra}"
        f"Difficulty: {difficulty} - {styles[difficulty]}.\n"
        f"{marks_line}\n"
        f"(Variation code: {random.randint(1000, 9999)})\n"
        "For every question give a correct, complete model answer. For numericals show the formula, "
        "the substitution and the final value with units (use g = 9.8 m/s^2 unless the question says otherwise). "
        "Double-check every calculation and fact. Do not copy textbook sentences. "
        "Use plain text (write m/s^2, x 10^5, sqrt(...), no LaTeX; Greek letters are fine).\n"
        "Return ONLY a JSON array. Each element must be an object with keys: "
        '"marks" (integer: 1, 2, 3 or 5), "question" (string), "answer" (string).'
    )


def thinking_variants(name):
    """Turn off / minimise 'thinking' so answers come back fast. Last variant = no setting."""
    base = {"temperature": 1.0, "responseMimeType": "application/json", "maxOutputTokens": 8192}
    low = dict(base, thinkingConfig={"thinkingLevel": "low"})
    zero = dict(base, thinkingConfig={"thinkingBudget": 0})
    return ([low, zero, base] if "gemini-3" in name.lower() else [zero, low, base])


def call_gemini(prompt, key, status=None, model=None):
    """Try several models; give up after about 3 minutes so the page never hangs."""
    start = time.time()
    chosen = model or get_secret("GEMINI_MODEL")
    models = [chosen] if chosen else (discover_models(key)[:6] or MODELS)
    problems = []
    for name in models:
        if time.time() - start > 150:
            problems.append("stopped after 2.5 minutes")
            break
        if status:
            status.write(f"Trying model: {name} ...")
        cfgs = thinking_variants(name)
        ci, busy_retries = 0, 0
        while ci < len(cfgs):
            try:
                r = requests.post(
                    f"{BASE}/models/{name}:generateContent",
                    headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": cfgs[ci]},
                    timeout=60,
                )
            except requests.Timeout:
                problems.append(f"{name}: too slow (60 s)")
                break
            except requests.RequestException as e:
                problems.append(f"{name}: network problem ({e})")
                break
            if r.status_code == 200:
                try:
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"], None
                except (KeyError, IndexError, ValueError):
                    problems.append(f"{name}: empty or blocked answer")
                    break
            msg = ""
            try:
                msg = r.json().get("error", {}).get("message", "")
            except ValueError:
                pass
            if r.status_code == 429:
                return None, "Gemini free limit reached for now. Wait a minute (or until tomorrow) and try again."
            if r.status_code in (401, 403) or "API key" in msg:
                return None, f"Gemini rejected the API key. Check the key in Secrets. ({msg})"
            if r.status_code in (500, 503) and busy_retries < 1:
                busy_retries += 1
                if status:
                    status.write(f"{name} is busy, retrying in 3 seconds ...")
                time.sleep(3)
                continue
            if r.status_code == 400 and ci < len(cfgs) - 1:
                ci += 1  # model may not accept this thinking setting: try the next variant
                continue
            problems.append(f"{name}: error {r.status_code} {msg[:80]}")
            break
    return None, "Could not get questions from Gemini. " + " | ".join(problems)




def parse_questions(text):
    data = json.loads(text)
    if isinstance(data, dict):
        data = data.get("questions", [data])
    items, skipped = [], 0
    for d in data:
        try:
            marks = int(d["marks"])
            q = str(d["question"]).strip()
            a = str(d["answer"]).strip()
            ok = marks in MARKS_CHOICES and q and a
        except (KeyError, TypeError, ValueError):
            ok = False
        if not ok:
            skipped += 1
            continue
        items.append((marks, q, a))
    return items, skipped


def collect(ch_id, difficulty, n, marks, key, model, status=None):
    """One Gemini request -> list of fresh questions (already stored in the session bank)."""
    history = st.session_state.setdefault("ai_history", {}).setdefault(ch_id, [])
    bank = st.session_state.setdefault("ai_bank", {}).setdefault(ch_id, [])
    terms = [t for t, _ in CHAPTERS[ch_id]["keywords"]]
    prompt = build_prompt(ch_id, difficulty, n, marks,
                          focus=random.sample(terms, min(3, len(terms))),
                          angles=random.sample(ANGLES, 2),
                          avoid=[q[:90] for q in history[-40:]])
    text, err = call_gemini(prompt, key, status, model)
    if err:
        return [], 0, err
    try:
        items, skipped = parse_questions(text)
    except (ValueError, TypeError):
        return [], 0, "Gemini's reply was not in the expected format. Please try again."
    seen = {q.lower()[:60] for q in history}
    fresh = []
    for it in items:
        if it[1].lower()[:60] not in seen:
            seen.add(it[1].lower()[:60])
            fresh.append(it)
    skipped += len(items) - len(fresh)
    for it in fresh:
        history.append(it[1])
        bank.append(it)
    return fresh, skipped, None


def bulk_view(ch_id, difficulty, marks, key, model):
    bank_all = st.session_state.get("ai_bank", {})
    target = st.slider("How many questions to collect for this chapter", 20, 100, 100, step=10)
    st.caption("This makes about 10 Gemini requests one after another and takes several minutes. "
               "Keep this tab open. If the free limit is reached it stops and keeps what it has.")
    if st.button("📚 Build question bank", key="bulk_btn"):
        have = len(bank_all.get(ch_id, []))
        bar = st.progress(min(have / target, 1.0))
        note = st.empty()
        fails = 0
        while len(st.session_state["ai_bank"].get(ch_id, [])) < target and fails < 3:
            have = len(st.session_state["ai_bank"].get(ch_id, []))
            note.write(f"Asking Gemini for the next 10 questions... ({have} of {target} collected)")
            fresh, _, err = collect(ch_id, difficulty, 10, marks, key, model)
            if err:
                fails += 1
                note.warning(err)
                if "limit" in err:
                    break
                time.sleep(5)
                continue
            if not fresh:
                fails += 1
                continue
            fails = 0
            bar.progress(min(len(st.session_state["ai_bank"].get(ch_id, [])) / target, 1.0))
            time.sleep(4)  # stay under the free per-minute limit
        note.success(f"Collected {len(st.session_state['ai_bank'].get(ch_id, []))} AI questions for this chapter.")
        bank_all = st.session_state.get("ai_bank", {})
    st.write(f"**{len(bank_all.get(ch_id, []))}** AI questions collected for this chapter in this session "
             f"({sum(len(v) for v in bank_all.values())} in all chapters).")
    if bank_all:
        st.download_button(
            "⬇️ Download ALL collected questions (ai_bank.json)",
            json.dumps({str(c): [list(r) for r in v] for c, v in bank_all.items()}, ensure_ascii=False),
            file_name="ai_bank.json", mime="application/json",
        )
        st.caption("Upload ai_bank.json to your GitHub repo (same folder as app.py). "
                   "The app then keeps these questions permanently.")


def ai_view(ch_id):
    st.header("AI question generator")
    key = get_secret("GEMINI_API_KEY")
    if not key:
        st.warning(
            "No Gemini key found. In Streamlit open **App settings -> Secrets** and add this line "
            "(with your own key):\n\n`GEMINI_API_KEY = \"your-key-here\"`\n\nThen save and reboot the app."
        )
        return
    st.caption("Questions and answers are written by Gemini AI and can contain mistakes. "
               "Check important answers (especially numericals) with your NCERT textbook.")
    col1, col2, col3 = st.columns(3)
    difficulty = col1.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Tricky"], index=2)
    marks = col2.selectbox("Marks", ["Mixed"] + MARKS_CHOICES)
    n = col3.slider("How many questions", 3, 10, 5)
    with st.expander("Advanced: choose the Gemini model"):
        found = discover_models(key)
        model_pick = st.selectbox("Model", ["Auto (recommended)"] + found)
    model = None if model_pick.startswith("Auto") else model_pick

    if st.button("✨ Generate questions", type="primary"):
        with st.status("Gemini is writing your questions...", expanded=True) as status:
            fresh, skipped, err = collect(ch_id, difficulty, n, marks, key, model, status)
            status.update(label="Done" if fresh else "Failed", state="complete" if fresh else "error")
        if err:
            st.error(err)
        elif not fresh:
            st.error("No new questions came back. Please try again.")
        else:
            st.session_state["ai_last"] = (ch_id, fresh)
            if skipped:
                st.info(f"{skipped} repeated or malformed question(s) were left out.")

    last = st.session_state.get("ai_last")
    if last and last[0] == ch_id:
        st.divider()
        st.subheader("Your new questions")
        show_questions(last[1], label_ai=True)

    with st.expander("📚 Bulk builder: collect up to 100 questions for this chapter"):
        bulk_view(ch_id, difficulty, marks, key, model)


# ----------------------------------------------------------------------- main
st.title("⚛️ CBSE Class XI Physics (NCERT)")
st.caption(f"Created by **{AUTHOR}**")

part = st.sidebar.radio("Choose a part", ["1. Key words", "2. Practice questions", "3. AI question generator"])
ch_id = st.sidebar.selectbox(
    "Chapter", list(CHAPTERS), format_func=lambda n: f"{n}. {CHAPTERS[n]['name']}",
)
st.sidebar.divider()
st.sidebar.markdown(f"✍️ **Created by {AUTHOR}**")

st.caption(f"Chapter {ch_id}: {CHAPTERS[ch_id]['name']}")
if part.startswith("1"):
    keywords_view(ch_id)
elif part.startswith("2"):
    practice_view(ch_id)
else:
    ai_view(ch_id)

st.divider()
st.caption(f"© {AUTHOR} · CBSE Class XI Physics (NCERT)")
