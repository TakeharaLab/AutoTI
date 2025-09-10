# 50 AB training.

from pyControl.utility import *
import hardware_definition as hw

# States and events.

states = [
    "init_trial",
    "choice_state",
    "correct_sound",
    "error_sound",
    "reward",
    "punishment",
    "inter_trial_interval",
]

events = [
    "A_poke",
    "INI_poke",
    "B_poke",
    "trial_count",
]

initial_state = "init_trial"

# Parameters.

# v.session_duration = 1 * hour  # Session duration.
v.trial_num = 51  # Total trial number.
v.ini_duration = [50]
v.audio_durations = [200]
v.reward_durations = [120]  # Reward delivery duration (ms).
v.ITI_duration = 3 * second  # Inter-trial interval duration.
v.timeout_duration = 5 * second  # Timeout duration after an error.

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
        timed_goto_state("choice_state", v.ini_duration[0])

def choice_state(event):
    # Wait for poke.
    if event == "entry":
        hw.P_A.LED.on()
        hw.P_B.LED.on()
        print("Choice A vs B")
    elif event == "exit":
        hw.P_A.LED.off()
        hw.P_B.LED.off()
    elif event == "A_poke":
        v.choice = "A"
        print("Correct")
        goto_state("correct_sound")
    elif event == "B_poke":
        print("Error")
        goto_state("error_sound")
        v.choice = "B"

def correct_sound(event):
    if event == "entry":
        timed_goto_state("reward", v.audio_durations[0])
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

def reward(event):
    # Deliver reward to Port A.
    if event == "entry":
        timed_goto_state("inter_trial_interval", v.reward_durations[0])
        hw.P_A.SOL.on()
        v.n_rewards += 1

    elif event == "exit":
        hw.P_A.SOL.off()

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
     
