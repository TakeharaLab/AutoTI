# This hardware definition specifies that 3 pokes are plugged into ports 1-3 and a speaker into
# port 4 of breakout board version 1.2.  The houselight is plugged into the center pokes solenoid socket.

from devices import *

board = Breakout_1_2()

# Instantiate Devices.

Speaker = Audio_board(board.port_4)

P_Init = Poke(board.port_5, rising_event="INI_poke", falling_event="INI_poke_out")

port_exp = Port_expander(board.port_3)
P_A = Poke(port=port_exp.port_1, rising_event="A_poke", falling_event="A_poke_out")
P_B = Poke(port=port_exp.port_2, rising_event="B_poke", falling_event="B_poke_out")
P_C = Poke(port=port_exp.port_3, rising_event="C_poke", falling_event="C_poke_out")
P_D = Poke(port=port_exp.port_4, rising_event="D_poke", falling_event="D_poke_out")
P_E = Poke(port=port_exp.port_5, rising_event="E_poke", falling_event="E_poke_out")


