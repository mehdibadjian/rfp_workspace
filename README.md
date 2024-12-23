# README.md

## RFP Cracking Workspace

This workspace contains Python code to instantiate multiple AI agents to process and respond to RFP (Request for Proposal) PDF documents.

### Agents

- **Presale Manager:** Orchestrates the responses from all other agents.
- **BD Manager:** Breaks down the costs associated with the RFP.
- **Tech Lead/Senior Solution Architect:** Develops the detailed technical approach.
- **SRE Lead:** Defines the best maintenance and support approach.
- **Test Lead:** Outlines the optimal testing strategy for the project.
- **Internet Researcher:** Searches the internet for additional information relevant to the RFP.


### Technologies

- Python
- Google Gemini API
- PyPDF2


### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repo.git  *(Replace with your repo URL)*
   cd your-repo
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv  *(Recommended: Using .venv keeps it local)*
   ```

3. **Activate the virtual environment:**

   - On Windows: `.venv\Scripts\activate`
   - On macOS and Linux: `source .venv/bin/activate`

4. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set your Google Gemini API key:**

   - **Environment variable:**  The recommended approach.
     ```bash
     export GOOGLE_API_KEY="YOUR_API_KEY"  *(Linux/macOS)*
     set GOOGLE_API_KEY="YOUR_API_KEY"      *(Windows)*
     ```
   - **.env file:** Create a `.env` file in the project root and add the following line:
      ```
      GOOGLE_API_KEY=YOUR_API_KEY
      ```
      Then install `python-dotenv`: `pip install python-dotenv` and load it in your `main.py` (see example below).


6. **Place the RFP PDF file:** Place the RFP PDF file in the root directory and name it `rfp_example.pdf` (or modify the `rfp_path` variable in `main.py`).


### Running the Application

```bash
python main.py
```


### Example `main.py` with .env file handling:

```python
import os
from dotenv import load_dotenv
from pypdf import PdfReader  # Example import

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("GOOGLE_API_KEY")

if api_key is None:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

# ... rest of your code ...

rfp_path = "rfp_example.pdf"  # Or get this from command-line arguments

reader = PdfReader(open(rfp_path, "rb"))

# ... process the PDF ...
```


### Project Structure (Suggestion)

```
rfp-cracking-workspace/
├── main.py          # Main application script
├── agents/          # Module for agent classes
│   ├── presale_manager.py
│   ├── bd_manager.py
│   ├── tech_lead.py
│   ├── ...
├── utils/           # Utility functions (e.g., PDF parsing, API interaction)
│   ├── pdf_utils.py
│   ├── api_utils.py
│   ├── ...
├── .env             # Environment variables (optional)
├── requirements.txt  # Project dependencies
├── README.md        # This file
└── rfp_example.pdf # Example RFP document
```

### Contributing

Contributions are welcome! Please submit a pull request with a clear description of your changes.

### License

[MIT License](LICENSE)  *(Create a LICENSE file with the MIT license text)*

### Contact

Your Name - [your.email@example.com](mailto:your.email@example.com)


This improved README provides:

* More detailed setup instructions, including .env file usage and virtual environment best practices.
* A suggested project structure for better organization.
* A code example demonstrating how to use the API key from the environment or a .env file.
* Placeholders for your repository URL and contact information.
* Sections for contributions and license.  Remember to create the LICENSE file.


This will make your project much more accessible and easier for others to contribute to. Remember to fill in the placeholders with your specific details.
```
