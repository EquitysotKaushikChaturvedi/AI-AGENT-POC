import os
import json
from typing import Dict, Any
from app.llm_provider import generate_ai_response

import random

def generate_response(intent: str, context: Dict[str, Any], message: str) -> str:
    """
    Generates a context-aware response using the configured AI provider.
    
    Args:
        intent (str): The detected intent of the user.
        context (Dict[str, Any]): The business profile data.
        message (str): The original user message.
        
    Returns:
        str: The generated response text.
    """

    try:
        # Construct a prompt that includes the persona and context
        company_name = context.get('company_name', 'our company')
        founded_year = context.get('founded_year', 'Unknown')
        tone = context.get('tone', 'professional')
        services = json.dumps(context.get('services', []), indent=2)
        leadership = json.dumps(context.get('leadership', []), indent=2)
        
        # Safety Guard for Out-of-Scope Queries
        if intent == "unknown":
            return "I can share information related to our company, leadership, and services. Please let me know how I can help within that scope."

        # Friendly Greeting Handler (Randomized)
        if intent == "greeting":
            greetings = [
                "Hello! I’m here to help with information about our company and services.",
                "Hi there. Feel free to ask about our leadership, services, or business offerings.",
                "Welcome. I can assist with details about our company or how we support businesses.",
                "Hello. Let me know what you’d like to learn about our organization.",
                "Greetings. I am ready to answer your questions about our mission, team, and services.",
                "Hi! How can I help you learn more about our business today?"
            ]
            return random.choice(greetings)

        # Special handling for leadership/founders to avoid excessive promotion
        # Now triggered directly by the granular 'leadership_info' intent
        if intent == "leadership_info":
            founders_list = context.get('leadership', [])
            if not founders_list:
                return "I apologize, but I don't have information about the company's leadership available at the moment."
            
            # Deterministic formatting
            formatted_leadership = ", ".join([f"{p['name']} ({p['role']})" for p in founders_list])
            
            instruction_override = f"""
            The user is asking about leadership.
            You MUST stick to these exact facts: {formatted_leadership}.
            Do NOT add promotional adjectives like "visionary", "esteemed", "highly respected".
            Do NOT invent background stories.
            Just state the names and roles clearly and professionally in a natural sentence.
            """
        else:
            instruction_override = ""

        system_instruction = f"""
        You are the AI assistant for {company_name}.
        
        # BUSINESS DATA (STRICT SOURCE OF TRUTH)
        - Company Name: {company_name}
        - Founded Year: {founded_year}
        - Mission: {context.get('mission')}
        - Leadership/Founders: {leadership}
        - Services: {services}
        - Target Audience: {context.get('target_audience')}
        - Tone: {tone}
        - Contact: {context.get('contact_info')}
        
        # INSTRUCTIONS
        - The user's intent was detected as: '{intent}'.
        {instruction_override}
        - IF asked about founders, directors, or leadership: You MUST list the names and roles explicitly from the 'Leadership/Founders' data.
        - IF asked about services: Only list services explicitly present in the 'Services' list. Do NOT hallucinate.
        - IF asked multiple questions (e.g. "Who founded it and what do you do?"): Answer ALL parts of the question clearly.
        - IF data is missing: State clearly that the information is not available.
        - IF asked multiple questions (e.g. "Who founded it and what do you do?"): Answer ALL parts of the question clearly.
        - IF data is missing: State clearly that the information is not available.
        - Maintain a friendly, conversational, and professional tone.
        
        # TONE & STYLE RULES
        - Be WARM and NATURAL. Write like a helpful human, not a bot.
        - If the user uses respectful language (e.g., "sir", "please"), respond with equal warmth and politeness.
        - Avoid stiff corporate speak. Use clear, simple, and confident language.
        - It is okay to sound enthusiastic about the company's mission or leaders.
        
        # RESPONSE VARIATION RULES (STRICT)
        - DO NOT start the response with "Thank you for your interest in..." or similar robotic greetings.
        - VARY your opening sentence. Start directly with the answer sometimes.
        - Use professional openers like "{company_name} was founded in...", "We specialize in...", etc.
        - Never repeat the exact same opening sentence twice in a row.
        - Make the response sound human-written, not like a template. 
        
        # FORMATTING RULES (CRITICAL)
        - Return the answer as CLEAN, PLAIN ENGLISH TEXT only.
        - DO NOT use Markdown formatting (no bold **, no headers #, no bullets -).
        - DO NOT use lists or bullet points. Write in complete sentences and paragraphs.
        - DO NOT include literal newline characters (\\n) in the output. Keep the flow continuous.
        - The output should look like a natural conversation from a senior representative.
        """
        
        full_prompt = f"{system_instruction}\n\nUser Message: {message}\n\nResponse:"
        
        return generate_ai_response(full_prompt)
        
    except Exception as e:
        print(f"Error in response generation: {e}")
        return "I apologize, but I'm having trouble formulating a response right now. Please try again later."
