import datetime
import json
import os
import shutil
import tempfile

import fire
import openai

RESUME_FILENAME = "resume.txt"

TEMPLATE_DIR = "job_application_cover_letter_template"

SAMPLE_OUTPUT = """
Dear Hiring Manager,

I am writing to apply for the Meta Data Scientist position in your company. I obtained my Master's Degree in CS from Stanford University in August 2021, and I am eager to apply my analytical and data-driven skills to a career in data science.

During my graduate program, I received rigorous training in statistical analysis, programming, and data visualization. I used Python and R to conduct data analysis on experimental observations and simulations, and I collaborated with interdisciplinary teams to derive insights about our environment. Through these experiences, I gained a solid foundation in machine learning techniques, including regression, classification, clustering, and deep learning.

I am confident that my skills acquired in my master's degree, my passion for data science, and my eagerness to learn will make me a valuable asset to your team. I am excited about the opportunity to contribute to an innovative company such as yours, which values creativity, initiative, and technical excellence.

Thank you for considering my application. I look forward to the opportunity to discuss my qualifications with you further.
"""


def inputs(info):
    # includes several rows of inputs unitl Ctrl+D
    print(f"{info}: ")
    contents = ""
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents = contents + " " + line
    return contents


def content_cover_letter(resume, description, debug=False):
    if debug:
        return SAMPLE_OUTPUT
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Here is my resume: {}".format(resume)},
                {
                    "role": "user",
                    "content": "I am applying for this position at this company: {}".format(description),
                },
                {
                    "role": "user",
                    "content": "Make a cover letter that emphasizes my experience and explains why I am a good fit for this role.",
                },
            ],
        )
        return (
            response["choices"][0]["message"]["content"]
            .replace("Sincerely,", "")
            .replace("[Your Name]", "")
            .replace("[Your name]", "")
            .strip()
        )


def format_address(address, debug=False):
    if debug:
        return {'street_address': '1600 Amphitheatre Parkway', 'city': 'Mountain View', 'state': 'CA', 'country': 'USA', 'postal_code': '94043'}
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Convert the following address into a JSON format with street_address, city, state, country, and postal_code fields: {address}",
                },
                {"role": "assistant", "content": "Sure! Here's the formatted address:"},
            ],
        )
        return json.loads(response["choices"][0]["message"]["content"])


def write_application_letter(dir_name, content_filename):
    # import txt file and load as content
    with open(f"{content_filename}", "r") as r:
        content = r.read()
        
    with open(f"{dir_name}/Txt/Application-letter.tex", "w") as w:
        w.write("\\section{Job Application Cover Letter}\n")
        w.write(content)


def update_main_tex(dir_name, date, company, position, address):
    main_file = f"{dir_name}/main.tex"
    with open(main_file, "r") as r:
        main_text = r.read()

    address_inject = f"\\ProvideAdress{{{address['street_address']}, {address['city']}}}{{{address['state']}, {address['country']} {address['postal_code']}}}{{II}}"
    main_text = (
        main_text.replace("__ADDRESS__", address_inject)
        .replace("__DATE__", date)
        .replace("__POSITION__", position)
        .replace("__COMPANY__", company)
    )

    with open(main_file, "w") as w:
        w.write(main_text)


def main(debug: bool = False):
    # collect info
    with open(RESUME_FILENAME, "r") as r:
        resume = r.read()
    company_name = input("company: ")  # single line input
    position = input("position: ")  # single line input
    address = format_address(input("address: "), debug)  # single line input with formatting
    print(address)
    description = inputs("description")  # multiple lines until Ctrl+D
    
    date = datetime.date.today().strftime("%m.%d.%Y")

    # prompt chatgpt
    cover_letter_content = content_cover_letter(resume, description, debug)

    # create new directory from template
    tmp_dir = tempfile.mkdtemp()
    shutil.copytree(TEMPLATE_DIR, tmp_dir, dirs_exist_ok=True)

    # update main.tex with above info
    update_main_tex(tmp_dir, date, company_name, position, address)
    
    # export content into data folder as txt file
    data_folder = f"data/{datetime.date.today().strftime('%y%m%d')}"
    os.makedirs(data_folder, exist_ok=True)
    
    # write the data to a txt file
    preprocessed_company_name = company_name.strip().lower().replace(" ", "_")
    preprocessed_position_name = position.strip().lower().replace(" ", "_")
    content_filename = f"{data_folder}/{preprocessed_company_name}_{preprocessed_position_name}_cover_letter_content.txt"
    with open(content_filename, "w") as file:
        file.write(cover_letter_content)
    
    # open content.txt in editor
    os.system(f"open {content_filename}")
    
    input("Press Enter after revising: ")
    # export the content.txt to Application-letter.tex
    write_application_letter(tmp_dir, content_filename)

    # compile pdf
    if debug:
        os.system(f"cd {tmp_dir} && pdflatex main.tex")
    else:
        # hide stdout from pdflatex
        os.system(f"cd {tmp_dir} && pdflatex main.tex >/dev/null 2>&1")

    ## create output folder
    output_folder = f"output/{datetime.date.today().strftime('%y%m%d')}"
    os.makedirs(output_folder, exist_ok=True)
    
    # move file
    os.rename(f"{tmp_dir}/main.pdf", f"{output_folder}/{preprocessed_company_name}_{preprocessed_position_name}.pdf")

    # open file
    os.system(f"open {output_folder}/{preprocessed_company_name}_{preprocessed_position_name}.pdf")


if __name__ == "__main__":
    fire.Fire(main)
