import os
from io import StringIO
import requests
import pandas as pd
import streamlit as st
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DataFrameLoader
import re
import sys
from dotenv import load_dotenv
# List of API keys (replace with your actual keys)
load_dotenv()
api_keys = [os.getenv('API_KEY1'), os.getenv('API_KEY2')]


# Function to get the next API key
def get_next_api_key():
    # Rotate the list and return the first key
    api_keys.append(api_keys.pop(0))
    return api_keys[0]

def get_google_sheet_data(google_sheet_link):
    last_slash_index = google_sheet_link.rfind('/')
    if last_slash_index != -1:
        export_link = google_sheet_link[:last_slash_index] + '/export?format=csv'
        response = requests.get(export_link)
        data = pd.read_csv(StringIO(response.text))
        data = data.to_json(orient='records', lines=True)
        return data
    else:
        return None

def function_for_g1():
    # Function logic for Grade 1
    pass

def function_for_g2():
    # Function logic for Grade 2
    pass


def function_for_g3():
    # Function logic for Grade 3
    pass

def function_for_g4():
    # Function logic for Grade 4
    pass

def function_for_g5():
    # Function logic for Grade 5
    pass

def function_for_g6():
    # Function logic for Grade 6
    pass

def function_for_g7():
    # Function logic for Grade 7
    pass

def function_for_g8():
    # Function logic for Grade 8
    pass

def function_for_g9():
    # Function logic for Grade 9
    pass

def function_for_g10():
    # Function logic for Grade 10
    pass

def function_for_g11():
    # Function logic for Grade 11
    pass

def function_for_g12():
    google_sheet_link = 'https://docs.google.com/spreadsheets/d/1RtkxiuY-JC0edTMJu2zURtdDEUUGGIq3IBje-LMqgxE/export?format=csv&gid=12929141'
    data = get_google_sheet_data(google_sheet_link)



    google_sheet_link_1 = 'https://docs.google.com/spreadsheets/d/1OqNRcee32NNRdkhO27c-dyKFe_J7vKtiFto66FPXid4/export?format=csv&gid=364006582'
    data_1 = get_google_sheet_data(google_sheet_link_1)
    return data,data_1




