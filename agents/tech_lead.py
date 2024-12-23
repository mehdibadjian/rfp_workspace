# agents/tech_lead.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TechLead:
    def __init__(self, model_name="gemini-pro", rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        self.model = genai.GenerativeModel(model_name)
        self.rfp_summary = rfp_summary
        self.rfp_analysis = rfp_analysis
        self.rfp_assumptions = rfp_assumptions
        logging.info(f"TechLead initialized with model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def create_technical_approach(self, rfp_content, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("Tech Lead: Starting to create a comprehensive technical approach with diagrams.")
        prompt = f"""
        You are the Technical Lead responsible for creating a detailed and comprehensive technical approach for the project described in the following Request for Proposal (RFP).

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}

        Outline a complete technical solution, including:
        - A detailed system architecture diagram illustrating the proposed system components and their interactions. Use Mermaid syntax to generate this diagram.
        - A comprehensive technology stack, listing all technologies, platforms, and tools to be used, with justifications for their selection. Present this as a table.
        - A detailed integration strategy with existing systems, detailing APIs, integration points, and data flow. Use Mermaid syntax for sequence diagrams if applicable.
        - Key functional components of the solution, with detailed descriptions of their functionality.

        Provide a thorough and well-justified technical approach that demonstrates a deep understanding of the technical requirements and a robust solution architecture. Ensure all diagrams are generated using Mermaid syntax.
        """
        logging.debug(f"Tech Lead: Technical approach prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("Tech Lead: Comprehensive technical approach creation complete.")
        return response.text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def provide_detailed_architecture(self, rfp_content, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("Tech Lead: Providing more details on the system architecture.")
        prompt = f"""
        You are the Technical Lead. Provide a more detailed explanation of the system architecture for the following RFP, including a Mermaid diagram.

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}
        """
        response = self.model.generate_content(prompt)
        return response.text