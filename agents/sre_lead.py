# agents/sre_lead.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SRELead:
    def __init__(self, model_name="gemini-pro", rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        self.model = genai.GenerativeModel(model_name)
        self.rfp_summary = rfp_summary
        self.rfp_analysis = rfp_analysis
        self.rfp_assumptions = rfp_assumptions
        logging.info(f"SRELead initialized with model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def create_maintenance_support_plan(self, rfp_content, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("SRE Lead: Starting to create a comprehensive maintenance and support plan.")
        prompt = f"""
        You are the SRE Lead responsible for creating a detailed maintenance and support plan for the solution described in the following Request for Proposal (RFP).

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}

        Outline a comprehensive maintenance and support plan, including:
        - Service Level Agreements (SLAs) for availability, performance, and response times.
        - Monitoring and alerting strategy, including tools and key metrics to be monitored.
        - Incident management process, detailing steps for handling and resolving incidents.
        - Problem management process for identifying and addressing recurring issues.
        - Change management process for managing updates and modifications to the system.
        - Security maintenance and patching strategy.
        - Backup and recovery procedures, including frequency and retention policies.
        - Performance optimization strategies and tools.
        - Support team structure and escalation paths.
        - Communication plan for updates and maintenance activities.

        Provide a thorough and detailed maintenance and support plan that ensures the long-term stability, performance, and security of the proposed solution.
        """
        logging.debug(f"SRE Lead: Maintenance and support plan prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("SRE Lead: Comprehensive maintenance and support plan creation complete.")
        return response.text