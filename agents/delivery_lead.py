# agents/delivery_lead.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DeliveryLead:
    def __init__(self, model_name="gemini-pro", rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        self.model = genai.GenerativeModel(model_name)
        self.rfp_summary = rfp_summary
        self.rfp_analysis = rfp_analysis
        self.rfp_assumptions = rfp_assumptions
        logging.info(f"DeliveryLead initialized with model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def create_delivery_plan(self, rfp_content, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("DeliveryLead: Starting to create a detailed delivery plan with Gantt chart and resource allocation.")
        prompt = f"""
        You are the Delivery Lead responsible for creating a comprehensive delivery plan for the project described in the following Request for Proposal (RFP).

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}

        Outline a detailed delivery approach, including:
        - Key phases of the project with clear objectives and deliverables for each phase.
        - A detailed timeline for each phase, including start and end dates, and dependencies between phases. Generate a Gantt chart using Mermaid syntax.
        - A comprehensive list of resources required for each phase, including personnel (roles and estimated hours), tools, software, and infrastructure. Present this as a table.
        - Risk assessment and mitigation strategies for potential delivery challenges.
        - Communication plan outlining frequency, stakeholders, and channels.
        - Quality assurance processes to ensure successful delivery.
        - Project governance structure, including roles and responsibilities.

        Provide a well-structured and detailed delivery plan that demonstrates a clear understanding of the project requirements and a robust approach to execution. Ensure the Gantt chart is generated using Mermaid syntax.
        """
        logging.debug(f"DeliveryLead: Delivery plan prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("DeliveryLead: Detailed delivery plan creation complete.")
        return response.text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def provide_detailed_resource_plan(self, rfp_content, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("Delivery Lead: Providing more details on the resource plan.")
        prompt = f"""
        You are the Delivery Lead. Provide a more detailed explanation of the resource plan for the following RFP, including a table of resources per phase.

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