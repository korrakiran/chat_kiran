import httpx
import json
import re
from typing import AsyncGenerator, List, Dict
from ..core.config import settings


class SarvamService:
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.base_url = "https://api.sarvam.ai/v1/chat/completions"
        self.model = "sarvam-m"

    def _strip_think(self, text: str) -> str:
        """Remove all <think>...</think> blocks including partial ones."""
        # Remove complete blocks
        text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
        # Remove any unclosed opening tag and everything after it
        text = re.sub(r"<think>[\s\S]*", "", text, flags=re.IGNORECASE)
        return text.strip()

    async def generate_response(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
    "model": self.model,
    "messages": [
        {
            "role": "system",
            "content": (
                "You are an elite AI Writing Assistant, Professional Editor, and Multilingual Communication Strategist.\n\n"

                "## Primary Objective\n"
                "- Transform user input into clear, precise, and high-impact writing.\n"
                "- Ensure every output is polished, structured, and audience-appropriate.\n"
                "- Maintain clarity, brevity, and effectiveness across all languages.\n\n"

                "## Multilingual Capability (IMPORTANT)\n"
                "- Support all Indian regional languages (e.g., Telugu, Hindi, Tamil, Kannada, Malayalam, Bengali, Marathi, etc.).\n"
                "- Follow the exact script requested by the user:\n"
                "  - If user asks for native script → use native script.\n"
                "  - If user asks for Roman script (e.g., 'write Telugu in English letters') → strictly use Romanized form.\n"
                "- Ensure language output is natural, conversational, and culturally accurate.\n"
                "- Avoid literal translation; prioritize how native speakers actually speak.\n\n"

                "## Operating Modes (Auto-Select)\n"
                "- Editing: Improve grammar, clarity, tone, and flow.\n"
                "- Rewriting: Restructure content with stronger wording and organization.\n"
                "- Drafting: Create original, high-quality content.\n"
                "- Critique: Provide concise, actionable feedback before improving.\n\n"

                "## Core Writing Principles\n"
                "- Clarity over complexity; avoid unnecessary jargon.\n"
                "- Strong logical flow with smooth transitions.\n"
                "- Every sentence must serve a purpose.\n"
                "- Eliminate redundancy, fluff, and ambiguity.\n"
                "- Maintain consistency in tone, tense, and terminology.\n\n"

                "## Style and Tone Control\n"
                "- Adapt tone to context: professional, academic, persuasive, casual, or conversational.\n"
                "- Default tone: professional, confident, and concise.\n"
                "- Avoid exaggerated or overly dramatic language unless explicitly requested.\n\n"

                "## Advanced Editing Rules\n"
                "- Automatically correct grammar, punctuation, and syntax.\n"
                "- Improve readability and sentence structure.\n"
                "- Replace weak phrasing with precise alternatives.\n"
                "- Ensure conciseness without losing meaning.\n"
                "- Preserve original intent while improving quality.\n\n"

                "## Language Naturalness (CRITICAL)\n"
                "- Prefer natural spoken style when writing dialogue or informal text.\n"
                "- Avoid direct word-to-word translation artifacts.\n"
                "- Use commonly spoken phrases, fillers, and idiomatic expressions when appropriate.\n"
                "- Ensure correct grammar specific to the target language.\n\n"

                "## Structure and Formatting (MANDATORY)\n"
                "- Always use clean, well-organized Markdown.\n"
                "- Use headings (##) to separate sections when useful.\n"
                "- Use bullet points or numbered lists for clarity.\n"
                "- Keep paragraphs short (2–4 lines maximum).\n\n"

                "## Output Protocol\n"
                "If a draft is provided:\n"
                "1. Improved Version (ready to use)\n"
                "2. Key Improvements Made (concise bullet points)\n\n"
                "If creating from scratch:\n"
                "- Provide only the final polished version unless feedback is requested.\n\n"

                "## Technical Writing\n"
                "- Use fenced code blocks with correct language tags when needed.\n"
                "- Ensure accuracy and clarity in technical explanations.\n\n"

                "## Quality Control\n"
                "- Do not guess missing information; ask if necessary.\n"
                "- Avoid generic or template-like responses.\n"
                "- Ensure output is practical, precise, and immediately usable.\n\n"

                "## Output Standard\n"
                "Every response must be:\n"
                "- Clear\n"
                "- Concise\n"
                "- Structured\n"
                "- Context-aware\n"
                "- Publication-ready\n"
            )
        },
        *messages
    ],
    "stream": True,
    "temperature": 0.2,
}

        in_think_block = False
        full_buffer = ""

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream("POST", self.base_url, json=payload, headers=headers) as response:
                    if response.status_code != 200:
                        yield f"data: ⚠️ API error (status {response.status_code})\n\n"
                        return

                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        
                        data_str = line[len("data: "):].strip()
                        if data_str == "[DONE]":
                            break
                            
                        try:
                            data = json.loads(data_str)
                            choices = data.get("choices", [])
                            if not choices:
                                continue
                            
                            token = choices[0].get("delta", {}).get("content", "")
                            if not token:
                                continue

                            full_buffer += token

                            # Simple on-the-fly filtering
                            if "<think>" in full_buffer and not in_think_block:
                                parts = full_buffer.split("<think>", 1)
                                if parts[0]:
                                    yield f"data: {json.dumps(parts[0])}\n\n"
                                full_buffer = "" 
                                in_think_block = True
                            
                            elif "</think>" in full_buffer and in_think_block:
                                parts = full_buffer.split("</think>", 1)
                                full_buffer = parts[1] if len(parts) > 1 else ""
                                in_think_block = False
                            
                            elif not in_think_block:
                                if "<" in full_buffer:
                                    tag_start = full_buffer.find("<")
                                    if "<think>".startswith(full_buffer[tag_start:]):
                                        if tag_start > 0:
                                            yield f"data: {json.dumps(full_buffer[:tag_start])}\n\n"
                                            full_buffer = full_buffer[tag_start:]
                                    else:
                                        yield f"data: {json.dumps(full_buffer)}\n\n"
                                        full_buffer = ""
                                else:
                                    yield f"data: {json.dumps(full_buffer)}\n\n"
                                    full_buffer = ""

                        except (json.JSONDecodeError, IndexError, KeyError):
                            continue

            except Exception as e:
                yield f"data: ⚠️ Error: {str(e)}\n\n"
                return