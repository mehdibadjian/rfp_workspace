# agents/bd_manager.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BDManager:
    def __init__(self, model_name="gemini-pro", rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        self.model = genai.GenerativeModel(model_name)
        self.rfp_summary = rfp_summary
        self.rfp_analysis = rfp_analysis
        self.rfp_assumptions = rfp_assumptions
        logging.info(f"BDManager initialized with model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def breakdown_costs(self, rfp_content, delivery_plan, technical_approach, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("BDManager: Starting a detailed cost breakdown with cost table.")
        prompt = f"""
        You are the Business Development Manager responsible for creating a detailed cost breakdown for the following Request for Proposal (RFP).
        You have access to the RFP summary, key analysis points, and identified assumptions, as well as the proposed delivery plan and technical approach.

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}

        Proposed Delivery Plan:
        {delivery_plan}

        Technical Approach:
        {technical_approach}

        Based on all this information, provide a comprehensive breakdown of all potential costs associated with delivering the solution. Present this information in a clear cost table. The table should include columns for:
        - Cost Item
        - Description
        - Quantity
        - Unit Cost
        - Total Cost

        Include the following cost categories:
        - Personnel costs: Detail the roles, number of resources, hourly/daily rates, and total cost per role, broken down by project phase.
        - Software licenses: List all necessary software licenses, their costs, and licensing terms.
        - Infrastructure costs: Detail cloud infrastructure costs (compute, storage, networking), including estimated usage and pricing models.
        - Third-party services: Include costs for any external services required.
        - Travel and expenses: Estimate any travel or other related expenses.
        - Contingency costs: Include a line item for unforeseen expenses (typically a percentage of the total cost).

        Provide a transparent and detailed cost breakdown table and suggest a competitive pricing strategy.
        """
        logging.debug(f"BDManager: Cost breakdown prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("BDManager: Detailed cost breakdown complete, considering delivery plan and context.")
        return response.text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def provide_detailed_cost_breakdown(self, rfp_content, delivery_plan, technical_approach, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("BD Manager: Providing more details on the cost breakdown.")
        prompt = f"""
        You are the Business Development Manager. Provide a more detailed explanation of the cost breakdown for the following RFP, ensuring a clear cost table is included.

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}

        Proposed Delivery Plan:
        {delivery_plan}

        Technical Approach:
        {technical_approach}
        """
        response = self.model.generate_content(prompt)
        return response.text