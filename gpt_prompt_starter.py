"""
Starter Code for passing a survey to GPT using OpenAI's API
Authors - Nirali Parekh, Johan Ugander (updated Jan 2026 for gpt-4o-mini)

SETUP INSTRUCTIONS
==================
1. Install the OpenAI Python package:
       pip install openai

2. Get your API key from OpenAI:
   - Go to https://platform.openai.com/api-keys
   - Sign in or create an account
   - Click "Create new secret key"
   - Copy the key (it starts with "sk-")
   - IMPORTANT: You won't be able to see the key again, so save it somewhere safe

3. Set your API key as an environment variable:

   On macOS/Linux (add to ~/.bashrc or ~/.zshrc for persistence):
       export OPENAI_API_KEY='sk-your-key-here'

   On Windows (Command Prompt):
       set OPENAI_API_KEY=sk-your-key-here

   On Windows (PowerShell):
       $env:OPENAI_API_KEY='sk-your-key-here'

4. Set a spending limit to avoid unexpected charges:
   - Go to https://platform.openai.com/account/billing/overview
   - Set a usage limit (e.g., $5)

5. Run this script:
       python gpt_prompt_starter.py
"""

import csv
import random
from openai import OpenAI

# Initialize the OpenAI client
# The client automatically reads the OPENAI_API_KEY environment variable.
# If you prefer to set it directly (not recommended for shared code), use:
#     client = OpenAI(api_key='sk-your-key-here')
client = OpenAI()

csv_file = 'comma-survey.csv'

# Function to generate GPT prompts based on age and gender
def generate_gpt_prompts(data):
    prompts = []
    for row in data:
        age = row['Age']
        gender = row['Gender']
        # Define the survey prompt - modify it based on the dataset information.
        # Customize the prompt format as needed, providing the multiple choices to GPT
        prompt = f"""
        You are {age} years old {gender} [...additional demographic information]
        You are invited to participate in a survey.
        Please answer the following questions:
        1.
        2.
        3.
        4. [...Additional survey questions...]
        """.format(age="AGE_FROM_CSV", gender="GENDER_FROM_CSV")
        prompts.append(prompt)
    return prompts

# Function to poll GPT
def poll_gpt(gpt_prompts, num_responses):
    responses = []
    for i in range(num_responses):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective model for this assignment
            messages=[
                {"role": "user", "content": gpt_prompts[i]}
            ],
            max_tokens=100,  # Adjust based on the expected response length
            n=1,  # Number of responses to generate
            temperature=1.0,  # Adjust for response variability
        )
        responses.append(response.choices[0].message.content.strip())
    return responses

# Load survey data from csv
survey_data = []
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        survey_data.append(row)

# Randomly select 300 rows (you can use a more sophisticated method for randomness). Set seed if needed.
num_responses = 3 #3 to test, 300 later
selected_data = random.sample(survey_data, num_responses)

# Generate GPT prompts based on the demographics
gpt_prompts = generate_gpt_prompts(selected_data)

# Poll GPT for survey responses (e.g. poll 300 GPT responses)
gpt_responses = poll_gpt(gpt_prompts, num_responses)

# Save the responses to a CSV file after processing them as needed
with open('gpt_survey.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Age", "Gender", "Income", "Education", "Location", "Response1", "Response2", ...])  # Add more columns for additional responses
    for response in gpt_responses:
        writer.writerow(["", "", "", "", "", response, "", ...])  # Fill in demographics as per data
