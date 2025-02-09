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
                # Get positioning inputs
                target_customer = request.form.get('target_customer', '').strip()
                need_statement = request.form.get('need_statement', '').strip()
                product_name = request.form.get('product_name', '').strip()
                product_category = request.form.get('product_category', '').strip()
                key_benefit = request.form.get('key_benefit', '').strip()
                competitive_alt = request.form.get('competitive_alt', '').strip()
                differentiation = request.form.get('differentiation', '').strip()
                social_proof = request.form.get('social_proof', '').strip()

                # Get framework content
                framework_content = request.form.get('frameworkContent', '')

                # Create context-aware positioning statement
                prompt = f"""Create a positioning statement that prioritizes the provided positioning inputs and enhances them with framework insights.

First, use these positioning inputs as the primary source:
Target Customer: {target_customer or '[Use framework insight]'}
Need/Opportunity: {need_statement or '[Use framework insight]'}
Product Name: {product_name or '[Use framework insight]'}
Product Category: {product_category or '[Use framework insight]'}
Key Benefit: {key_benefit or '[Use framework insight]'}
Competitive Alternative: {competitive_alt or '[Use framework insight]'}
Primary Differentiation: {differentiation or '[Use framework insight]'}
Social Proof: {social_proof or '[Use framework insight]'}

Then, enhance and fill gaps using these framework insights:
{framework_content}

Additional context from framework:
Situation: {situation}
Current Way: {current_way}
Problems: {problems}
Capabilities: {capabilities}
Product Features: {product_features}
Benefits: {benefits}

Create a positioning statement using exactly this structure:
For [target customer]
Who [statement of need or opportunity]
Our product [product name] is [category]
That [key benefit – compelling reason to buy]
Unlike [primary competitive alternative]
Our product [statement of primary differentiation]
Proven by [credible social proof]

Important: 
1. Prioritize using the positioning inputs when provided
2. Use framework insights to enhance and fill gaps in the positioning
3. Maintain exactly this seven-line structure
4. Each line must start with the exact phrases shown above"""

            elif section == 'positioning-standalone':
                # Only use positioning inputs
                prompt = f"""Create a positioning statement using only the provided inputs:

Target Customer: {request.form.get('target_customer', 'N/A')}
Need/Opportunity: {request.form.get('need_statement', 'N/A')}
Product Name: {request.form.get('product_name', 'N/A')}
Product Category: {request.form.get('product_category', 'N/A')}
Key Benefit: {request.form.get('key_benefit', 'N/A')}
Competitive Alternative: {request.form.get('competitive_alt', 'N/A')}
Primary Differentiation: {request.form.get('differentiation', 'N/A')}
Social Proof: {request.form.get('social_proof', 'N/A')}

Create a positioning statement using exactly this structure:
For [target customer]
Who [statement of need or opportunity]
Our product [product name] is [category]
That [key benefit – compelling reason to buy]
Unlike [primary competitive alternative]
Our product [statement of primary differentiation]
Proven by [credible social proof]

Important:
1. Use ONLY the provided inputs above
2. Do NOT use any framework insights
3. If an input is 'N/A', create appropriate content based on other provided inputs
4. Maintain exactly this seven-line structure
5. Each line must start with the exact phrases shown above"""
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