def create_llm_chains(api_key):
    # Set the API key for the llm
    os.environ['OPENAI_API_KEY'] = api_key
    llm = ChatOpenAI(model_name='gpt-4-1106-preview', temperature=0.3)

    # Define LLMChains
    template_1 = """Your Role: You are a US educational assessment developer and have master's degrees and/or PhDs in both education and psychology.
You have deep knowledge and understanding of all US educational test standards for grade school levels for {grade}.
You also possess extensive knowledge and understanding of all grade level test frameworks in the US, including MAP, ISEE, SSAT, STAAR, NAEP, Common Core/CCSS, NGSS, IXL Skills, etc.
Keep tracks of steps and generate response with step number mentioned.

Objectives: Analyze ELA (English Language Arts) test questions and items and find the alignments to CCSS Codes and IXL Skill Codes that are highly accurate.

Step 1a) Analyze this test question and the test items:
{question}
"""
    prompt_template_1 = PromptTemplate(input_variables=['grade','question'], template=template_1)
    chain_1 = LLMChain(llm=llm, prompt=prompt_template_1, output_key="Step_1")

    template_2 = """
{question}

Step 2 )Map the CCSS Codes alignment to the Test Question and Test Items.

There may be more than CCSS Codes aligned, include all that match perfectly.

Print the CCSS  Code(s) you have found that have alignment.

If it doesnt match perfectly, clearly state that and give closest match from data.

Precisely follow below format for answering:

Correct Perfect Match: Give correct perfect match from data

Closest Match: Give the match that is closest from data

Explantaion for both:

Use below data to answer for above Step 2:
Google Sheet----"CCSS Subject Standards Compiled | ELA Grade 11-12":

{data}

"""
    prompt_template_2 = PromptTemplate(input_variables=[ "data", 'question'], template=template_2)
    chain_2 = LLMChain(llm=llm, prompt=prompt_template_2, output_key="Step_2")

    template_3 = """
{question}

Step 3)Map the IXL Skill Codes alignment to the Test Question and Test Items.

There may be more than IXL Skill Codes aligned, include all that match perfectly.

Print the IXL Skill Code(s) you have found that have alignment. Important Note: Use key 'IXL SKILL CODE' for your answer.

If it doesnt match perfectly, clearly state that and give closest match from data.

Precisely follow below format for answering:

Correct Perfect Match: Give correct perfect match from data ('IXL SKILL CODE')

Closest Match (It should always be there) : Give the match that is closest from data ('IXL SKILL CODE')

Explantaion for both:


Use below data to answer for above Step 3):

These are IXL Language Skill Codes in the {grade} Skill Plan.
Google Sheet------Language {grade} | IXL Skill Plan:

{data_1}

"""
    prompt_template_3 = PromptTemplate(input_variables=['grade', "data_1", 'question'], template=template_3)
    chain_3 = LLMChain(llm=llm, prompt=prompt_template_3, output_key="Step_3")

    template_4 = """
{question}

{Step_3}

Step 4a) First reverify your previous analysis in step 3b for accuracy, update your analysis output as required to proceed with step 4b.

Step 4b) Your Analysis must include Each of the Items (principial elements) in the Example Question 1 below, Print your analysis in the same format:
	The following test question and test items (principal elements) serve only as an example for the format and details of the test items you need to generate.
	Do NOT copy the example test question and items verbatim! Do not generate a new test item or answer options.
	You must only base you response on your previous analysis and responses from Steps 1, 2, 3a, 3b, 4a.

	- **Question ID**:
	### Example Question 1
	- **Passage**: None required.
	- **Question Type**: Multiple-choice (Language - L).
	- **Question**: "Choose the sentence that demonstrates correct comma usage for an introductory element."
	- **CCSS Codes Aligned**: L.12.2a.
	- **CCSS Alignment Explanation**: This question assesses understanding of colon usage in sentence structure.
	- **IXL Skills Assessed**: ZZ.1: Use commas correctly.
	- **Answer Options**:
	A) Before the movie starts, I want to buy some popcorn.
	B) Before the movie starts I want to buy some popcorn.
	C) Before the movie starts; I want to buy some popcorn.
	D) Before the movie starts: I want to buy some popcorn.
	- **Answer**: A) Before the movie starts, I want to buy some popcorn.
	- **Skills Assessed**: Punctuation and grammar.
	Clearly state if the IXL Skill Code is present in the {grade} Skill Plan or NOT.

Use this data:
Google Sheet----Language {grade} | Current IXL Skill Plan:
{data_1}

Always re-verify you are maintaining the requirements provided in previous steps 1, 2, 3a, 3b, 4a, 4b as you generate the analysis items before you print.
"""
    prompt_template_4 = PromptTemplate(input_variables=['grade',"Step_3", 'question','data_1'], template=template_4)
    chain_4 = LLMChain(llm=llm, prompt=prompt_template_4, output_key="Step_4")


    template_5 = """
{question}

{Step_4}

Step 5) Re-analyze your response from Step 4b (the test question and related test items) and re-verify for accuracy (as in the following test items) you have generated thoroughly and make corrections and updates as required.
	The following test question and test items (principal elements) serve only as an example for the format and details of the test items you need to generate.
	Do NOT copy the example test question and items verbatim! Do not generate new a new test item or answer options.
	You must only base you response on your previous analysis and responses from Steps 1, 2, 3a, 3b, 4a, 4b.

	- **Question ID**:
	### Example Question 1
	- **Passage**: None required.
	- **Question Type**: Multiple-choice (Language - L).
	- **Question**: "Choose the sentence that demonstrates correct comma usage for an introductory element."
	- **CCSS Codes Aligned**: L.12.2a.
	- **CCSS Alignment Explanation**: This question assesses understanding of colon usage in sentence structure.
	- **IXL Skills Assessed**: ZZ.1: Use commas correctly.
	- **Answer Options**:
	A) Before the movie starts, I want to buy some popcorn.
	B) Before the movie starts I want to buy some popcorn.
	C) Before the movie starts; I want to buy some popcorn.
	D) Before the movie starts: I want to buy some popcorn.
	- **Answer**: A) Before the movie starts, I want to buy some popcorn.
	- **Skills Assessed**: Punctuation and grammar.
	Clearly state if the IXL Skill Code is present in the {grade} Current Skill Plan or NOT.

Reverify the IXL Skill Code(s) identified as aligned with the test question and test items are present in the IXL Skill Plan for {grade}

Use this data:
Google Sheet-----Language {grade} | Current IXL Skill Plan:
{data_1}

Re-print all the items with updates in the required format (example format given in step 5) if a refinement to your analysis needs to made.

"""
    prompt_template_5 = PromptTemplate(input_variables=['grade',"Step_4", 'question','data_1'], template=template_5)
    chain_5 = LLMChain(llm=llm, prompt=prompt_template_5, output_key="Step_5")
    return chain_1, chain_2, chain_3, chain_4, chain_5

