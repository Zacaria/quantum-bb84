def state_to_bloch_vector(state, trials=10000):
    """Estimate a one-qubit state's Bloch vector using X, Y, and Z measurements."""
    from qiskit import Aer, QuantumCircuit, execute

    # Define a quantum circuit and initialize it with the desired state.
    circuit = QuantumCircuit(1, 1)
    circuit.initialize([state[0], state[1]], [0])

    # Prepare measurements over Z, X, and Y.
    measure_z = QuantumCircuit(1, 1)
    measure_z.measure(0, 0)

    measure_x = QuantumCircuit(1, 1)
    measure_x.h(0)
    measure_x.measure(0, 0)

    measure_y = QuantumCircuit(1, 1)
    measure_y.sdg(0)
    measure_y.h(0)
    measure_y.measure(0, 0)

    bloch_vector = []
    for measure_circuit in [measure_x, measure_y, measure_z]:
        counts = execute(
            circuit.compose(measure_circuit),
            Aer.get_backend("qasm_simulator"),
            shots=trials,
        ).result().get_counts()
        probabilities = {
            output: counts.get(output, 0) / trials for output in ["0", "1"]
        }
        bloch_vector.append(probabilities["0"] - probabilities["1"])

    return bloch_vector


def draw_and_plot_state(circuit):
    """Display a circuit and the Bloch vectors of its statevector."""
    from IPython.display import display
    from qiskit import Aer, execute
    from qiskit.visualization import plot_bloch_multivector

    display(circuit.draw(output="mpl"))
    simulator = Aer.get_backend("statevector_simulator")
    result = execute(circuit, backend=simulator, shots=1000).result()
    output_vector = result.get_statevector(circuit)
    display(plot_bloch_multivector(output_vector))


def console_print(*message):
    print("\n ----------------------------------------------------------------- \n$ ", *message)


def filter_none(array):
    return list(filter(lambda element: element is not None, array))


def int_array_to_str(array):
    return "".join(str(bit) for bit in array)
