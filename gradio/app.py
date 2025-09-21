import gradio as gr
import time
import json
import random
from prompt_engineering.prompt_template import Patient_Summary_System
PSS = Patient_Summary_System()

css = """
.gradio-container p {
    font-family: 'Arial', sans-serif;
}
"""


if __name__ == "__main__":


    with gr.Blocks(theme=gr.themes.Soft(),css=css) as demo:
        gr.Markdown(
            """
            #           🏥 Medical Health Report Summarizer
            
            ---
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("")
                fetch_btn = gr.Button(" Fetch Medical Report", variant="primary")
                report_box = gr.Code(label="Medical Report", language="json", interactive=False)

            with gr.Column(scale=1):
                gr.Markdown("")
                summarize_btn = gr.Button(" Generate Summary", variant="primary")
                output_box = gr.Markdown()

        # Status
        status = gr.Label(value="", label="Status")


        def fetch_with_loader():
            yield "", "⏳ Fetching medical report..."
            report = json.dumps(PSS.get_patient_data(url='http://localhost:8000/patient-app/api/patients/1/'))
            yield report, "✅ Report fetched successfully!"


        fetch_btn.click(
            fn=fetch_with_loader,
            inputs=None,
            outputs=[report_box, status]
        )


        def summarize_with_loader():
            yield "", "⏳ Summarizing report with AI..."
            summary = PSS.generate_summary(url='http://localhost:8000/patient-app/api/patients/1/')
            yield summary, "✅ Summary ready!"


        summarize_btn.click(
            fn=summarize_with_loader,
            inputs=None,
            outputs=[output_box, status]
        )


    demo.launch()