def execute_analysis_chain(grade, question, chain_1, chain_2,chain_3,chain_4,chain_5,chain_type):

    def normalize_grade_input(grade):
     # Convert to lower case and remove spaces
     normalized_grade = grade.lower().replace(" ", "")

    # Extracting the grade number
     if normalized_grade.startswith("grade") and normalized_grade[5:].isdigit():
        grade_number = int(normalized_grade[5:])
     elif normalized_grade.startswith("g") and normalized_grade[1:].isdigit():
        grade_number = int(normalized_grade[1:])
     else:
        return None

    # Return the neat format
     return f"Grade {grade_number}"

    grade  = normalize_grade_input(grade)

    function_mapping = {
    "Grade 1": function_for_g1,
    "Grade 2": function_for_g2,
    "Grade 3": function_for_g3,
    "Grade 4": function_for_g4,
    "Grade 5": function_for_g5,
    "Grade 6": function_for_g6,
    "Grade 7": function_for_g7,
    "Grade 8": function_for_g8,
    "Grade 9": function_for_g9,
    "Grade 10": function_for_g10,
    "Grade 11": function_for_g11,
    "Grade 12": function_for_g12,
}


    try:
      data,data_1 = function_mapping.get(grade)()
    except:
      st.write("<p style='color:red;'>Please Enter Correct Grade!</p>", unsafe_allow_html=True)

      sys.exit(1)



    if "CCSS" in chain_type and "XLI" not in chain_type:
        st.write("You selected CCSS only. Executing CCSS function...")
        result = chain_2({"data": data, 'question': question})
        Step_2 = result['Step_2']
        return None, Step_2, None, None, None

    elif "XLI" in chain_type and "CCSS" not in chain_type:
        st.write("You selected XLI only. Executing XLI function...")
        result = chain_3({'grade': grade, 'data_1': data_1, 'question': question})
        Step_3 = result['Step_3']
        return None, None, Step_3, None, None

    elif "CCSS" in chain_type and "XLI" in chain_type:
        st.write("You selected both CCSS and XLI. Executing combined function...")
        result_1 = chain_2({"data": data, 'question': question})
        result_2 = chain_3({'grade': grade, 'data_1': data_1, 'question': question})
        Step_2 = result_1['Step_2']
        Step_3 = result_2['Step_3']
        return None, Step_2, Step_3, None, None

    else:
        st.write("<p style='color:red;'>Incorrect Code Type!</p>", unsafe_allow_html=True)
        sys.exit(1)





def main():
    st.title("Educational Assessment and Play Review App")

    # Load data from Google Sheets

    # loader = DataFrameLoader(data, page_content_column="Category")
    # data = loader.load()
    # data = data.to_csv(index=True, header=True, line_terminator=', , , , , , , , , , , , , , , , , , , , , , , , , , , , \n')



    # loader = DataFrameLoader(data_1, page_content_column="CCSS Code")
    # data_1 = loader.load()
    # data_1 = data_1.to_csv(index=True, header=True, line_terminator=', , , , , , , , , , , , , , , , , , , , , , , , , , , , \n')

    grade = st.text_area("Enter your grade:")
    questions_link = st.text_area("Please Provide sheet link with questions")
    chain_type = st.text_area("What do you want to evaluate? Separate by commas for multiple options:\n a) CCSS\n b) XLI")


    if st.button("Run Analysis"):
        chain_type = [option.strip().upper() for option in chain_type.split(',')]

        try:
         question_data = get_google_sheet_data(questions_link)
         questions = pd.read_json(question_data, orient='records', lines=True)
        except:
          st.write("<p style='color:red;'>Incorrect Question Link!</p>", unsafe_allow_html=True)
          sys.exit(1)


        # questions = pd.read_csv(StringIO(question_data))

        for i, row in questions.iterrows():
            # Get the next API key and create LLM chains
            api_key = get_next_api_key()
            print(api_key)
            chain_1, chain_2, chain_3, chain_4, chain_5 = create_llm_chains(api_key)

            question_col = row.index[0]
            question = row[question_col]
            question_id_match = re.search(r'\d+', question)
            question_id = question_id_match.group() if question_id_match else 'Not Found'

            with st.spinner("Running analysis..."):
                Step_1, Step_2, Step_3, Step_4, Step_5 = execute_analysis_chain(
                    grade,question, chain_1, chain_2, chain_3, chain_4, chain_5,chain_type
                )

            st.subheader(f"Results for Question ID: {question_id}")
            data = {
    "Step_1": Step_1,
    "Step_2": Step_2,
    "Step_3": Step_3,
    "Step_4": Step_4,
    "Step_5": Step_5
}
            filtered_data = {k: v for k, v in data.items() if v is not None}

            st.write(filtered_data)
if __name__ == "__main__":
    main()
