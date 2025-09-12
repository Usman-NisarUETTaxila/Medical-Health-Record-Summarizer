import gradio as gr
import time
import json
import random

def fetch_medical_report_api():
    """
       API

    """
    time.sleep(2)  #  delay
    report = {
    }

    if report == {}:
        raise gr.Error("Data not loaded!")
    return json.dumps(report, indent=2)

def summarize_report(report_json): 
    try:
        report = json.loads(report_json)
        summary = f"""
    ### 🧑 Patient Info
    - **ID:** {report['patient_id']}
    - **Age:** {report['age']}
    - **Gender:** {report['gender']}

    ### 🩺 Diagnosis
    - **Condition:** {report['diagnosis']}

    ### ⚠️ Key Symptoms
    - {', '.join(report['symptoms'])}

    ### 💊 Medications
    - {', '.join(report['medications'])}

    ### 🧪 Lab Results
    - **BP:** {report['lab_results']['BP']}
    - **Cholesterol:** {report['lab_results']['Cholesterol']}
    """
    except json.decoder.JSONDecodeError as e:
        raise gr.Error("Cannot Summarize Empty Data.")
    return summary


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        #           🏥 Health Sync - Medical Report Summarizer
          
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
        report = fetch_medical_report_api()
        yield report, "✅ Report fetched successfully!"


    fetch_btn.click(
        fn=fetch_with_loader,
        inputs=None,
        outputs=[report_box, status]
    )


    def summarize_with_loader(report_json):
        yield "", "⏳ Summarizing report with AI..."
        summary = summarize_report(report_json)
        yield summary, "✅ Summary ready!"


    summarize_btn.click(
        fn=summarize_with_loader,
        inputs=report_box,
        outputs=[output_box, status]
    )


demo.launch()
