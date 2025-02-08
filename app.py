from flask import Flask, render_template, request, jsonify, url_for
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def home():
    return render_template('valueprop.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get form data for framework
    situation = request.form.get('situation', '')
    current_way = request.form.get('current_way', '')
    problems = request.form.get('problems', '')
    capabilities = request.form.get('capabilities', '')
    product_features = request.form.get('product_features', '')
    benefits = request.form.get('benefits', '')
    
    # Get custom prompts
    framework_prompt = request.form.get('framework_prompt', '')
    homepage_prompt = request.form.get('homepage_prompt', '')
    social_prompt = request.form.get('social_prompt', '')
    
    # Get section if specified
    section = request.form.get('section')

    # Construct the prompt based on section
    if section == 'framework':
        prompt = f"""SECTION 1 - Value Proposition Framework:
Create a structured value proposition using this input:
Situation: {situation}
Current Way: {current_way}
Problem(s): {problems}
Capability(ies): {capabilities}
Product Category/Feature(s): {product_features}
Benefit(s): {benefits}
Additional Instructions: {framework_prompt}"""
    elif section == 'homepage':
        prompt = f"""SECTION 2 - Homepage Copy:
Create a homepage copy following exactly this structure:
We are... {product_features}
That helps... {situation}
Dealing with... {problems}
Solved by... {capabilities}
Additional Instructions: {homepage_prompt}"""
    elif section == 'social':
        prompt = f"""SECTION 3 - Social Media Copy:
Create the following social media content:
1. LinkedIn post (max 200 words)
2. Twitter/X post (max 280 characters)
3. Three potential taglines (max 10 words each)
4. Three hashtag suggestions
Additional Instructions: {social_prompt}"""
    else:
        # Original full prompt for initial generation
        prompt = f"""Please provide three separate sections:

SECTION 1 - Value Proposition Framework:
Create a structured value proposition using this input:
Situation: {situation}
Current Way: {current_way}
Problem(s): {problems}
Capability(ies): {capabilities}
Product Category/Feature(s): {product_features}
Benefit(s): {benefits}
Additional Instructions: {framework_prompt}

SECTION 2 - Homepage Copy:
Create a homepage copy following exactly this structure:
We are... {product_features}
That helps... {situation}
Dealing with... {problems}
Solved by... {capabilities}
Additional Instructions: {homepage_prompt}

SECTION 3 - Social Media Copy:
Create the following social media content:
1. LinkedIn post (max 200 words)
2. Twitter/X post (max 280 characters)
3. Three potential taglines (max 10 words each)
4. Three hashtag suggestions
Additional Instructions: {social_prompt}

Format your response with clear section headers and keep each section concise and impactful."""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional copywriter and value proposition expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Extract the generated content
        generated_content = response.choices[0].message.content

        return jsonify({"success": True, "content": generated_content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
