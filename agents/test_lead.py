# agents/test_lead.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestLead:
    def __init__(self, model_name="gemini-pro", rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        self.model = genai.GenerativeModel(model_name)
        self.rfp_summary = rfp_summary
        self.rfp_analysis = rfp_analysis
        self.rfp_assumptions = rfp_assumptions
        logging.info(f"TestLead initialized with model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def create_testing_approach(self, rfp_content, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("Test Lead: Starting to create a comprehensive testing approach.")
        prompt = f"""
        You are the Test Lead responsible for creating a detailed testing approach for the project described in the following Request for Proposal (RFP).

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}

        Outline a comprehensive testing approach, including:
        - Different levels of testing to be performed (e.g., unit, integration, system, acceptance).
        - Specific testing methodologies and techniques to be used for each level.
        - Test environment setup and requirements.
        - Test data strategy and management.
        - Test case design and coverage strategy.
        - Defect tracking and management process.
        - Performance testing approach and tools.
        - Security testing approach and tools.
        - Automation strategy for testing.
        - Roles and responsibilities within the testing team.
        - Entry and exit criteria for each testing phase.

        Provide a thorough and detailed testing approach that ensures the quality and reliability of the proposed solution.
        """
        logging.debug(f"Test Lead: Testing approach prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("Test Lead: Comprehensive testing approach creation complete.")
        return response.text