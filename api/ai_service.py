"""
AI Response Generation Service
Uses Google Gemini API to generate conversational legal responses
with retrieved legal context as grounding.
"""

import os
import traceback

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from api.nlp_pipeline import get_pipeline

# System prompt for the legal AI assistant
LEGAL_SYSTEM_PROMPT = """You are "India's Legal Voice", an expert AI legal assistant specializing in Indian law. You assist users with questions about:
- Indian Constitution (Fundamental Rights, DPSPs, Amendments)
- Indian Penal Code (IPC) — criminal offences and punishments
- Code of Criminal Procedure (CrPC) — criminal procedures, FIR, bail
- Code of Civil Procedure (CPC) — civil suits and procedures
- Family Law — Hindu Marriage Act, divorce, maintenance, domestic violence
- Labor Law — minimum wages, EPF, ESI, workplace safety
- Consumer Protection — consumer rights, complaint procedures
- Cyber Law — IT Act, cyber crimes
- Right to Information (RTI)
- And other Indian legal topics

RULES:
1. Always provide accurate, well-cited legal information based on the provided context.
2. Mention specific article numbers, section numbers, and act names when relevant.
3. Explain legal concepts in simple, accessible language.
4. Provide practical guidance — steps the user can take.
5. Include important caveats: recommend consulting a qualified lawyer for specific cases.
6. Be conversational and empathetic — many people seeking legal information are in distress.
7. If the context doesn't contain relevant information, provide general guidance based on your legal knowledge.
8. When mentioning landmark cases, cite them properly (e.g., "Maneka Gandhi v. Union of India, 1978").
9. Structure your response with clear sections: Legal Reference, Explanation, Practical Guidance.
10. Keep responses concise but comprehensive — aim for 200-400 words.

IMPORTANT DISCLAIMER: Always remind users that your responses are for informational purposes only and do not constitute legal advice. They should consult a qualified lawyer for their specific situation."""


class AIService:
    """AI service for generating legal responses using Gemini."""

    def __init__(self):
        self.model = None
        self.pipeline = get_pipeline()
        self._initialize()

    def _initialize(self):
        """Initialize the Gemini AI model."""
        if not GEMINI_AVAILABLE:
            print("[WARN] google-generativeai not installed. Using fallback responses.")
            return

        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key or api_key == "your_gemini_api_key_here":
            print("[WARN] GEMINI_API_KEY not set. Using fallback responses.")
            return

        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=LEGAL_SYSTEM_PROMPT,
            )
            print("[OK] Gemini AI model initialized successfully.")
        except Exception as e:
            print(f"[WARN] Failed to initialize Gemini: {e}")
            self.model = None

    async def generate_response(self, query: str, language: str = "en") -> dict:
        """
        Generate a legal response for the user's query.

        Args:
            query: User's legal question (in English or translated to English)
            language: Target language code for the response

        Returns:
            Dict with 'response', 'sources', and 'status' keys.
        """
        # Step 1: Retrieve relevant legal context
        context = self.pipeline.get_context_for_query(query, top_k=3)
        search_results = self.pipeline.search(query, top_k=3)

        # Extract source references
        sources = []
        for result in search_results:
            entry = result["entry"]
            sources.append({
                "id": entry.get("id", ""),
                "title": entry.get("title", ""),
                "category": entry.get("category", ""),
                "score": result["score"],
            })

        # Step 2: Generate AI response
        if self.model:
            try:
                response_text = await self._generate_with_gemini(query, context)
                return {
                    "response": response_text,
                    "sources": sources,
                    "status": "ai_generated",
                }
            except Exception as e:
                print(f"Gemini generation failed: {e}")
                traceback.print_exc()

        # Step 3: Fallback to template-based response
        response_text = self._generate_fallback(query, search_results)
        return {
            "response": response_text,
            "sources": sources,
            "status": "fallback",
        }

    async def _generate_with_gemini(self, query: str, context: str) -> str:
        """Generate response using Gemini AI with legal context."""
        prompt = f"""User's Legal Question: {query}

Relevant Legal Context from Knowledge Base:
{context}

Please provide a helpful, accurate, and conversational response to the user's question based on the above legal context. Include specific legal references (article/section numbers) and practical guidance."""

        response = self.model.generate_content(prompt)
        return response.text

    def _generate_fallback(self, query: str, search_results: list) -> str:
        """Generate a template-based response when AI is unavailable."""
        if not search_results:
            return self._generic_fallback(query)

        best_match = search_results[0]["entry"]
        response_parts = []

        # Title and citation
        response_parts.append(f"📋 **Legal Reference: {best_match.get('title', '')}**\n")

        # Content
        content = best_match.get("content", "")
        if content:
            response_parts.append(f"{content}\n")

        # Explanation
        explanation = best_match.get("explanation", "")
        if explanation:
            response_parts.append(f"\n💡 **Explanation:**\n{explanation}\n")

        # Guidance
        guidance = best_match.get("guidance", [])
        if guidance:
            response_parts.append("\n📝 **Practical Guidance:**")
            for g in guidance:
                response_parts.append(f"• {g}")

        # Steps
        steps = best_match.get("steps", [])
        if steps:
            response_parts.append("\n📋 **Steps to Follow:**")
            for i, step in enumerate(steps, 1):
                response_parts.append(f"{i}. {step}")

        # Additional sources
        if len(search_results) > 1:
            response_parts.append("\n📚 **Related Topics:**")
            for result in search_results[1:]:
                entry = result["entry"]
                response_parts.append(f"• {entry.get('title', '')}")

        response_parts.append(
            "\n\n⚠️ *Disclaimer: This information is for general guidance only and does not constitute legal advice. Please consult a qualified lawyer for your specific situation.*"
        )

        return "\n".join(response_parts)

    def _generic_fallback(self, query: str) -> str:
        """Generate a generic response when no matching legal content is found."""
        return f"""I appreciate your question about "{query}". While I don't have specific information matching your query in my current knowledge base, here's some general guidance:

📌 **For Constitutional Matters:**
• Fundamental Rights are in Articles 12-35 of the Indian Constitution
• Directive Principles: Articles 36-51
• Fundamental Duties: Article 51A

📌 **For Criminal Matters:**
• File FIR at the nearest police station (Section 154 CrPC)
• Emergency: Call 100 (Police) or 112 (Universal Emergency)
• Cyber crimes: Report at cybercrime.gov.in or call 1930

📌 **For Civil Disputes:**
• Consult a civil lawyer for property, contract, or money disputes
• Consumer complaints: File at e-daakhil.nic.in
• RTI applications: rtionline.gov.in

📌 **For Family Matters:**
• Domestic violence helpline: 181
• Family courts handle marriage, divorce, and custody matters
• Maintenance can be claimed under Section 125 CrPC

📌 **Useful Helplines:**
• Women Helpline: 181
• Police: 100
• Legal Aid: nalsa.gov.in

⚠️ *This is general information only. Please consult a qualified lawyer for advice specific to your situation.*"""


# Singleton instance
_ai_service_instance = None


def get_ai_service() -> AIService:
    """Get or create the singleton AI service instance."""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance
