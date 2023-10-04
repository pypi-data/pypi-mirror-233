import parmed as pmd
import json
import sys
from sys import platform
import mdtraj as md
import mdtraj.reporters
import random
import simtk.unit as u
from whole_nucleus_model import OpenNucleome

prob_P_dP = 0.2 # Transition probability from P to dP
prob_dP_P = 0.2 # Transition probability from dP to P
transition_freq = 4000
sampling_freq = 2000
dP_type = 6
P_type = 7
total_steps = 3000000

model = OpenNucleome(1.0, 0.1, 0.005, 1.0) # 1.0: temperature (LJ reduced unit);
                                           # 0.1: damping coefficient (LJ reduced unit);
                                           # 0.005: timestep (LJ reduced unit);
                                           # 1.0: mass_scale

PDB_file = "human.pdb" #The initial configuration

# Generate new elements and construct topology as well
# membrane_dynamics: True for including lamina dynamics, False for excluding lamina dynamics;
# membrane_bond: A file contains the lamina bond when membrane_dynamics is on.
model.create_system(PDB_file, flag_membrane = False, lam_bond = None)

# Add the default force field
model.load_default_settings()

index_spec_spec_potential = 6

#model.save_system("model_before_simulation_0.xml")

simulation = model.create_simulation(platform_type = "CPU") # Users can also use CPU, Reference, OpenCL.
simulation.context.setPositions(model.chr_positions)

print("Bonding potential:", simulation.context.getState(getEnergy=True, groups={10}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Softcore potential:", simulation.context.getState(getEnergy=True, groups={11}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Ideal(intra) potential:", simulation.context.getState(getEnergy=True, groups={12}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Compt-Compt potential:", simulation.context.getState(getEnergy=True, groups={13}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Hardwall:", simulation.context.getState(getEnergy=True, groups={21}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Nuc-Spec:", simulation.context.getState(getEnergy=True, groups={18}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Nuc-Nuc:", simulation.context.getState(getEnergy=True, groups={17}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Spec-Spec:", simulation.context.getState(getEnergy=True, groups={15}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Nuc-Chr:", simulation.context.getState(getEnergy=True, groups={19}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Spec-Chr:", simulation.context.getState(getEnergy=True, groups={16}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Chr-Lamina:", simulation.context.getState(getEnergy=True, groups={20}).getPotentialEnergy() / u.kilojoule_per_mole)
print("Inter:", simulation.context.getState(getEnergy=True, groups={14}).getPotentialEnergy() / u.kilojoule_per_mole)
