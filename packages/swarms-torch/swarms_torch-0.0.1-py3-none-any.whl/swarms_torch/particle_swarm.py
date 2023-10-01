import torch

class ParticleSwarmOptimization:
    def __init__(self, goal, n_particles=100, inertia=0.5, personal_best_weight=1.5, global_best_weight=1.5):
        self.goal = torch.tensor([ord(c) for c in goal])
        self.n_particles = n_particles
        self.inertia = inertia
        self.personal_best_weight = personal_best_weight
        self.global_best_weight = global_best_weight
        
        self.particles = torch.randint(0, 255, (n_particles, len(goal)))
        self.velocities = torch.zeros((n_particles, len(goal)))
        
        self.personal_best = self.particles.clone()
        self.global_best = self.particles[0].clone()

    def compute_fitness(self, particle):
        return 1.0 / (1.0 + torch.norm((particle - self.goal).float()))

    def update(self):
        for i in range(self.n_particles):
            fitness = self.compute_fitness(self.particles[i])
            personal_best_fitness = self.compute_fitness(self.personal_best[i])
            
            if fitness > personal_best_fitness:
                self.personal_best[i] = self.particles[i]
            
            global_best_fitness = self.compute_fitness(self.global_best)
            if fitness > global_best_fitness:
                self.global_best = self.particles[i]

            # Update velocity
            personal_attraction = self.personal_best_weight * torch.rand(self.goal.size()) * (self.personal_best[i] - self.particles[i])
            global_attraction = self.global_best_weight * torch.rand(self.goal.size()) * (self.global_best - self.particles[i])
            
            self.velocities[i] = self.inertia * self.velocities[i] + personal_attraction + global_attraction
            
            # Update position
            self.particles[i] += self.velocities[i].int()
            self.particles[i].clamp_(0, 255)

    def optimize(self, iterations):
        for _ in range(iterations):
            self.update()
            best_particle = self.global_best
            print("Best Particle: ", ''.join([chr(int(i)) for i in best_particle]))

# Test
pso = ParticleSwarmOptimization(goal="Attention is all you need", n_particles=100)
pso.optimize(iterations=1000)
