# agents/presale_manager.py
import google.generativeai as genai
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PresaleManager:
    def __init__(self, model_name="gemini-pro", rfp_summary=None, rfp_analysis=None, rfp_assumptions=None):
        self.model = genai.GenerativeModel(model_name)
        self.responses = {}
        self.rfp_summary = rfp_summary
        self.rfp_analysis = rfp_analysis
        self.rfp_assumptions = rfp_assumptions
        logging.info(f"PresaleManager initialized with model: {model_name}")

    def evaluate_response(self, agent_name, response):
        """Evaluates the response from an agent and returns feedback if needed."""
        if not response or len(response) < 100:  # Example criteria for insufficient response
            return f"The response from {agent_name} is too short and lacks detail. Please provide more comprehensive information."
        return None

    def request_more_details(self, agent, method_name, rfp_content, **kwargs):
        """Requests more details from a specific agent."""
        logging.info(f"PresaleManager requesting more details from {agent.__class__.__name__} using {method_name}")
        method = getattr(agent, method_name)
        return method(rfp_content, self.rfp_summary, self.rfp_analysis, self.rfp_assumptions, **kwargs)

    def orchestrate_responses(self, rfp_content):
        """
        Orchestrates the responses from all agents and generates the final comprehensive RFP response.
        """
        prompt = f"""
        You are the Presale Manager responsible for crafting the final, highly detailed and comprehensive response to the following Request for Proposal (RFP).
        You have received information from various expert agents. Synthesize this information into a well-structured, persuasive, and thorough proposal that addresses all requirements. Ensure all diagrams and tables are included using Mermaid syntax where applicable.

        RFP Summary:
        {self.rfp_summary}

        RFP Analysis:
        {self.rfp_analysis}

        RFP Assumptions:
        {self.rfp_assumptions}

        RFP Content:
        {rfp_content}

        Responses from Expert Agents:
        {self.responses}

        Based on the RFP content and the detailed expert agent responses, generate the complete RFP response. The technical proposal should include the following items extensively:

        1. Executive Summary
            - Overview of the Proposal
            - Objectives and Goals
            - Key Deliverables

        2. Background and Context
            - Current Challenges or Needs
            - Existing Systems or Processes
            - Stakeholder Insights

        3. Proposal Objectives
            - High-Level Goals
            - Specific and Measurable Outcomes
            - Alignment with Business Strategy

        4. Scope of Work
            - In-Scope Items
            - Out-of-Scope Items
            - Assumptions and Constraints

        5. Technical Approach
            - System Architecture Overview (Include Mermaid Diagram)
            - Technology Stack (Include Table)
            - Integration Strategy (Include Mermaid Sequence Diagram if applicable)
            - Key Functional Components

        6. Implementation Plan
            - Phases and Milestones
            - Resource Allocation
            - Tools and Platforms to be Used
            - Risk Management Plan

        7. Detailed Deliverables
            - Technical Specifications
            - Code Modules/Features
            - Testing and QA Artifacts
            - Documentation

        8. Timeline and Schedule
            - Project Roadmap
            - Detailed Gantt Chart (using Mermaid syntax)
            - Contingency Plans for Delays

        9. Resource Requirements
            - Team Structure and Roles
            - Hardware and Software Needs
            - Budget Allocation

        10. Risk Analysis and Mitigation
            - Potential Risks and Impacts
            - Mitigation Strategies
            - Dependencies and Assumptions

        11. Quality Assurance Plan
            - Testing Strategy and Framework
            - Metrics for Success
            - Post-Implementation Validation

        12. Monitoring and Evaluation
            - KPIs and Metrics to Track Progress
            - Reporting Mechanisms
            - Feedback Loop

        13. Maintenance and Support
            - Support Model
            - SLAs and Response Times
            - Post-Launch Enhancements

        14. Cost Estimate and Budget
            - Detailed Cost Breakdown (Include Cost Table)
            - ROI Analysis
            - Funding Sources

        15. Conclusion and Recommendations
            - Summary of Key Points
            - Why This Proposal Should Be Accepted
            - Next Steps

        16. Appendices
            - Glossary of Terms
            - Reference Documents
            - Supporting Data

        17. References and Citations
            - Technical Sources
            - Standards and Guidelines Followed

        Focus on providing specific details, clear explanations, and strong justifications for all proposed solutions and approaches. Ensure the proposal is persuasive and addresses all aspects of the RFP comprehensively. Include all generated Mermaid diagrams and tables within the relevant sections.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def receive_response(self, agent_name, response):
        """
        Receives and stores the response from an individual agent.
        """
        self.responses[agent_name] = response
        logging.info(f"PresaleManager received response from {agent_name}")