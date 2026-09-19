import gradio as gr

from engine import port_and_run, fetch_system_commands, execute_python

pi_code = """import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result

start_time = time.time()
result = calculate(200_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time: {(end_time - start_time):.6f} seconds")
"""



with gr.Blocks(title="Python to C++ Translator", theme=gr.themes.Monochrome()) as app:
    gr.Markdown("# Python to C++ High-Performance Porting")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Step 1: System Commands")
            gr.Markdown("Query the LLM to get the optimized compile and execution commands for your specific hardware.")
            fetch_btn = gr.Button("Get Compile & Run Commands")
            comp_cmd_out = gr.Textbox(label="Compile Command (List format)")
            run_cmd_out = gr.Textbox(label="Run Command (List format)")
            
        with gr.Column():
            gr.Markdown("### Step 2: Source Code")
            gr.Markdown("Define your Python logic and execute it to get a baseline timing.")
            py_input = gr.Code(label="Python Code", language="python", value=pi_code)
            py_run_btn = gr.Button("Test Python Code")
            py_out = gr.Textbox(label="Python Output & Benchmark")
            
    gr.Markdown("---")
    gr.Markdown("### Step 3: Port, Compile & Compare")
    
    with gr.Row():
        llm_selector = gr.Radio(["OpenAI", "Gemini"], label="Select LLM for Porting", value="OpenAI")
        port_btn = gr.Button("Port to C++, Compile & Run", variant="primary")
        
    with gr.Row():
        cpp_out_code = gr.Code(label="Generated C++ Code", language="cpp")
        cpp_out_result = gr.Textbox(label="C++ Execution Output")

    fetch_btn.click(fn=fetch_system_commands, outputs=[comp_cmd_out, run_cmd_out])
    py_run_btn.click(fn=execute_python, inputs=[py_input], outputs=[py_out])
    port_btn.click(
        fn=port_and_run, 
        inputs=[llm_selector, py_input, comp_cmd_out, run_cmd_out], 
        outputs=[cpp_out_code, cpp_out_result]
    )