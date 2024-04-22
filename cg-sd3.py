import gradio as gr
import requests
import datetime
import os
sStr="photographic"
aStr="1:1"
fStr="png"
model="core"

def rs_change(c):
    global sStr
    sStr=c
    return gr.Dropdown(choices=choices[c], interactive=True) # Make it interactive as it is not by default

def aspect_change(c):
    global aStr
    aStr=c
    return gr.Dropdown(choices=choices[c], interactive=True) # Make it interactive as it is not by default

def format_change(c):
    global fStr
    fStr=c
    return gr.Dropdown(choices=choices[c], interactive=True) # Make it interactive as it is not by default

def model_change(value):
    global model
    if(value=="Core"):
        model="core"
        return
    model="sd3"
    return
    
def respond(msg, history):
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/{model}",
        headers={
            "authorization": f"Bearer sk-cYM2C9F0wxieJh8DhSmSAX6C8A9N72YwAobrPA1dnnePI80r",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": msg,
            "aspect_ratio": aStr,
            "style_preset": sStr,
            "output_format": fStr,
        },
    )

    if response.status_code == 200:
        now = datetime.datetime.now()
        date_str = now.strftime("%d%m%Y")

        # Get the current working directory
        current_dir = os.getcwd()

        # Create the "output" directory if it doesn't exist
        output_dir = os.path.join(current_dir, "output/")
        os.makedirs(output_dir, exist_ok=True)
        
        # Find the next available sequential number
        file_count = 0
        while True:
            filename = f"{output_dir}{date_str}-{file_count}.{fStr}"
            if not os.path.exists(filename):
                break  # Found an unused filename
            file_count += 1

        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))


#    # Construct the full path to the output file
#    image_path = os.path.join(output_dir, filename)

#    image_path = '/media/drkeithcox/DevDrive/onedrive/dev/code/gradiobot/'+filename  # Or get image data
    return filename

with gr.Blocks(title="Professor Cosmic's SD3 Tester") as demo:    
    gr.Markdown("# **Professor Cosmic's SD3 Tester**")
    mBtn=gr.Radio(choices=["Core", "SD-3"], label="Model")
    mBtn.change(model_change, inputs=mBtn)
    msg = gr.Textbox(label="Prompt", interactive=True)
#    msg.submit(respond, msg, msg)
    with gr.Row():
        sBox=gr.Dropdown(
            ["3d-model", "analog-film", "anime", "cinematic", "comic-book", "digital-art", "enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound", "neon-punk", "origami", "photographic", "pixel-art", "tile-texture"], label="Style Preset"
        )
        sBox.select(fn=rs_change, inputs=sBox)
        aBox=gr.Dropdown(
            ["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"], label="Aspect"
        )
        aBox.select(fn=aspect_change, inputs=aBox)
        fBox=gr.Dropdown(
            ["jpeg", "png", "webp"], label="Format"
        )
        fBox.select(fn=format_change, inputs=fBox)
       
    imageDisplay=gr.Image()
    button = gr.Button("Show Image")
    button.click(respond, msg, outputs=imageDisplay)

print("Gradio version "+gr. __version__) 
print("requests version "+requests. __version__)
demo.launch()