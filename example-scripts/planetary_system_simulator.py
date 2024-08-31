import argparse
import numpy as np
from manim import *
import random
class PlanetarySystem(Scene):
    def __init__(self, planets, duration, timestep, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.planets = planets
        self.duration = duration
        self.timestep = timestep
        self.G = 6.67430e-11  # Gravitational constant
        self.sun_mass = 1.989e30  # Mass of the Sun in kg

    def construct(self):
        # Create a VGroup to hold all celestial bodies
        celestial_bodies = VGroup()
        # Create and add the central star (Sun)
        sun = Dot(color=YELLOW, radius=0.05).move_to(ORIGIN)
        celestial_bodies.add(sun)
        # Create and add planets
        for planet in self.planets:
            planet_obj = Dot(color=planet['color'], radius=0.03).move_to(planet['initial_position'])
            planet['object'] = planet_obj
            celestial_bodies.add(planet_obj)
        self.add(celestial_bodies)
        # Create paths for planets
        paths = VGroup(*[
            TracedPath(planet['object'].get_center, stroke_opacity=0.8, stroke_color=planet['color'])
            for planet in self.planets
        ])
        self.add(paths)
        # Simulate planetary motion
        def update_planets(mob, dt):
            for planet in self.planets:
                r = np.array(planet['object'].get_center())
                # Calculate gravitational force from the Sun
                F = -self.G * self.sun_mass * planet['mass'] / np.linalg.norm(r)**3 * r
                # Update velocity and position
                planet['velocity'] += F / planet['mass'] * self.timestep
                new_pos = planet['object'].get_center() + planet['velocity'] * self.timestep
                planet['object'].move_to(new_pos)
        # Run the animation
        self.play(
            UpdateFromAlphaFunc(celestial_bodies, update_planets),
            run_time=self.duration,
            rate_func=linear
        )
def main():
    parser = argparse.ArgumentParser(description="""
    Planetary System Simulator
    This script uses Manim to simulate and visualize a planetary system. 
    You can specify the number of planets and their properties such as mass, 
    initial position, velocity, semi-major axis, and eccentricity.
    How to use:
    1. Specify the number of planets using the --num_planets argument.
    2. For each planet, provide its mass, semi-major axis, and eccentricity.
    3. Set the simulation duration and timestep.
    4. Choose the frame rate and resolution for the output animation.
    Example:
    python planetary_system_simulator.py --num_planets 3 
           --masses 1 0.5 0.3 
           --semi_major_axes 1 1.5 2 
           --eccentricities 0.1 0.2 0.3 
           --duration 10 
           --timestep 0.01 
           --frame_rate 30 
           --resolution 1080p
    """)
    parser.add_argument('--num_planets', type=int, required=True, help='Number of planets in the system')
    parser.add_argument('--masses', type=float, nargs='+', required=True, help='Masses of planets (in Earth masses)')
    parser.add_argument('--semi_major_axes', type=float, nargs='+', required=True, help='Semi-major axes of planet orbits (in AU)')
    parser.add_argument('--eccentricities', type=float, nargs='+', required=True, help='Eccentricities of planet orbits')
    parser.add_argument('--duration', type=float, required=True, help='Simulation duration (in years)')
    parser.add_argument('--timestep', type=float, required=True, help='Simulation timestep (in years)')
    parser.add_argument('--frame_rate', type=int, default=30, help='Frame rate of the output animation')
    parser.add_argument('--resolution', choices=['480p', '720p', '1080p'], default='1080p', help='Resolution of the output animation')
    args = parser.parse_args()
    # Validate input
    if args.num_planets != len(args.masses) or args.num_planets != len(args.semi_major_axes) or args.num_planets != len(args.eccentricities):
        raise ValueError("Number of planets must match the number of masses, semi-major axes, and eccentricities provided")
    # Convert units
    AU = 1.496e11  # 1 AU in meters
    year = 365.25 * 24 * 3600  # 1 year in seconds
    earth_mass = 5.97e24  # Earth mass in kg
    # Create planet objects
    planets = []
    colors = [RED, GREEN, BLUE, ORANGE, PURPLE, TEAL]  # Add more colors if needed
    for i in range(args.num_planets):
        # Calculate initial position and velocity based on orbital elements
        a = args.semi_major_axes[i] * AU
        e = args.eccentricities[i]
        # Random angle for initial position
        theta = random.uniform(0, 2*np.pi)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        # Calculate velocity (perpendicular to position vector)
        v = np.sqrt(6.67430e-11 * 1.989e30 * (2/r - 1/a))  # Use Sun's mass
        vx = -v * np.sin(theta)
        vy = v * np.cos(theta)
        planets.append({
            'mass': args.masses[i] * earth_mass,
            'initial_position': np.array([x, y, 0]) / (100 * AU),  # Scale down further for better visualization
            'velocity': np.array([vx, vy, 0]) / (100 * AU) * year,  # Scale velocity accordingly
            'color': random.choice(colors)
        })
    # Set up Manim configuration
    config.frame_rate = args.frame_rate
    config.pixel_height = int(args.resolution[:-1])
    config.pixel_width = int(16/9 * config.pixel_height)
    # Create and render the animation
    try:
        scene = PlanetarySystem(planets, args.duration, args.timestep / year)
        scene.render()
        print("Animation rendered successfully!")
    except Exception as e:
        print(f"An error occurred during rendering: {str(e)}")
if __name__ == "__main__":
    main()