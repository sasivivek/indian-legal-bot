"""
Bharat Legal AI — RAG (Retrieval-Augmented Generation) Pipeline
Orchestrates semantic retrieval from ChromaDB, prompt construction with legal guardrails, and Gemini response generation.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

from api.retriever import get_retriever, LegalRetriever, RetrievalResult
from api.ai_service import get_ai_service, AIService

load_dotenv()


# Strict legal system prompt for Gemini
RAG_SYSTEM_PROMPT = """You are Bharat Legal AI (भारत लीगल एआई), an authoritative yet accessible legal information assistant specializing in Indian Law and the Constitution of India.

CRITICAL INSTRUCTIONS & GUARDRAILS:
1. STRICTLY GROUNDED: Answer the question using ONLY the retrieved legal context provided below.
2. NO HALLUCINATION: Do NOT invent legal provisions, Act names, Article numbers, or Section numbers. If a provision is not in the context, do not make it up.
3. INSUFFICIENT CONTEXT: If the retrieved context does not contain enough information to answer the question reliably, explicitly state: "I could not find sufficient information in my legal knowledge base to answer this question reliably."
4. STRUCTURE & CLARITY: Explain legal principles in simple, clear language while preserving exact legal terms (e.g., "Cognizable offence", "Anticipatory bail", "Fundamental Rights").
5. ACTIONABLE GUIDANCE: Where applicable, summarize rights, key conditions, and practical steps clearly with bullet points.
6. CITATIONS: Reference the specific Act, Article, or Section mentioned in the context.
7. DISCLAIMER: Always remind the user that this is for informational purposes and not formal legal advice.

FORMAT YOUR ANSWER WITH:
- 📋 **Legal Summary / Provisions**: Direct explanation of the relevant law
- 💡 **Key Rights & Meaning**: What it means for the citizen
- 📝 **Practical Guidance / Steps**: Any procedural steps or helplines (if applicable)
- ⚠️ **Disclaimer**: Standard legal advisory notice
"""


@dataclass
class RAGResponse:
    """Structured response from the RAG pipeline."""
    response: str
    sources: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "rag_generated"  # 'rag_generated' | 'rag_fallback' | 'no_relevant_context'
    query_used: str = ""


class RAGPipeline:
    """
    End-to-end RAG orchestrator for Indian Legal Q&A.
    """

    _instance: Optional["RAGPipeline"] = None

    def __init__(
        self,
        retriever: Optional[LegalRetriever] = None,
        ai_service: Optional[AIService] = None,
    ):
        self.retriever = retriever or get_retriever()
        self.ai_service = ai_service or get_ai_service()

    @classmethod
    def get_instance(cls) -> "RAGPipeline":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def answer(self, query: str, top_k: Optional[int] = None) -> RAGResponse:
        """
        Full RAG pipeline execution:
        1. Query validation
        2. Semantic similarity search in ChromaDB via Retriever
        3. Threshold filtering & check
        4. Context formatting & Prompt assembly
        5. Grounded generation via Gemini (with fallback if API key not present)
        """
        if not query or not query.strip():
            return RAGResponse(
                response="Please provide a valid question about Indian law or the Constitution.",
                sources=[],
                status="invalid_query",
                query_used="",
            )

        clean_query = query.strip()

        # Step 1: Semantic Vector Retrieval from ChromaDB
        retrieved_results = self.retriever.retrieve(clean_query, top_k=top_k)

        # Step 2: Handle cases where no context meets the relevance threshold
        if not retrieved_results:
            return RAGResponse(
                response=(
                    "I could not find sufficient information in my legal knowledge base to answer this question reliably.\n\n"
                    "⚠️ *Please consult a qualified advocate or visit [NALSA](https://nalsa.gov.in) for specific legal assistance.*"
                ),
                sources=[],
                status="no_relevant_context",
                query_used=clean_query,
            )

        # Format sources metadata list
        sources_list = [res.to_source_dict() for res in retrieved_results]

        # Step 3: Format Context Block
        formatted_context = self.retriever.format_context_for_prompt(retrieved_results)

        # Step 4: Construct RAG Prompt for LLM
        prompt = self._build_rag_prompt(clean_query, formatted_context)

        # Step 5: Generate Answer via Gemini
        if self.ai_service.is_configured():
            try:
                llm_response = await self.ai_service.generate(prompt)
                return RAGResponse(
                    response=llm_response,
                    sources=sources_list,
                    status="rag_generated",
                    query_used=clean_query,
                )
            except Exception as e:
                print(f"[RAGPipeline] Gemini generation failed ({e}), falling back to structured RAG context...")

        # Step 6: Fallback to structured grounded response from retrieved chunks
        fallback_text = self._build_grounded_fallback(clean_query, retrieved_results)
        return RAGResponse(
            response=fallback_text,
            sources=sources_list,
            status="rag_fallback",
            query_used=clean_query,
        )

    def _build_rag_prompt(self, query: str, context: str) -> str:
        """Construct the prompt combining system instructions, retrieved context, and question."""
        return f"""{RAG_SYSTEM_PROMPT}

==================================================
RETRIEVED LEGAL CONTEXT (FROM VECTOR DATABASE):
==================================================
{context}
==================================================

USER QUESTION:
{query}

GROUNDED LEGAL ANSWER:"""

    def _build_grounded_fallback(
        self, query: str, results: List[RetrievalResult]
    ) -> str:
        """
        Generate a structured, deterministic answer directly from the top retrieved chunks
        when Gemini AI API is unavailable.
        """
        primary = results[0]

        lines = [
            f"## 📋 Legal Information: {primary.title}",
            "",
            f"**Category:** {primary.category.title()}",
        ]

        if primary.act:
            lines.append(f"**Governing Act:** {primary.act}")
        if primary.article:
            lines.append(f"**Constitutional Provision:** Article {primary.article}")
        if primary.section:
            lines.append(f"**Statutory Section:** Section {primary.section}")

        lines.extend([
            "",
            "### 📖 Legal Context & Meaning",
            primary.text.strip(),
            "",
        ])

        if len(results) > 1:
            lines.append("### 📚 Related Legal Provisions Found")
            for other in results[1:]:
                lines.append(f"- **{other.title}** ({other.category.title()})")
            lines.append("")

        lines.extend([
            "---",
            "⚠️ **Legal Disclaimer:** *This information is retrieved directly from our Indian legal knowledge base for educational purposes only and does not constitute formal legal advice. Please consult a licensed advocate for your specific case.*",
        ])

        return "\n".join(lines)


# Helper factory function
def get_rag_pipeline() -> RAGPipeline:
    return RAGPipeline.get_instance()
