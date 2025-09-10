# 25BC+25CD block training.

from pyControl.utility import *
import hardware_definition as hw

# States and events.

states = [
    "init_trial",
    "choice_state_b",
    "choice_state_c",
    "correct_sound",
    "error_sound",
    "reward_b",
    "reward_c",
    "punishment",
    "inter_trial_interval",
]

events = [
    "B_poke",
    "INI_poke",
    "C_poke",
    "D_poke",
    "trial_count", 
]

initial_state = "init_trial"

my_sampler = Sample_without_replacement(['b','c'])

# Parameters.

# v.session_duration = 1 * hour  # Session duration.
v.trial_num = 51  # Total trial number.
v.audio_durations = [200]
v.ini_duration = [50]
v.reward_durations = [80]  # Reward delivery duration (ms).
v.ITI_duration = 3 * second  # Inter-trial interval duration.
v.timeout_duration = 5 * second  # Timeout duration after an error.
v.next_sample =["a"]

# Variables.

v.n_rewards = 0  # Number of rewards obtained.
v.n_trials = 0  # Number of trials received.
v.choice = "Initiation"

# Non-state machine code.      
    
# Print trial information.
print_variables(["n_trials", "n_rewards", "choice"])

# Run start and stop behaviour.

def run_end():
    # Turn off all hardware outputs.
    hw.off()

# State behaviour functions.

def init_trial(event):
    # Turn on Initiation Port LED and wait for poke.
    if event == "entry":
        hw.P_Init.LED.on()
        v.n_trials += 1
        print("Trial number {}".format(v.n_trials))
    elif event == "exit":
        hw.P_Init.LED.off()
        hw.P_Init.SOL.off()
    elif event == "INI_poke":
        hw.P_Init.SOL.on()
        if v.n_trials <= 25:
            timed_goto_state("choice_state_b", v.ini_duration[0])
        else:
            timed_goto_state("choice_state_c", v.ini_duration[0]) 

        
def choice_state_b(event):  # B vs C
    # Wait for poke.
    if event == "entry":
        hw.P_B.LED.on()
        hw.P_C.LED.on()
        print("Choice B vs C")
    elif event == "exit":
        hw.P_B.LED.off()
        hw.P_C.LED.off()
    elif event == "B_poke":
        v.choice = "B"
        print("Correct")
        goto_state("correct_sound")
    elif event == "C_poke":
        print("Error")
        goto_state("error_sound")
        v.choice = "C"
        goto_state("error_sound")

def choice_state_c(event):  # C vs D
    # Wait for poke.
    if event == "entry":
        hw.P_C.LED.on()
        hw.P_D.LED.on()
        print("Choice C vs D")
    elif event == "exit":
        hw.P_C.LED.off()
        hw.P_D.LED.off()
    elif event == "C_poke":
        v.choice = "C"
        print("Correct")
        goto_state("correct_sound")
    elif event == "D_poke":
        print("Error")
        goto_state("error_sound")
        v.choice = "D"
        goto_state("error_sound")

def correct_sound(event):
    if event == "entry":
        if v.choice == "B":
            timed_goto_state("reward_b", v.audio_durations[0])
        elif v.choice == "C":
            timed_goto_state("reward_c", v.audio_durations[0])
            
        hw.Speaker.set_volume(90)
        hw.Speaker.sine(2500)
    elif event == "exit":
        hw.Speaker.off()

def error_sound(event):
    if event == "entry":
        timed_goto_state("punishment", v.audio_durations[0])
        hw.Speaker.set_volume(90)
        hw.Speaker.noise(10000)
    elif event == "exit":
        hw.Speaker.off()


def reward_b(event):
    # Deliver reward to Port B.
    if event == "entry":
        timed_goto_state("inter_trial_interval", v.reward_durations[0])
        hw.P_B.SOL.on()
        v.n_rewards += 1

    elif event == "exit":
        hw.P_B.SOL.off()

def reward_c(event):
    # Deliver reward to Port C.
    if event == "entry":
        timed_goto_state("inter_trial_interval", v.reward_durations[0])
        hw.P_C.SOL.on()
        v.n_rewards += 1

    elif event == "exit":
        hw.P_C.SOL.off()

def punishment(event):
    # Extend inter-trial interval for timeout punishment.
    if event == "entry":
        timed_goto_state("inter_trial_interval", v.timeout_duration)

def inter_trial_interval(event):
    # Go to init trial after specified delay.
    if event == "entry":
        timed_goto_state("init_trial", v.ITI_duration)

# State independent behaviour.

def all_states(event):
    if v.n_trials == v.trial_num:
        stop_framework()
     
