# quantum-bb84

Project located in Jovian : https://jovian.ai/zacaria/quantumbb84tp

## Implementation of quantum-bb84

### Features :

- bb84 implementation
- teleportation of qubit between alice and bob
- eve intercepting the communication and sending a new qubit
- DEBUG global (on top of notebook) : enables to add more insight of what happens through the code. Make sure to reduce the number of qubit sent to not overload memory
- DEFAULT_TIMES global (on top of notebook) : controls the number of shot to run a simulation to a get a measurement
- use only one circuit which is cleaned before each qubit transmission
- you can unitary test each function on each block by changing the code under the "#TESTS ----" line
