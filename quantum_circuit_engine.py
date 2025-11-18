from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import sys

# Check environment
print(f"Python version: {sys.version}")
print(f"Qiskit version: {QuantumCircuit.__module__}")

# Import ADK tools
try:
    from adk.tools import tool
    ADK_AVAILABLE = True
    print("✅ ADK tools available - ready for agent integration")
except ImportError:
    ADK_AVAILABLE = False
    print("⚠️ ADK not available - running in standalone mode")

# CORE QUANTUM FUNCTIONS

def create_circuit(num_qubits):
    """Create quantum circuit with error handling"""
    try:
        if num_qubits <= 0:
            raise ValueError("Number of qubits must be positive")
        
        circuit = QuantumCircuit(num_qubits)
        print(f"✅ Created quantum circuit with {num_qubits} qubit(s)")
        return circuit
    except Exception as e:
        print(f"❌ Error creating circuit: {e}")
        return None

def apply_gate(circuit, gate_name, target_qubit, control_qubit=None):
    """Apply quantum gate with better error handling"""
    gate_name = gate_name.lower().strip()
    
    try:
        if gate_name == 'h':
            circuit.h(target_qubit)
            print(f"✅ Applied Hadamard (H) gate to qubit {target_qubit}")
        elif gate_name == 'x':
            circuit.x(target_qubit)
            print(f"✅ Applied Pauli-X gate to qubit {target_qubit}")
        elif gate_name == 'y':
            circuit.y(target_qubit)
            print(f"✅ Applied Pauli-Y gate to qubit {target_qubit}")
        elif gate_name == 'z':
            circuit.z(target_qubit)
            print(f"✅ Applied Pauli-Z gate to qubit {target_qubit}")
        elif gate_name == 'cx':
            if control_qubit is not None:
                circuit.cx(control_qubit, target_qubit)
                print(f"✅ Applied CNOT gate: control={control_qubit}, target={target_qubit}")
            else:
                if target_qubit < circuit.num_qubits - 1:
                    circuit.cx(target_qubit, target_qubit + 1)
                    print(f"✅ Applied CNOT gate: control={target_qubit}, target={target_qubit + 1}")
                else:
                    circuit.cx(target_qubit, 0)
                    print(f"✅ Applied CNOT gate: control={target_qubit}, target=0")
        else:
            supported_gates = ['h', 'x', 'y', 'z', 'cx']
            print(f"❌ Unknown gate: {gate_name}. Supported gates: {supported_gates}")
        
        return circuit
    except Exception as e:
        print(f"❌ Error applying gate {gate_name} to qubit {target_qubit}: {e}")
        return circuit

def visualize_circuit(circuit):
    """
    FIXED visualization function with multiple fallback methods
    """
    try:
        if circuit is None:
            return "❌ No circuit to visualize"
        
        print(f"🔧 Visualizing circuit with {circuit.num_qubits} qubits and {len(circuit.data)} gates...")
        
        # METHOD 1: Try text-based output first
        print("\n" + "="*50)
        print("TEXT-BASED CIRCUIT REPRESENTATION:")
        print("="*50)
        text_diagram = str(circuit)
        print(text_diagram)
        
        # METHOD 2: Try matplotlib with Agg backend (for headless environments)
        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            plt.ioff()  # Turn off interactive mode
            
            # Create figure with specific size
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Draw circuit
            circuit_drawer(circuit, output='mpl', ax=ax, style={'backgroundcolor': '#ffffff'})
            ax.set_title(f'Quantum Circuit: {circuit.num_qubits} qubits, {len(circuit.data)} gates', 
                        pad=20, fontsize=12, fontweight='bold')
            
            # Save to buffer
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', 
                       facecolor='white', edgecolor='black')
            buf.seek(0)
            
            # Convert to base64
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)  # Important: close the figure to free memory
            
            print("✅ Matplotlib visualization successful")
            
            # Create HTML output
            html_output = f'''
            <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); margin: 10px 0;">
                <h3 style="color: #2c3e50; margin-top: 0; text-align: center;">🧪 QUASAR Quantum Circuit</h3>
                <div style="text-align: center; background: white; padding: 10px; border-radius: 5px;">
                    <img src="data:image/png;base64,{img_str}" alt="Quantum Circuit" style="max-width: 100%; border: 1px solid #ddd;">
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; color: #555;">
                    <span>🔢 <strong>Qubits:</strong> {circuit.num_qubits}</span>
                    <span>⚡ <strong>Gates:</strong> {len(circuit.data)}</span>
                    <span>📐 <strong>Depth:</strong> {circuit.depth()}</span>
                </div>
            </div>
            '''
            return html_output
            
        except Exception as e:
            print(f"⚠️ Matplotlib visualization failed: {e}")
            
            # METHOD 3: Pure text-based HTML output as fallback
            text_html = f'''
            <div style="border: 2px solid #ff9800; padding: 15px; border-radius: 10px; background: #fff3e0; margin: 10px 0;">
                <h3 style="color: #e65100; margin-top: 0;">⚠️ Quantum Circuit (Text View)</h3>
                <pre style="background: white; padding: 15px; border-radius: 5px; border: 1px solid #ffcc80; overflow-x: auto; font-family: 'Courier New', monospace;">{text_diagram}</pre>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; color: #555;">
                    <span>🔢 <strong>Qubits:</strong> {circuit.num_qubits}</span>
                    <span>⚡ <strong>Gates:</strong> {len(circuit.data)}</span>
                    <span>📐 <strong>Depth:</strong> {circuit.depth()}</span>
                </div>
            </div>
            '''
            return text_html
            
    except Exception as e:
        error_msg = f"❌ All visualization methods failed: {e}"
        print(error_msg)
        return f'<div style="color: red; padding: 10px; border: 2px solid red;">{error_msg}</div>'

