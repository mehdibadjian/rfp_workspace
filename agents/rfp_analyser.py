# agents/rfp_analyser.py
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RFPanalyser:
    def __init__(self, model_name="gemini-pro"):
        self.model = genai.GenerativeModel(model_name)
        logging.info(f"RFPanalyser initialized with model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def summarize_rfp(self, rfp_content):
        logging.info("RFPanalyser: Starting to summarize RFP.")
        prompt = f"""
        You are an expert RFP analyst tasked with summarizing the following Request for Proposal (RFP).
        Your summary should capture the following key details:

        Step 1: Summarize the RFP
        Carefully read the RFP and create a concise summary capturing the following key details:
        Client:
        - Name of the client organization
        - Industry or sector they operate in
        - Approximate size or scale of their operations
        - Current IT infrastructure and any specific challenges they face in Oman
        Project Objectives:
        - Clearly state the client's primary goals and desired outcomes for the cloud migration project (e.g., cost reduction, improved scalability, enhanced security, compliance with Oman regulations).
        Scope of Work:
        - Outline the specific services requested:
            - Cloud migration (which applications or workloads)
            - Managed services (e.g., monitoring, security, optimization)
            - Specific cloud technologies or platforms preferred
        - List any deliverables expected (e.g., migration plan, documentation, training)
        Key Requirements:
        - Identify any critical technical requirements (e.g., performance benchmarks, integration needs)
        - Highlight any regulatory or compliance requirements specific to Oman
        - Note any other client priorities (e.g., data residency, local support)
        Evaluation Criteria:
        - List the criteria the client will use to evaluate proposals (e.g., experience, technical expertise, cost, understanding of the Oman market)
        - Note any specific weighting or priorities assigned to different criteria
        Other Relevant Information:
        - Summarize any additional details that could be crucial to winning the project:
            - Client's pain points or challenges
            - Budget constraints or expectations
            - Timeline or project schedule preferences
            - Any specific preferences for local partners or resources

        RFP Content:
        {rfp_content}
        """
        logging.debug(f"RFPanalyser: Summary prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("RFPanalyser: RFP summarization complete.")
        return response.text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def analyse_rfp(self, rfp_content, rfp_summary):
        logging.info("RFPanalyser: Starting to analyse RFP and extract key information.")
        prompt = f"""
        You are an expert RFP analyst tasked with analyzing the following Request for Proposal (RFP) and its summary.
        Extract the following key information to guide proposal content generation:

        Step 2: Analyze the RFP and Extract Key Information
        Thoroughly analyze the RFP and extract the following key information to guide proposal content generation:
        Client Background and Needs:
        - Refine your understanding of the client's industry, current IT landscape, and challenges based on the RFP summary.
        - Identify any specific Oman-specific regulations or considerations mentioned in the RFP.
        Project Scope and Deliverables:
        - Refine your understanding of the specific services requested, expected deliverables, and timelines based on the RFP summary.
        - Pay close attention to any specific technical, regulatory, or Oman-specific requirements mentioned.
        Evaluation Criteria:
        - Ensure you have a clear understanding of the criteria the client will use to evaluate proposals and any assigned weighting or priorities.

        RFP Content:
        {rfp_content}

        RFP Summary:
        {rfp_summary}
        """
        logging.debug(f"RFPanalyser: Analysis prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("RFPanalyser: RFP analysis and key information extraction complete.")
        return response.text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def identify_assumptions(self, rfp_content):
        logging.info("RFPanalyser: Starting to identify assumptions.")
        prompt = f"""
        You are an expert RFP analyst tasked with identifying assumptions based on the following Request for Proposal (RFP).

        Step 3: Identify Assumptions
        Based on your RFP analysis, list any assumptions you are making in your proposal due to points not being fully detailed in the RFP. These could include:
        Current IT Environment: Assumptions about the client's existing infrastructure, applications, data volumes, etc., that will impact the migration strategy.
        Technical Requirements: Any assumptions about specific technical needs or performance expectations that are not explicitly stated.
        Regulatory Compliance: Assumptions about specific Oman regulations or compliance standards that may apply to the project but are not fully outlined in the RFP.
        Timeline & Budget: Any assumptions about project timelines or budget constraints that might influence the proposed solution.
        Other: Any other relevant assumptions made due to ambiguities or gaps in the RFP.

        RFP Content:
        {rfp_content}
        """
        logging.debug(f"RFPanalyser: Assumptions prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.info("RFPanalyser: Assumption identification complete.")
        return response.text