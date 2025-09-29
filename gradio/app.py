import gradio as gr
import time
import json
import random
from io import BytesIO
from prompt_engineering.prompt_template import Patient_Summary_System
PSS = Patient_Summary_System()

css = """
/* Modern Medical Theme */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%) !important;
    min-height: 100vh;
}

/* Header Styling */
.gradio-container h1 {
    background: linear-gradient(135deg, #1e40af, #3b82f6, #06b6d4) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center !important;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: -0.025em !important;
}

.gradio-container h3 {
    color: #1e40af !important;
    font-weight: 600 !important;
    font-size: 1.25rem !important;
    margin-bottom: 1rem !important;
    border-bottom: 2px solid #e0f2fe !important;
    padding-bottom: 0.5rem !important;
}

/* Card Styling */
.gradio-container .block {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(59, 130, 246, 0.1) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    backdrop-filter: blur(8px) !important;
    margin: 12px !important;
    padding: 24px !important;
    transition: all 0.3s ease !important;
}

.gradio-container .block:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
    transform: translateY(-2px) !important;
}

/* Button Styling */
.gradio-container .btn {
    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
    border: none !important;
    cursor: pointer !important;
    text-transform: none !important;
    letter-spacing: 0.025em !important;
}

.gradio-container .btn-primary {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    color: white !important;
    box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.4) !important;
}

.gradio-container .btn-primary:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    box-shadow: 0 6px 20px 0 rgba(59, 130, 246, 0.6) !important;
    transform: translateY(-2px) !important;
}

.gradio-container .btn-success {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: white !important;
    box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.4) !important;
}

.gradio-container .btn-success:hover {
    background: linear-gradient(135deg, #059669, #047857) !important;
    box-shadow: 0 6px 20px 0 rgba(16, 185, 129, 0.6) !important;
    transform: translateY(-2px) !important;
}

.gradio-container .btn-secondary {
    background: linear-gradient(135deg, #6b7280, #4b5563) !important;
    color: white !important;
    box-shadow: 0 4px 14px 0 rgba(107, 114, 128, 0.4) !important;
}

/* Input Styling */
.gradio-container input, .gradio-container textarea {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 2px solid #e5e7eb !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    color: #374151 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}

.gradio-container input:focus, .gradio-container textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    outline: none !important;
}

/* Label Styling */
.gradio-container label {
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    margin-bottom: 6px !important;
}

/* Code Block Styling */
.gradio-container .code {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 13px !important;
    color: #334155 !important;
}

/* Radio Button Styling */
.gradio-container .radio {
    background: transparent !important;
}

.gradio-container .radio label {
    background: rgba(255, 255, 255, 0.8) !important;
    border: 2px solid #e5e7eb !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    margin: 4px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.gradio-container .radio label:hover {
    border-color: #3b82f6 !important;
    background: rgba(59, 130, 246, 0.05) !important;
}

/* Status Label Styling */
.gradio-container .label {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe) !important;
    border: 2px solid #bae6fd !important;
    border-radius: 12px !important;
    padding: 16px !important;
    color: #0c4a6e !important;
    font-weight: 500 !important;
    text-align: center !important;
}

/* Patient ID Display */
.patient-id-display input {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: white !important;
    font-weight: 600 !important;
    text-align: center !important;
    font-size: 16px !important;
    border: 2px solid #10b981 !important;
    box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.4) !important;
}

.patient-id-display input::placeholder {
    color: rgba(255, 255, 255, 0.7) !important;
}

/* Image Upload Styling */
.gradio-container .image-container {
    border: 2px dashed #d1d5db !important;
    border-radius: 12px !important;
    background: #f9fafb !important;
    transition: all 0.2s ease !important;
}

.gradio-container .image-container:hover {
    border-color: #3b82f6 !important;
    background: #eff6ff !important;
}

/* Enhanced Mobile Responsiveness */
@media (max-width: 1200px) {
    .gradio-container .block {
        margin: 8px !important;
        padding: 20px !important;
    }
}

@media (max-width: 768px) {
    .gradio-container {
        padding: 8px !important;
    }
    
    .gradio-container .block {
        margin: 4px !important;
        padding: 16px !important;
        border-radius: 12px !important;
    }
    
    .gradio-container h1 {
        font-size: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    .gradio-container h2 {
        font-size: 1.5rem !important;
    }
    
    .gradio-container h3 {
        font-size: 1.2rem !important;
    }
    
    .gradio-container .btn {
        padding: 12px 16px !important;
        font-size: 14px !important;
        width: 100% !important;
        margin: 4px 0 !important;
    }
    
    .gradio-container .code {
        font-size: 12px !important;
        max-height: 200px !important;
        overflow-y: auto !important;
    }
    
    .gradio-container input, .gradio-container textarea {
        font-size: 16px !important; /* Prevents zoom on iOS */
    }
}

@media (max-width: 480px) {
    .gradio-container h1 {
        font-size: 1.8rem !important;
    }
    
    .gradio-container .block {
        padding: 12px !important;
    }
    
    .gradio-container .btn {
        padding: 10px 12px !important;
        font-size: 13px !important;
    }
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.gradio-container .block {
    animation: fadeIn 0.5s ease-out !important;
}

/* Success/Error States */
.status-success {
    color: #059669 !important;
    background: #d1fae5 !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

.status-error {
    color: #dc2626 !important;
    background: #fee2e2 !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

/* Text Colors */
.gradio-container p, .gradio-container span, .gradio-container .markdown {
    color: #374151 !important;
}

/* Improved Layout and Spacing */
.gradio-container .group {
    margin-bottom: 1.5rem !important;
}

.gradio-container .row {
    gap: 1rem !important;
}

/* Better Button Layout on Mobile */
@media (max-width: 768px) {
    .gradio-container .row .btn {
        flex: 1 !important;
        min-width: 0 !important;
    }
}

/* Improved Status Display */
.gradio-container .label {
    font-size: 14px !important;
    line-height: 1.4 !important;
}

/* Better Code Block on Mobile */
@media (max-width: 768px) {
    .gradio-container .code {
        border-radius: 8px !important;
        line-height: 1.3 !important;
    }
}

/* Smooth Transitions */
.gradio-container * {
    transition: all 0.2s ease !important;
}
"""


