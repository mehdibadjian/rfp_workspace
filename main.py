import os
from dotenv import load_dotenv
import google.generativeai as genai
from agents.presale_manager import PresaleManager
from agents.bd_manager import BDManager
from agents.tech_lead import TechLead
from agents.sre_lead import SRELead
from agents.test_lead import TestLead
from agents.internet_researcher import InternetResearcher
from agents.delivery_lead import DeliveryLead
from agents.rfp_analyser import RFPanalyser
import PyPDF2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
# Configure generative AI
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
logging.info("Google Generative AI configured.")

def read_pdf(file_path):
    logging.info(f"Reading PDF file: {file_path}")
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    logging.info(f"PDF content read successfully. Length: {len(text)} characters.")
    return text

if __name__ == "__main__":
    rfp_path = "data/rfp.pdf"  # Replace with your RFP file path
    logging.info(f"Processing RFP file: {rfp_path}")
    rfp_content = read_pdf(rfp_path)

    rfp_analyser = RFPanalyser("gemini-1.5-flash")
    logging.info("RFPanalyser initialized.")

    logging.info("Calling RFPanalyser to summarize RFP.")
    rfp_summary = rfp_analyser.summarize_rfp(rfp_content)
    logging.info(f"RFPanalyser summary received. Length: {len(rfp_summary)} characters.")

    logging.info("Calling RFPanalyser to analyse RFP and extract key information.")
    rfp_analysis = rfp_analyser.analyse_rfp(rfp_content, rfp_summary)
    logging.info(f"RFPanalyser analysis received. Length: {len(rfp_analysis)} characters.")

    logging.info("Calling RFPanalyser to identify assumptions.")
    rfp_assumptions = rfp_analyser.identify_assumptions(rfp_content)
    logging.info(f"RFPanalyser assumptions received. Length: {len(rfp_assumptions)} characters.")

    presale_manager = PresaleManager("gemini-1.5-flash", rfp_summary, rfp_analysis, rfp_assumptions)
    bd_manager = BDManager("gemini-1.5-flash", rfp_summary, rfp_analysis, rfp_assumptions)
    tech_lead = TechLead("gemini-1.5-flash", rfp_summary, rfp_analysis, rfp_assumptions)
    sre_lead = SRELead("gemini-1.5-flash", rfp_summary, rfp_analysis, rfp_assumptions)
    test_lead = TestLead("gemini-1.5-flash", rfp_summary, rfp_analysis, rfp_assumptions)
    internet_researcher = InternetResearcher("gemini-1.5-flash", rfp_summary, rfp_analysis, rfp_assumptions)
    delivery_lead = DeliveryLead("gemini-1.5-flash", rfp_summary, rfp_analysis, rfp_assumptions)
    logging.info("Agents initialized.")

    logging.info("Calling Delivery Lead to create delivery plan.")
    delivery_plan = delivery_lead.create_delivery_plan(rfp_content, rfp_summary, rfp_analysis, rfp_assumptions)
    presale_manager.receive_response("Delivery Lead", delivery_plan)
    feedback = presale_manager.evaluate_response("Delivery Lead", delivery_plan)
    if feedback:
        delivery_plan = presale_manager.request_more_details(delivery_lead, "provide_detailed_resource_plan", rfp_content)
        presale_manager.receive_response("Delivery Lead", delivery_plan)
    logging.info(f"Delivery Lead response received. Length: {len(delivery_plan)} characters.")

    logging.info("Calling Tech Lead to create technical approach.")
    tech_response = tech_lead.create_technical_approach(rfp_content, rfp_summary, rfp_analysis, rfp_assumptions)
    presale_manager.receive_response("Tech Lead", tech_response)
    feedback = presale_manager.evaluate_response("Tech Lead", tech_response)
    if feedback:
        tech_response = presale_manager.request_more_details(tech_lead, "provide_detailed_architecture", rfp_content)
        presale_manager.receive_response("Tech Lead", tech_response)
    logging.info(f"Tech Lead response received. Length: {len(tech_response)} characters.")

    logging.info("Calling BD Manager to breakdown costs based on delivery plan and technical approach.")
    bd_response = bd_manager.breakdown_costs(rfp_content, delivery_plan, tech_response, rfp_summary, rfp_analysis, rfp_assumptions)
    presale_manager.receive_response("BD Manager", bd_response)
    feedback = presale_manager.evaluate_response("BD Manager", bd_response)
    if feedback:
        bd_response = presale_manager.request_more_details(bd_manager, "provide_detailed_cost_breakdown", rfp_content, delivery_plan=delivery_plan, technical_approach=tech_response)
        presale_manager.receive_response("BD Manager", bd_response)
    logging.info(f"BD Manager response received. Length: {len(bd_response)} characters.")

    logging.info("Calling SRE Lead to create maintenance and support plan.")
    sre_response = sre_lead.create_maintenance_support_plan(rfp_content, rfp_summary, rfp_analysis, rfp_assumptions)
    presale_manager.receive_response("SRE Lead", sre_response)
    logging.info(f"SRE Lead response received. Length: {len(sre_response)} characters.")

    logging.info("Calling Test Lead to create testing approach.")
    test_response = test_lead.create_testing_approach(rfp_content, rfp_summary, rfp_analysis, rfp_assumptions)
    presale_manager.receive_response("Test Lead", test_response)
    logging.info(f"Test Lead response received. Length: {len(test_response)} characters.")

    logging.info("Calling Internet Researcher to research RFP context.")
    research_response = internet_researcher.research_rfp_context(rfp_content, rfp_summary, rfp_analysis, rfp_assumptions)
    presale_manager.receive_response("Internet Researcher", research_response)
    logging.info(f"Internet Researcher response received. Length: {len(research_response)} characters.")

    presale_manager.receive_response("RFP Summary", rfp_summary)
    presale_manager.receive_response("RFP Analysis", rfp_analysis)
    presale_manager.receive_response("RFP Assumptions", rfp_assumptions)

    logging.info("Generating final response using Presale Manager.")
    final_response = presale_manager.orchestrate_responses(rfp_content)
    logging.info(f"Final response generated. Length: {len(final_response)} characters.")

    # Create the 'temp' folder if it doesn't exist
    temp_folder = "temp"
    os.makedirs(temp_folder, exist_ok=True)

    # Define the file path
    file_path = os.path.join(temp_folder, "final_technical_proposal.md")

    # Write the final response to the Markdown file
    with open(file_path, "w") as f:
        f.write(final_response)

    logging.info(f"Final response saved to: {file_path}")

    # Remove the print statement
    # print("Final Response:\n", final_response)
    logging.info("Final response printing to console removed.")