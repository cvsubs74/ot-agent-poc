import os
import io
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import vision

class EvidenceValidator:
    """
    A class that handles evidence validation by allowing the user to upload a document and
    provide an evidence task description. It then uses Google Vertex AI Generative Model
    (e.g., Google Gemini) to validate whether the uploaded evidence meets the required criteria.
    """
    def __init__(self):
        # Initialize Vertex AI with the provided project credentials and model
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]
        vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
        self.model = GenerativeModel(os.environ["MODEL"])
        # Initialize Vision API client
        self.vision_client = vision.ImageAnnotatorClient()

    def validate_evidence(self):
        # Allow the user to upload various document types or images
        uploaded_file = st.file_uploader(
            "Upload Evidence Document (PDF, DOC, TXT, Excel, Images, etc.)", 
            type=["pdf", "doc", "docx", "xlsx", "csv", "png", "jpg", "jpeg", "txt"]
        )
        
        # Input text area for the evidence task description
        evidence_description = st.text_area("Enter the description of the evidence task:")
        
        if st.button("Validate Evidence"):
            if not uploaded_file:
                st.error("Please upload a file for validation.")
                return
            if not evidence_description:
                st.error("Please provide a description of the evidence task.")
                return

            # Extract content from the uploaded file
            file_content = ""
            file_type = uploaded_file.type
            
            if file_type in ["image/png", "image/jpeg"]:
                # Read the image file
                image_content = uploaded_file.read()
                image = vision.Image(content=image_content)
                
                # Perform text detection
                text_detection = self.vision_client.text_detection(image=image)
                texts = text_detection.text_annotations
                
                # Perform object detection
                objects = self.vision_client.object_localization(image=image).localized_object_annotations
                
                # Perform web detection
                web_detection = self.vision_client.web_detection(image=image).web_detection
                
                # Combine all analysis results
                file_content = "Image Analysis Results:\n\n"
                
                if texts:
                    file_content += "1. Extracted Text Content:\n"
                    file_content += texts[0].description + "\n\n"
                
                if objects:
                    file_content += "2. Detected UI Elements:\n"
                    file_content += ", ".join([obj.name for obj in objects]) + "\n\n"
                
                if web_detection.best_guess_labels:
                    file_content += "3. Image Classification:\n"
                    file_content += ", ".join([label.label for label in web_detection.best_guess_labels])
            else:
                try:
                    # Attempt to decode the file content as text
                    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
                    if not file_content.strip():
                        file_content = f"File type {file_type} appears to contain non-textual data."
                except Exception as e:
                    file_content = f"Could not extract text content from the file. Error: {str(e)}"

            # Construct the prompt for the generative model
            prompt = f"""
                Validate the following evidence based on the provided evidence task description.

                Evidence Task Description:
                {evidence_description}

                Extracted Evidence Content:
                {file_content}

                Please assess whether the uploaded evidence meets the requirements described in the evidence task.
                Provide a detailed validation with your assessment and, if necessary, recommendations for further evidence.
            """

            with st.spinner("Validating evidence using Google Gemini..."):
                try:
                    response = self.model.generate_content(prompt)
                    if response and hasattr(response, "text"):
                        st.markdown("### Validation Result")
                        st.write(response.text)
                    else:
                        st.warning("No validation result received from the AI model.")
                except Exception as e:
                    st.error(f"An error occurred during evidence validation: {str(e)}")
