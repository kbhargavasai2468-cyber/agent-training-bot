from flask import Flask, render_template, request, jsonify, session
from groq import Groq

app = Flask(__name__)
app.secret_key = "agentbot_secret_2024"

client = None

TRAINING_DATA = """
=== REAL ESTATE AGENT TRAINING MANUAL ===

COMPANY: SriVarma Properties
REGION: Hyderabad, Telangana

--- PLOT PRICING ---
- Plots range from ₹15 Lakhs to ₹2 Crores depending on location and size
- Premium zones: Shamshabad, Adibatla, Tukkuguda (near airport)
- Mid-range zones: Chevella, Shadnagar, Kothur
- Budget zones: Vikarabad, Tandur, Parigi
- Price per sq yard: ₹3,000 to ₹25,000

--- DOCUMENT CHECKLIST ---
Required documents from buyer:
1. Aadhaar Card (mandatory)
2. PAN Card (mandatory)
3. Passport size photos (2)
4. Bank statement (last 6 months)
5. Income proof (salary slip or ITR)

Documents company provides:
1. Sale Deed (registered)
2. Pattadar Passbook
3. Link Documents (chain of title)
4. Adangal (land records)
5. DTCP/HMDA approval
6. EC (Encumbrance Certificate)
7. Soil Report

--- SITE VISIT PROCESS ---
Step 1: Confirm customer interest via call/WhatsApp
Step 2: Schedule visit (weekdays 10AM-5PM, weekends 9AM-6PM)
Step 3: Assign agent to accompany customer
Step 4: Send WhatsApp confirmation with location pin
Step 5: Follow up within 24 hours after visit
Step 6: Note customer feedback and interest level

--- BOOKING PROCESS ---
1. Customer confirms interest after site visit
2. Token amount: ₹25,000 to ₹1,00,000 depending on plot value
3. Sale agreement signed within 7 days
4. Registration at Sub-Registrar office within 30-45 days
5. Balance payment via RTGS/NEFT/DD
6. Documents handed over after full payment

--- PROFIT SHARING (AGENT COMMISSION) ---
- Plot sale below ₹50 Lakhs: 1.5% commission
- Plot sale ₹50L to ₹1 Crore: 2% commission
- Plot sale above ₹1 Crore: 2.5% commission
- Referral bonus: ₹5,000 per successful referral
- Target bonus: Extra ₹20,000 if monthly target of 3 sales achieved

--- MAINTENANCE & AMENITIES ---
Monthly maintenance: ₹500 to ₹2,000 depending on plot size
Amenities included:
- 24/7 security
- CC cameras
- Roads (BT roads inside layout)
- Underground drainage
- Electricity connection (ready)
- Water supply (borewell)
- Parks and open spaces
- Compound wall

--- COMMON CUSTOMER OBJECTIONS ---
Q: Is this DTCP approved?
A: Yes, all our layouts are DTCP/HMDA approved. We provide official approval documents.

Q: What about loan facility?
A: We have tie-ups with SBI, HDFC, Axis Bank for plot loans up to 70% of property value.

Q: Is the road access good?
A: All layouts are on main road or within 500 meters of main road.

Q: What is the resale value?
A: Historically our plots appreciate 15-25% per year in growth corridors.

--- AGENT DO'S AND DON'TS ---
DO:
- Always greet customer by name
- Respond within 2 hours to any inquiry
- Always carry visiting card and brochure
- Take photos/videos during site visit
- Update CRM after every customer interaction

DON'T:
- Never promise exact returns or appreciation %
- Never share pricing without manager approval
- Never badmouth competitors
- Never collect cash directly from customer
- Never sign any document without manager review

--- TELUGU PHRASES FOR AGENTS ---
Welcome: స్వాగతం (Swagatam)
How can I help: నేను మీకు ఎలా సహాయం చేయగలను
Plot price: స్థలం ధర
Site visit: సైట్ విజిట్
Documents: పత్రాలు
Registration: రిజిస్ట్రేషన్
Commission: కమీషన్
"""

def get_ai_response(user_message, language, conversation_history):
    global client

    lang_instruction = ""
    if language == "Telugu":
        lang_instruction = "Respond ONLY in Telugu script (తెలుగు లిపి)."
    elif language == "Bilingual":
        lang_instruction = "Respond in English first, then provide Telugu translation below it."
    else:
        lang_instruction = "Respond in English."

    system_prompt = f"""You are an intelligent training assistant for SriVarma Properties, a real estate company in Hyderabad, India.
Your job is to help real estate agents learn about company policies, processes, pricing, documents, and best practices.

TRAINING KNOWLEDGE BASE:
{TRAINING_DATA}

LANGUAGE INSTRUCTION: {lang_instruction}

RESPONSE STYLE:
- Be helpful, clear, and professional
- Use bullet points for lists
- Keep answers concise but complete
- If asked something not in training data, say "This topic is not covered in current training material. Please contact your manager."
- Always encourage the agent
- You are ONLY a training assistant for real estate agents. Do not answer unrelated questions."""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history[-6:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=600,
        temperature=0.7
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    session['conversation'] = []
    return render_template('index.html')

@app.route('/setup', methods=['POST'])
def setup():
    global client
    data = request.json
    api_key = data.get('api_key', '').strip()

    if not api_key:
        return jsonify({'success': False, 'error': 'Please enter your API key'})

    try:
        client = Groq(api_key=api_key)
        # Test call
        test = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say hi"}],
            max_tokens=5
        )
        if test.choices[0].message.content:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'No response from API'})
    except Exception as e:
        client = None
        return jsonify({'success': False, 'error': str(e)})

@app.route('/chat', methods=['POST'])
def chat():
    global client
    if not client:
        return jsonify({'error': 'API not configured. Please enter your API key first.', 'success': False})

    data = request.json
    user_message = data.get('message', '').strip()
    language = data.get('language', 'English')

    if not user_message:
        return jsonify({'error': 'Empty message', 'success': False})

    if 'conversation' not in session:
        session['conversation'] = []

    conversation = session['conversation']

    try:
        response = get_ai_response(user_message, language, conversation)
        conversation.append({"role": "user", "content": user_message})
        conversation.append({"role": "assistant", "content": response})
        session['conversation'] = conversation[-12:]
        session.modified = True
        return jsonify({'response': response, 'success': True})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}', 'success': False})

@app.route('/reset', methods=['POST'])
def reset():
    session['conversation'] = []
    return jsonify({'success': True})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
