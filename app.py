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

    try:
        if section:
            # For single section regeneration
            if section == 'framework':
                prompt = f"""Create a structured value proposition following exactly this format:

Situation: {situation}
- Describe: {situation}

Current Way:
- Current approach: {current_way}

Problem(s):
- Key challenges: {problems}

Capability(ies):
- Our solution: {capabilities}

Product Category/Feature(s):
- What we offer: {product_features}

Benefit(s):
- Value delivered: {benefits}

Additional Instructions: {framework_prompt}

Please maintain this exact structure in your response, elaborating on each section while keeping the format."""

            elif section == 'homepage':
                prompt = f"""Create a homepage copy following exactly this four-line structure:

We are... {product_features}
That helps... {situation}
Dealing with... {problems}
Solved by... {capabilities}

Additional Instructions: {homepage_prompt}

Important: Maintain exactly these four lines starting with 'We are...', 'That helps...', 'Dealing with...', and 'Solved by...' in your response."""

            elif section == 'social':
                prompt = f"""Create the following social media content:
1. LinkedIn post (max 200 words)
2. Twitter/X post (max 280 characters)
3. Three potential taglines (max 10 words each)
4. Three hashtag suggestions
Additional Instructions: {social_prompt}"""

            elif section == 'positioning-context':
                prompt = f"""Create a positioning statement using the following structure and incorporating insights from the previous sections:

For {request.form.get('target_customer', '[derived from context]')}
Who {request.form.get('need_statement', situation)}
Our product {request.form.get('product_name', product_features)} is {request.form.get('product_category', '[derived from context]')}
That {request.form.get('key_benefit', benefits)}
Unlike {request.form.get('competitive_alt', current_way)}
Our product {request.form.get('differentiation', capabilities)}
Proven by {request.form.get('social_proof', '[derived from context]')}

Use the structure above but incorporate insights from:
Situation: {situation}
Current Way: {current_way}
Problems: {problems}
Capabilities: {capabilities}
Product Features: {product_features}
Benefits: {benefits}

Important: Maintain exactly this seven-line structure in your response."""

            elif section == 'positioning-standalone':
                prompt = f"""Create a positioning statement using exactly this structure:

For {request.form.get('target_customer', 'N/A')}
Who {request.form.get('need_statement', 'N/A')}
Our product {request.form.get('product_name', 'N/A')} is {request.form.get('product_category', 'N/A')}
That {request.form.get('key_benefit', 'N/A')}
Unlike {request.form.get('competitive_alt', 'N/A')}
Our product {request.form.get('differentiation', 'N/A')}
Proven by {request.form.get('social_proof', 'N/A')}

Important: Maintain exactly this seven-line structure in your response, using only the provided inputs."""
        else:
            # Original full prompt for initial generation
            prompt = f"""Please provide three separate sections:

SECTION 1 - Value Proposition Framework:
Create a structured value proposition following exactly this format:

Situation: {situation}
- Describe: {situation}

Current Way:
- Current approach: {current_way}

Problem(s):
- Key challenges: {problems}

Capability(ies):
- Our solution: {capabilities}

Product Category/Feature(s):
- What we offer: {product_features}

Benefit(s):
- Value delivered: {benefits}

Additional Instructions: {framework_prompt}

SECTION 2 - Homepage Copy:
Create a homepage copy following exactly these four lines:

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

SECTION 4 - Qollabi Positioning (Context-Based):
Create a positioning statement using the following structure and incorporating insights from previous sections:

For {request.form.get('target_customer', '[derived from context]')}
Who {request.form.get('need_statement', situation)}
Our product {request.form.get('product_name', product_features)} is {request.form.get('product_category', '[derived from context]')}
That {request.form.get('key_benefit', benefits)}
Unlike {request.form.get('competitive_alt', current_way)}
Our product {request.form.get('differentiation', capabilities)}
Proven by {request.form.get('social_proof', '[derived from context]')}

SECTION 5 - Qollabi Positioning (Standalone):
Create a positioning statement using exactly this structure:

For {request.form.get('target_customer', 'N/A')}
Who {request.form.get('need_statement', 'N/A')}
Our product {request.form.get('product_name', 'N/A')} is {request.form.get('product_category', 'N/A')}
That {request.form.get('key_benefit', 'N/A')}
Unlike {request.form.get('competitive_alt', 'N/A')}
Our product {request.form.get('differentiation', 'N/A')}
Proven by {request.form.get('social_proof', 'N/A')}

Important: Maintain the exact structure for each section. For the homepage copy, keep exactly the four lines starting with 'We are...', 'That helps...', 'Dealing with...', and 'Solved by...'."""

        # Call OpenAI API with a stronger system message
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional copywriter and value proposition expert. Always maintain the exact structure provided in the prompt. For frameworks, keep all sections. For homepage copy, maintain the exact four-line format."},
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