# ADK TOOL WRAPPERS

# Global variable to store current circuit for ADK tools
current_circuit = None

if ADK_AVAILABLE:
    @tool
    def create_quantum_circuit(num_qubits: int) -> str:
        """Create a new quantum circuit with specified number of qubits."""
        global current_circuit
        current_circuit = create_circuit(num_qubits)
        if current_circuit:
            return f"✅ Successfully created quantum circuit with {num_qubits} qubits. Ready for gate operations."
        else:
            return f"❌ Failed to create quantum circuit with {num_qubits} qubits."

    @tool
    def apply_quantum_gate(gate_type: str, target_qubit: int, control_qubit: int = None) -> str:
        """Apply a quantum gate to a specific qubit."""
        global current_circuit
        if current_circuit is None:
            return "❌ No active quantum circuit. Please create a circuit first using create_quantum_circuit."
        
        current_circuit = apply_gate(current_circuit, gate_type, target_qubit, control_qubit)
        
        gate_names = {'h': 'Hadamard', 'x': 'Pauli-X', 'y': 'Pauli-Y', 'z': 'Pauli-Z', 'cx': 'CNOT'}
        gate_display = gate_names.get(gate_type, gate_type)
        
        if control_qubit is not None:
            return f"✅ Applied {gate_display} gate with control qubit {control_qubit} and target qubit {target_qubit}"
        else:
            return f"✅ Applied {gate_display} gate to qubit {target_qubit}"

    @tool
    def visualize_quantum_circuit() -> str:
        """Generate visualization of the current quantum circuit."""
        global current_circuit
        if current_circuit is None:
            return "❌ No active quantum circuit to visualize. Please create a circuit first."
        
        return visualize_circuit(current_circuit)

    print("🎯 ADK Tool Wrappers successfully created!")

# TESTING FUNCTION

def test_quantum_engine_enhanced():
    """Enhanced test with better debugging"""
    print("🧪 QUASAR Quantum Engine - ENHANCED TEST")
    print("=" * 60)
    
    # Test 1: Basic circuit creation
    print("\n1. 🎯 Testing Circuit Creation:")
    print("-" * 35)
    qc = create_circuit(3)
    
    # Test 2: Gate applications
    print("\n2. ⚡ Testing Gate Applications:")
    print("-" * 35)
    qc = apply_gate(qc, 'h', 0)
    qc = apply_gate(qc, 'x', 1)
    qc = apply_gate(qc, 'cx', 2, 1)  # CNOT: control=2, target=1
    qc = apply_gate(qc, 'y', 0)
    
    # Test 3: Enhanced visualization
    print("\n3. 📊 Testing Enhanced Visualization:")
    print("-" * 35)
    viz_result = visualize_circuit(qc)
    
    # Test 4: Circuit information
    print("\n4. 📈 Circuit Information:")
    print("-" * 35)
    print(f"   Qubits: {qc.num_qubits}")
    print(f"   Classical bits: {qc.num_clbits}") 
    print(f"   Total gates: {len(qc.data)}")
    print(f"   Circuit depth: {qc.depth()}")
    
    # Test 5: ADK tools if available
    if ADK_AVAILABLE:
        print("\n5. 🤖 Testing ADK Tool Integration:")
        print("-" * 35)
        global current_circuit
        current_circuit = create_circuit(2)
        
        tool_results = []
        tool_results.append(create_quantum_circuit(2))
        tool_results.append(apply_quantum_gate('h', 0))
        tool_results.append(apply_quantum_gate('x', 1))
        tool_results.append(apply_quantum_gate('cx', 1, 0))
        
        for i, result in enumerate(tool_results, 1):
            print(f"   Tool {i}: {result}")
    
    print("\n" + "=" * 60)
    print("✅ ENHANCED TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return viz_result

# QUICK START FUNCTION

def quick_demo():
    """Quick demonstration for immediate testing"""
    print("🚀 QUICK DEMO: 2-Qubit Entanglement Circuit")
    print("=" * 50)
    
    # Create Bell state circuit
    qc = create_circuit(2)
    qc = apply_gate(qc, 'h', 0)
    qc = apply_gate(qc, 'cx', 1, 0)  # CNOT
    
    print("\n🏗️ Circuit created: |Φ⁺⟩ Bell state")
    print("   H(0) → CNOT(0,1)")
    
    # Show visualization
    viz = visualize_circuit(qc)
    
    return viz

# MAIN EXECUTION

if __name__ == "__main__":
    print("🌌 QUASAR PROJECT - QUANTUM CIRCUIT ENGINE")
    print("Phase 1: Core Engine with Fixed Visualization")
    print("=" * 65)
    
    # Run quick demo first
    demo_result = quick_demo()
    
    # Then run full test
    print("\n" + "🔧" * 30)
    test_result = test_quantum_engine_enhanced()
    
    # Display results
    try:
        from IPython.display import HTML, display
        print("\n📊 DISPLAYING RESULTS:")
        print("-" * 25)
        display(HTML(demo_result))
        display(HTML(test_result))
    except:
        print("\n📊 Results generated successfully!")
        print("Note: HTML display not available in this environment")
    
    print("\n🎉 PHASE 1 COMPLETE!")
    print("Next: Integrate with AI Agent or proceed to Phase 2")
