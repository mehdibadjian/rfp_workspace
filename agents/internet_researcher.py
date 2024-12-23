# agents/internet_researcher.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InternetResearcher:
    def __init__(self, model_name="gemini-pro", rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        self.model = genai.GenerativeModel(model_name)
        self.rfp_summary = rfp_summary
        self.rfp_analysis = rfp_analysis
        self.rfp_assumptions = rfp_assumptions
        logging.info(f"InternetResearcher initialized with model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def research_rfp_context(self, rfp_content, rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        logging.info("Internet Researcher: Starting detailed research on RFP context.")
        prompt = f"""
        You are an expert Internet Researcher tasked with gathering detailed contextual information for the following Request for Proposal (RFP).

        RFP Summary:
        {rfp_summary}

        RFP Analysis:
        {rfp_analysis}

        RFP Assumptions:
        {rfp_assumptions}

        RFP Content:
        {rfp_content}

        Conduct thorough research to provide comprehensive context, including:
        - Detailed information about the client organization: their history, market position, key products/services, recent news, and financial performance.
        - In-depth analysis of the client's industry or sector in Oman: current trends, challenges, and opportunities.
        - Detailed understanding of the client's competitors and their solutions.
        - Insights into any specific technologies or platforms mentioned in the RFP and their relevance to the client's needs.
        - Information about regulatory and compliance requirements in Oman relevant to the project.
        - Any publicly available information about the client's past projects or initiatives.
        - Information about potential local partners or resources in Oman.

        Provide a detailed research report that offers valuable context for crafting a winning proposal.
        """
        logging.debug(f"Internet Researcher: Research prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("Internet Researcher: Detailed context research complete.")
        return response.text