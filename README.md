# Generate Cover Letter with Chat GPT

This project is designed to create a cover letter for your job application. Once you input your personal information as a default, and the company's information as the prompt asks, it creates a txt file for the content. You get to check and modify, and then it creates a PDF file using LaTeX.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

- To install the necessary libraries, run the following command:
```
pip install openai
pip install fire
```
- To install a LaTeX distribution, visit [MacTeX](https://www.tug.org/mactex/).
- To install LaTeX packages, run the following command:
```
sudo tlmgr install lipsum hyperref adjustbox fancyhdr ifmtarg xcolor geometry
```

- To create an OpenAI API key, follow the [OpenAI README](https://cran.r-project.org/web/packages/openai/readme/README.html#:~:text=First%2C%20sign%20up%20for%20OpenAI,on%20the%20green%20text%20Copy.).
- To set your OpenAI API key as an environment variable, run the following command:
```
export OPENAI_API_KEY=<your-api-key>
```

## Usage

### Preparation

To prepare, input your default information.

- Rewrite lines 11-18 of `project/job_application_cover_letter_template/main.tex`.
- Upload your resume as `project/resume.txt`.
  - Note that the longer the resume is, the more expensive the OpenAI fee will be.
- Add your signature image as `project/job_application_cover_letter_template/Img/My_Signature.jpg`.

### Execution

1. Run this on your terminal: `python main.py`.
2. It will ask about the company you want to apply to. Input information.
  - Company name, position, and address must be in a single line.
  - Description of the position can be multiple lines. Press Ctrl+D when done.
3. Once the txt file is opened in your default editor, check and revise manually.
4. Press Enter on your terminal when ready.
5. The final PDF file will open. Done!


## License
 https://creativecommons.org/licenses/by/4.0/