if __name__ == "__main__":


    with gr.Blocks(theme=gr.themes.Base(), css=css, title="MedRecord AI") as demo:
        # Header
        gr.HTML("""
        <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 16px; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #1e40af, #3b82f6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🏥 MedRecord AI
            </h1>
            <p style="font-size: 1.2rem; color: #64748b; margin: 0.5rem 0 0 0; font-weight: 400;">
                Advanced Medical Record Processing & AI Analysis Platform
            </p>
        </div>
        """)

        with gr.Row(equal_height=False):
            # Left Panel - Data Input
            with gr.Column(scale=1, min_width=300):
                with gr.Group():
                    gr.HTML("<h2 style='color: #1e40af; font-weight: 600; margin-bottom: 1rem; border-bottom: 2px solid #e0f2fe; padding-bottom: 0.5rem;'>📊 Data Input</h2>")
                    
                    source = gr.Radio(
                        choices=["Database", "Upload Photo", "Type Text"],
                        value="Database",
                        label="Select Data Source",
                        info="Choose your preferred method to input patient data"
                    )
                    
                    # Dynamic input sections
                    with gr.Group() as input_section:
                        patient_id = gr.Textbox(
                            value="1",
                            label="Patient ID",
                            placeholder="Enter patient ID (e.g., 1, 2, 3...)",
                            info="Fetch existing patient data from database"
                        )
                        
                        image_input = gr.Image(
                            type="pil",
                            label="Upload Medical Report Image",
                            visible=False,
                            height=250
                        )
                        
                        text_input = gr.Textbox(
                            label="Medical Report Text",
                            lines=6,
                            visible=False,
                            placeholder="Paste or type the complete medical report text here...",
                            info="Enter the full medical report content"
                        )
                    
                    fetch_btn = gr.Button(
                        "🔄 Process Data",
                        variant="primary",
                        size="lg",
                        scale=1
                    )
                
                # Data Display
                with gr.Group():
                    gr.HTML("<h3 style='color: #1e40af; font-weight: 600; margin: 1rem 0 0.5rem 0;'>📋 Processed Data</h3>")
                    report_box = gr.Code(
                        label="Patient Data (JSON Format)",
                        language="json",
                        interactive=False,
                        lines=12
                    )

            # Right Panel - AI Analysis
            with gr.Column(scale=1, min_width=300):
                with gr.Group():
                    gr.HTML("<h2 style='color: #1e40af; font-weight: 600; margin-bottom: 1rem; border-bottom: 2px solid #e0f2fe; padding-bottom: 0.5rem;'>🤖 AI Analysis</h2>")
                    
                    with gr.Row():
                        summarize_btn = gr.Button(
                            "✨ Generate Summary",
                            variant="primary",
                            size="lg"
                        )
                        save_btn = gr.Button(
                            "💾 Save to Database",
                            variant="success",
                            size="lg"
                        )
                    
                    # AI Summary Output
                    gr.HTML("<h3 style='color: #1e40af; font-weight: 600; margin: 1rem 0 0.5rem 0;'>📄 Medical Summary</h3>")
                    output_box = gr.Markdown(
                        value="*AI-generated medical summary will appear here after processing...*",
                        elem_classes=["summary-output"]
                    )
                
                # Patient Management
                with gr.Group():
                    gr.HTML("<h3 style='color: #1e40af; font-weight: 600; margin: 1rem 0 0.5rem 0;'>📈 Patient Management</h3>")
                    
                    saved_patient_id = gr.Textbox(
                        label="Saved Patient ID",
                        interactive=False,
                        placeholder="New patient ID will appear here after saving",
                        elem_classes=["patient-id-display"]
                    )

        # Status Bar
        with gr.Group():
            status = gr.Label(
                value="🟢 System Ready - Select data source to begin",
                label="System Status",
                show_label=False
            )


        def on_source_change(choice):
            # Toggle visibility of controls
            if choice == "Database":
                return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
            elif choice == "Upload Photo":
                return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
            else:  # Type Text
                return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

        source.change(
            fn=on_source_change,
            inputs=source,
            outputs=[patient_id, image_input, text_input]
        )

        def fetch_with_loader(choice, pid, img, text):
            # choice: "Database" | "Upload Photo" | "Type Text"
            if choice == "Database":
                yield "", "🔄 Fetching patient data from database..."
                url = f"http://localhost:8000/patient-app/api/patients/{pid}/"
                report_dict = PSS.get_patient_data(url=url)
                report_json = json.dumps(report_dict, indent=2)
                yield report_json, "🟢 Patient data retrieved successfully"
            elif choice == "Upload Photo":
                yield "", "🔄 Processing medical report image with AI..."
                if img is None:
                    yield "{}", "🔴 Please upload a medical report image"
                else:
                    try:
                        # Convert PIL to PNG bytes
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        image_bytes = buf.getvalue()
                        report_dict = PSS.image_to_patient_json(image_bytes)
                        report_json = json.dumps(report_dict, indent=2)
                        
                        # Check if there was an error in processing
                        if "error" in report_dict:
                            status_msg = f"🔴 Processing failed: {report_dict['error']}"
                        elif report_dict:
                            status_msg = "🟢 Medical data extracted successfully from image"
                        else:
                            status_msg = "🟡 Image processed but no structured data found"
                            
                        yield report_json, status_msg
                    except Exception as e:
                        error_json = json.dumps({"error": f"Image processing failed: {str(e)}"}, indent=2)
                        yield error_json, f"🔴 Image processing error: {str(e)}"
            else:  # Type Text
                yield "", "🔄 Converting text to structured medical data..."
                if not text.strip():
                    yield "{}", "🔴 Please enter medical report text"
                else:
                    try:
                        report_dict = PSS.text_to_patient_json(text)
                        report_json = json.dumps(report_dict, indent=2)
                        
                        if "error" in report_dict:
                            status_msg = f"🔴 Processing failed: {report_dict['error']}"
                        elif report_dict:
                            status_msg = "🟢 Text converted to structured medical data"
                        else:
                            status_msg = "🟡 Text processed but structure incomplete"
                            
                        yield report_json, status_msg
                    except Exception as e:
                        error_json = json.dumps({"error": f"Text processing failed: {str(e)}"}, indent=2)
                        yield error_json, f"🔴 Text processing error: {str(e)}"


        fetch_btn.click(
            fn=fetch_with_loader,
            inputs=[source, patient_id, image_input, text_input],
            outputs=[report_box, status]
        )


        def summarize_with_loader(choice, pid, report_json):
            yield "", "🔄 Generating AI medical summary..."
            try:
                record = json.loads(report_json) if report_json else {}
            except Exception:
                record = {}

            if record and "error" not in record:
                summary = PSS.generate_summary_from_data(record)
                yield summary, "🟢 AI medical summary generated successfully"
            else:
                # Fallback: if database is selected, summarize directly from URL
                if choice == "Database":
                    url = f"http://localhost:8000/patient-app/api/patients/{pid}/"
                    summary = PSS.generate_summary(url=url)
                    yield summary, "🟢 Medical summary generated from database"
                else:
                    yield "**No valid medical data available for summary generation.**\n\nPlease process patient data first using one of the available methods.", "🔴 No data available - please process medical data first"


        summarize_btn.click(
            fn=summarize_with_loader,
            inputs=[source, patient_id, report_box],
            outputs=[output_box, status]
        )

        def save_with_loader(report_json):
            yield "🔄 Saving patient record to database...", ""
            try:
                if not report_json.strip():
                    yield "🔴 No data to save - please process patient data first", ""
                    return
                
                record = json.loads(report_json)
                if "error" in record:
                    yield "🔴 Cannot save data containing errors - please fix data first", ""
                    return
                
                # Additional debug: show the record structure before saving
                print("DEBUG: Record structure before saving:")
                print(f"Type: {type(record)}")
                print(f"Keys: {list(record.keys()) if isinstance(record, dict) else 'Not a dict'}")
                if isinstance(record, dict) and "medical_history" in record:
                    print(f"Medical history type: {type(record['medical_history'])}")
                    print(f"Medical history content: {record['medical_history']}")
                
                result = PSS.save_to_database(record)
                
                if result["success"]:
                    patient_id = result.get("patient_id", "Unknown")
                    yield f"🟢 Patient record saved successfully to database", f"Patient ID: {patient_id}"
                else:
                    error_msg = result.get("error", "Unknown error")
                    details = result.get("details", "")
                    if "Django backend server is not running" in error_msg:
                        yield "🔴 Database server not running - please start Django backend", ""
                    else:
                        full_error = f"{error_msg}"
                        if details:
                            full_error += f" | {details}"
                        yield f"🔴 Save failed: {full_error}", ""
                    
            except json.JSONDecodeError as e:
                yield f"🔴 Invalid data format: {str(e)}", ""
            except Exception as e:
                yield f"🔴 System error: {str(e)}", ""

        save_btn.click(
            fn=save_with_loader,
            inputs=[report_box],
            outputs=[status, saved_patient_id]
        )

        # Add some interactive features
        def update_status_on_data_change(data):
            if data and data.strip():
                try:
                    parsed = json.loads(data)
                    if "error" in parsed:
                        return "🟡 Data contains errors - review before processing"
                    else:
                        return "🟢 Medical data ready for analysis and saving"
                except:
                    return "🟡 Invalid data format detected"
            return "🔵 Ready to process medical data"

        report_box.change(
            fn=update_status_on_data_change,
            inputs=[report_box],
            outputs=[status]
        )

    demo.launch(share=False, server_name="127.0.0.1", server_port=None)
