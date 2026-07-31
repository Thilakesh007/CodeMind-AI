import os
from app.config_manager import load_config

# For fallback local models
import ollama

def generate_response(prompt: str, history: list = None, stream: bool = False):
    config = load_config()
    provider = getattr(config, "ai_provider", "ollama").lower()
    
    messages = []
    if history:
        for msg in history:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
    
    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        if provider == "openai":
            return _generate_openai(messages, config, stream)
        elif provider == "anthropic":
            return _generate_anthropic(messages, config, stream)
        elif provider == "gemini":
            return _generate_gemini(messages, config, stream)
        else:
            return _generate_ollama(messages, config, stream)
    except Exception as e:
        if stream:
            def error_gen():
                yield f"Error calling {provider}: {str(e)}"
            return error_gen()
        else:
            return f"Error calling {provider}: {str(e)}"

def _generate_ollama(messages, config, stream):
    host = os.environ.get("OLLAMA_HOST", config.ollama_host)
    client = ollama.Client(host=host)
    model_name = config.primary_model
    
    if stream:
        response = client.chat(
            model=model_name,
            messages=messages,
            stream=True
        )
        for chunk in response:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
    else:
        response = client.chat(
            model=model_name,
            messages=messages,
            stream=False
        )
        return response["message"]["content"]

def _generate_openai(messages, config, stream):
    import openai
    api_key = getattr(config, "openai_api_key", "")
    if not api_key:
        raise ValueError("OpenAI API key is missing.")
    
    client = openai.OpenAI(api_key=api_key)
    
    # We could allow setting the model specifically for OpenAI, but let's default for now
    model_name = "gpt-4o-mini" 
    
    if stream:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    else:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content

def _generate_anthropic(messages, config, stream):
    import anthropic
    api_key = getattr(config, "anthropic_api_key", "")
    if not api_key:
        raise ValueError("Anthropic API key is missing.")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Convert role array for Anthropic
    anthropic_msgs = []
    system_prompt = ""
    for m in messages:
        if m["role"] == "system":
            system_prompt = m["content"]
        elif m["role"] in ["user", "assistant"]:
            anthropic_msgs.append(m)
        else:
            anthropic_msgs.append({"role": "user", "content": m["content"]})
    
    model_name = "claude-3-5-sonnet-20241022"
    
    if stream:
        with client.messages.stream(
            max_tokens=1024,
            system=system_prompt,
            messages=anthropic_msgs,
            model=model_name,
        ) as stream_resp:
            for text in stream_resp.text_stream:
                yield text
    else:
        response = client.messages.create(
            max_tokens=1024,
            system=system_prompt,
            messages=anthropic_msgs,
            model=model_name,
        )
        return response.content[0].text

def _generate_gemini(messages, config, stream):
    from google import genai
    from google.genai import types
    
    api_key = getattr(config, "gemini_api_key", "")
    if not api_key:
        raise ValueError("Gemini API key is missing.")
    
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash"
    
    gemini_msgs = []
    system_instruction = None
    for m in messages:
        if m["role"] == "system":
            system_instruction = m["content"]
        else:
            role = "user" if m["role"] == "user" else "model"
            gemini_msgs.append({"role": role, "parts": [{"text": m["content"]}]})
            
    # For Gemini, system instructions are passed separately
    kwargs = {}
    if system_instruction:
         kwargs['config'] = types.GenerateContentConfig(system_instruction=system_instruction)
         
    if stream:
        response = client.models.generate_content_stream(
            model=model_name,
            contents=gemini_msgs,
            **kwargs
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    else:
        response = client.models.generate_content(
            model=model_name,
            contents=gemini_msgs,
            **kwargs
        )
        return response.text
