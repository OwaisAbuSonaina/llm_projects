import os
import io
import sys
import ast
import subprocess
import re
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from system_info import retrieve_system_info

# Load environment variables
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize clients
openai_client = OpenAI(api_key=openai_api_key)
gemini_client = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# Define models 
OPENAI_MODEL = "gpt-4o" 
GEMENI_MODEL = "gemini-3.1-flash-lite"


system_info = retrieve_system_info()

# Default Python benchmark code
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


def fetch_system_commands():
    """Fetches compiler and execution commands tailored to the host system."""
    message = f"""
    Here is a report of the system information for my computer.
    I want to run a C++ compiler to compile a single C++ file called main.cpp and then execute it in the simplest way possible.
    Please tell me exactly what I should use for the compile_command and run_command to achieve the fastest runtime.
    
    IMPORTANT NOTE: Make your answer ONLY in the following way (without any markdown formatting or extra text):
    compile_command = ["g++", "main.cpp", "-O3", "-march=native", "-flto", "-pipe", "-std=c++20", "-s", "-o", "main"]
    run_command = ["./main"]

    System Information:
    {system_info}
    """
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL, 
        messages=[{"role": "user", "content": message}]
    )
    raw_reply = response.choices[0].message.content.strip()
    
    # Strip backticks/fences and normalize line endings
    cleaned_reply = raw_reply.replace('```python', '').replace('```', '').replace('\r', '').strip()
    
    # Extract the bracketed lists specifically using regex
    comp_match = re.search(r'compile_command\s*=\s*(\[.*?\])', cleaned_reply, re.DOTALL)
    run_match = re.search(r'run_command\s*=\s*(\[.*?\])', cleaned_reply, re.DOTALL)
    
    if not comp_match or not run_match:
        return f"Could not match commands in reply:\n{raw_reply}", ""
        
    try:
        comp_cmd = ast.literal_eval(comp_match.group(1).strip())
        run_cmd = ast.literal_eval(run_match.group(1).strip())
    except Exception as e:
        return f"Error evaluating parsed lists: {e}\nRaw reply:\n{raw_reply}", ""
        
    return str(comp_cmd), str(run_cmd)

def execute_python(code):
    """Executes the Python code to establish a benchmark baseline."""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        # Pass basic builtins so things like print() and time work naturally
        exec(code, {"__builtins__": __builtins__})
    except Exception as e:
        print(f"Python Error: {e}")
    sys.stdout = old_stdout
    return redirected_output.getvalue()

def port_and_run(llm_choice, python_code, comp_cmd_str, run_cmd_str):
    """Ports Python to C++, writes to disk, compiles, and executes."""
    if not comp_cmd_str or not run_cmd_str:
        return "Commands missing. Fetch them in Step 1 first.", "N/A"
        
    try:
        compile_command = ast.literal_eval(comp_cmd_str)
        run_command = ast.literal_eval(run_cmd_str)
    except Exception as e:
        return f"Invalid command format: {e}", "N/A"
        
    client = openai_client if llm_choice == "OpenAI" else gemini_client
    model = OPENAI_MODEL if llm_choice == "OpenAI" else GEMENI_MODEL
    
    system_prompt = "Your task is to convert Python code into high performance C++ code. Respond only with C++ code. Do not provide any explanation other than occasional comments. The C++ response needs to produce an identical output in the fastest possible time."
    
    user_prompt = f"""Port this Python code to C++ with the fastest possible implementation that produces identical output in the least time.
System info: {system_info}
Compile command: {compile_command}
Respond only with C++ code.
Python code:
```python
{python_code}
```"""
    
    # Configure request payload
    kwargs = {
        "model": model, 
        "messages": [
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_prompt}
        ]
    }
    
    # Handle specific model reasoning parameters if necessary
    # if "gpt" in model:
    #     kwargs["reasoning_effort"] = "high"
        
    try:
        response = client.chat.completions.create(**kwargs)
        cpp_code = response.choices[0].message.content
        # Clean up markdown formatting
        cpp_code = cpp_code.replace('```cpp', '').replace('```', '').strip()
    except Exception as e:
        return f"LLM Error: {e}", "N/A"
        
    # Write to disk
    with open("main.cpp", "w", encoding="utf-8") as f:
        f.write(cpp_code)
        
    # Compile
    try:
        subprocess.run(compile_command, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return cpp_code, f"Compilation failed:\n{e.stderr}"
        
    # Run
    try:
        run_res = subprocess.run(run_command, check=True, text=True, capture_output=True)
        return cpp_code, run_res.stdout
    except subprocess.CalledProcessError as e:
        return cpp_code, f"Execution failed:\n{e.stderr}"

# --- UI Layout ---
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

    # Wire up the event listeners
    fetch_btn.click(fn=fetch_system_commands, outputs=[comp_cmd_out, run_cmd_out])
    py_run_btn.click(fn=execute_python, inputs=[py_input], outputs=[py_out])
    port_btn.click(
        fn=port_and_run, 
        inputs=[llm_selector, py_input, comp_cmd_out, run_cmd_out], 
        outputs=[cpp_out_code, cpp_out_result]
    )
    
if __name__ == '__main__':
    app.launch(inbrowser=True)