import os
import datetime
import random
import gradio as gr
from glob import glob
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
        "--out_folder",
        default="./evaluation_results",
        type=str,
        help="Folder to save evaluation result per user",
    )

parser.add_argument(
        "--out_file",
        default="./annotation.csv",
        type=str,
        help="File to save evaluation result",
    )

parser.add_argument(
        "--sample_A",
        default="/home/hawau/Documents/projects/evaluation/artst_arvoice_evaluation/wo_d/",
        type=str,
        required=True,
        help="Absolute path to samples from experiment A",
    )

parser.add_argument(
        "--sample_B",
        default="/home/hawau/Documents/projects/evaluation/arvoice_h_r_wd_prolific/",
        type=str,
        required=True,
        help="Absolute path to samples from experiment B",
    )

args = parser.parse_args()

def shuffle_indices(list1, list2, num_swaps=None):
    if num_swaps is None:
        num_swaps = random.randint(1, len(list1))  # Random number of swaps
    
    indices = random.sample(range(len(list1)), num_swaps)  # Select random indices

    for i in indices:
        list1[i], list2[i] = list2[i], list1[i]  # Swap elements

    return list1, list2

out_folder = args.out_folder
out_file = args.out_file

os.makedirs(out_folder, exist_ok=True)

generated_w_diacritics = list(glob(args.sample_A + "/*.wav"))
generated_w_diacritics.sort()

generated_wo_diacritics = list(glob(args.sample_B + "/*.wav"))
generated_wo_diacritics.sort()

w_d, wo_d = shuffle_indices(generated_w_diacritics, generated_wo_diacritics, 10)

assert len(w_d) > 0, "Number of samples must be greater than 0."

assert len(w_d) == len(wo_d), "Lengths of samples in the two experiments must be equal"

all_samples = list(zip(w_d, wo_d))

index = 0
sample_a = ""
sample_b = ""

def load_data():
    global index, all_samples, sample_a, sample_b
    index = 0
    sample_a = all_samples[index][0]
    sample_b = all_samples[index][1]

def next():
    global index,sample_a,sample_b
    index += 1
    if index >= len(all_samples):
        index = 0
        return gr.Info("Test Completed! Please close the browser to exit. Completion Code: C103IYNJ", duration=50),None,None,gr.Button("Click here to submit completion code", link="https://app.prolific.com/submissions/complete?cc=C103IYNJ", )
    
    sample_a = all_samples[index][0]
    sample_b = all_samples[index][1]
    return all_samples[index][0], all_samples[index][1], gr.Radio(value=None), gr.Button(visible=False)

def begin_session(name, speaks_arabic, gender): 
    load_data()
    global index, all_samples, sample_a, sample_b, out_folder, out_file
    out_file = f"{out_folder}/{name.replace(' ','')}_{speaks_arabic}_{gender}_eval.txt"
    if not os.path.exists(out_file):
        os.system(f"touch {out_file}")
        done = 0
    
    else:
        with open(out_file, "r") as f:
            done = len(f.readlines())
            if done >= len(all_samples):
                return gr.Info("Completed!\nIf you haven't completed try using a different name"),None,None,None
    
    index = done
    sample_a, sample_b = all_samples[index]
    
    return gr.Column(visible=False), gr.Column(visible=True),\
        sample_a, sample_b


def new_sample(choice):
    global index,sample_a,sample_b,out_file
    out = open(out_file, "a")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{choice},{sample_a},{sample_b},{time}", file=out)
    out.close()
    return next()

if __name__ == "__main__":
    demo = gr.Blocks(theme=gr.themes.Glass())
    
    with demo:
        gr.Markdown("""## Preference Test \n
        """)
        
        with gr.Column() as recorder_details:
            gr.Markdown('<h3> Give some demography details to begin.</h3>')
            with gr.Row():
                recorder_name = gr.Textbox(label="Evaluator Name / Prolific Id ", placeholder="EnterYourName")    
                recorder_dialect = gr.Radio(["yes", "no"], label="Native Arabic Speaker")
                gender = gr.Radio(
                    ["Female", "Male"], label="Gender"
                )
            begin_session_btn = gr.Button("Begin Evaluating", variant="primary",visible=True)
        
        with gr.Column(visible=False) as evaluate_block:
        
            with gr.Row():
                aud_1 = gr.Audio(value="./test_spkr_0.wav", type="filepath", label="Sample A", autoplay=False)
                aud_2 = gr.Audio(value="./test_spkr_0.wav", type="filepath", label="Sample B", autoplay=False)
            
            choice = gr.Radio(["A is better", "B is better", "Both are same"], label="Preference",type="value", info="Which audio sample do you prefer?")
            btn_1 = gr.Button("Next", visible=False)
            
            choice.input(lambda x: gr.Button("Next", visible=True), outputs=[btn_1])
            
            btn_1.click(new_sample,[choice],[aud_1, aud_2, choice, btn_1])

            begin_session_btn.click(begin_session, [recorder_name, recorder_dialect, gender], \
                                outputs=[recorder_details, evaluate_block, aud_1, aud_2])
        
    demo.launch(share=True, allowed_paths=["/"])
