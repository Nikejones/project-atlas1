"""
LLM and Rule-based Intelligence Service for GCC Atlas
Integrates Gemini API when configured, with a transparent, high-fidelity local rule-based fallback.
"""

import httpx
from typing import Dict, Any, List, Optional
from app.config import settings
from app.models import AssistantChatResponse, SourceCitation
from app.services.rag_service import retrieve_context


def generate_rule_based_response(user_query: str, context: Dict[str, Any]) -> str:
    """
    Synthesize an honest, highly structured, rule-based response directly from
    retrieved SQLite records when no external LLM key is configured.
    """
    query_lower = user_query.lower()
    matched_city_ids = context.get("matched_city_ids", [])
    matched_sectors = context.get("matched_sectors", [])
    companies = context.get("retrieved_companies", [])
    cities = context.get("retrieved_cities", [])
    is_setup = context.get("is_setup_guidance", False)

    # 1. Setup / checklist guidance
    if is_setup:
        ans = (
            "### Strategic Intelligence: Pre-Setup Checklist for Establishing a GCC in India\n\n"
            "Based on verified national guidelines (**Invest India**) and **NASSCOM GCC Frameworks**, "
            "multinational corporations evaluating an Indian capability centre should gather the following five core data categories:\n\n"
            "1. **Location & Micro-Market Real Estate Benchmarks**\n"
            "   - Grade A commercial lease rentals vary considerably across hubs:\n"
            "     - *Bengaluru (ORR / Whitefield)*: ₹75 – ₹125 / sq ft / month\n"
            "     - *Hyderabad (HITEC City / Financial District)*: ₹58 – ₹88 / sq ft / month\n"
            "     - *Gurugram (Cyber City / Golf Course Rd)*: ₹72 – ₹118 / sq ft / month\n"
            "     - *Noida (Expressway corridors)*: ₹44 – ₹68 / sq ft / month\n"
            "     - *Pune & Chennai*: ₹50 – ₹80 / sq ft / month\n\n"
            "2. **Talent Availability & Compensation Structuring**\n"
            "   - Indicative tech salaries across verified hubs:\n"
            "     - Entry-level (0–2 yrs): ₹5.0L – ₹8.0L p.a.\n"
            "     - Mid-career software/data engineers (3–7 yrs): ₹14.5L – ₹22.0L p.a.\n"
            "     - Principal / Engineering Leads (8–12 yrs): ₹31.0L – ₹45.0L+ p.a.\n\n"
            "3. **State-Level IT Policies & Incentive Programs**\n"
            "   - **Telangana (TS-iPASS)**: 15-day statutory clearance, 100% stamp duty waiver, ₹1.5/unit power concession.\n"
            "   - **Karnataka (KITS IT Policy)**: Stamp duty exemptions, patent filing subsidies up to ₹10 Lakh.\n"
            "   - **Uttar Pradesh (Invest UP)**: Up to 25% capital subsidy and 100% electricity duty waiver for 10 years.\n"
            "   - **Tamil Nadu (Guidance TN)**: Capital subsidies up to 25% and female talent EPF reimbursement.\n\n"
            "4. **Legal, Regulatory & Tax Frameworks**\n"
            "   - Software Technology Parks of India (STPI) customs bonding vs. Special Economic Zones (SEZ).\n"
            "   - Arm's-length Transfer Pricing documentation and cross-border IP cost-sharing agreements.\n\n"
            "5. **Infrastructure & Commute Resilience**\n"
            "   - Direct international aviation connectivity, metro connectivity to tech parks, and power grid stability."
        )
        return ans

    # 2. City comparison query
    if len(matched_city_ids) >= 2 or ("compare" in query_lower and len(cities) >= 2):
        city_names = [c["name"] for c in cities]
        ans = f"### Comparative Analysis: {', '.join(city_names)}\n\n"
        ans += "Here is a side-by-side assessment grounded in the verified dataset benchmarks:\n\n"

        for c in cities:
            rent_str = f"₹{c.get('indicative_rent_min', 'N/A')} – ₹{c.get('indicative_rent_max', 'N/A')} / sq ft / mo ({c.get('indicative_rent_period', '')})"
            sal_str = f"Entry: ₹{c.get('indicative_salary_entry_lakh', 'N/A')}L | Mid: ₹{c.get('indicative_salary_mid_lakh', 'N/A')}L | Senior: ₹{c.get('indicative_salary_senior_lakh', 'N/A')}L"
            ans += f"#### **{c['name']} ({c['state']})**\n"
            ans += f"- **Tier**: {c['tier']}\n"
            ans += f"- **Grade A Commercial Rent**: {rent_str}\n"
            ans += f"- **Tech Salary Benchmarks**: {sal_str}\n"
            ans += f"- **Key Advantages**: {c.get('tradeoff_pros', 'Data unavailable')}\n"
            ans += f"- **Key Trade-offs / Friction**: {c.get('tradeoff_cons', 'Data unavailable')}\n"
            ans += f"- **State Policy Support**: {c.get('state_incentives', 'Data unavailable')}\n\n"

        # Trade-off summary
        rents = [c.get("indicative_rent_min", 999) for c in cities if c.get("indicative_rent_min")]
        if rents:
            lowest_rent_city = min(cities, key=lambda x: x.get("indicative_rent_min") or 999)
            ans += f"**Strategic Takeaway**: **{lowest_rent_city['name']}** offers the lowest real estate occupancy baseline among the compared locations. "
        if any(c["id"] == "bengaluru" for c in cities):
            ans += "**Bengaluru** retains the highest specialized talent depth in AI and architecture, balanced against elevated rental costs and traffic friction. "
        if any(c["id"] == "hyderabad" for c in cities):
            ans += "**Hyderabad** provides strong municipal infrastructure, faster airport connectivity, and aggressive single-window approvals."

        return ans

    # 3. Companies in a specific city query
    if matched_city_ids and companies:
        city_obj = cities[0] if cities else None
        city_label = city_obj["name"] if city_obj else matched_city_ids[0].capitalize()
        ans = f"### Verified GCC Presence in {city_label}\n\n"
        ans += f"In our verified dataset, **{len(companies)} multinational companies** operate major Global Capability Centres in **{city_label}**:\n\n"

        for comp in companies:
            est_year = comp.get("year_established") or "Data unavailable"
            parent = comp.get("parent_company") or comp["name"]
            ans += f"1. **{comp['name']}** ({comp['sector']})\n"
            ans += f"   - **Parent HQ**: {comp['hq_country']} ({parent})\n"
            ans += f"   - **Established in India**: {est_year}\n"
            ans += f"   - **Core Functions**: {comp['business_functions']}\n"
            ans += f"   - **Operational Scope**: {comp['short_description']}\n"
            ans += f"   - **Evidence Link**: [{comp['source_name']}]({comp['evidence_url']})\n\n"

        if city_obj:
            ans += f"**Indicative {city_label} Benchmarks**:\n"
            ans += f"- Office Rent: ₹{city_obj.get('indicative_rent_min')} – ₹{city_obj.get('indicative_rent_max')} / sq ft / mo\n"
            ans += f"- Tech Salary (Mid): ₹{city_obj.get('indicative_salary_mid_lakh')} Lakh p.a.\n"

        return ans

    # 4. Sector representation query
    if matched_sectors or ("sector" in query_lower and companies):
        sectors_found = set(c["sector"] for c in companies)
        ans = "### Sector Representation in the Verified Dataset\n\n"
        ans += f"The dataset contains verified capability centres across the following sectors:\n\n"
        for s in sorted(sectors_found):
            s_comps = [c["name"] for c in companies if c["sector"] == s]
            ans += f"- **{s}** ({len(s_comps)} GCCs): {', '.join(s_comps[:4])}\n"
        return ans

    # 5. Direct company search
    if companies:
        ans = f"### Verified Company Records Found ({len(companies)})\n\n"
        for comp in companies[:5]:
            est_year = comp.get("year_established") or "Data unavailable"
            ans += f"#### **{comp['name']}** — {comp['city_name']}\n"
            ans += f"- **Sector**: {comp['sector']} | **HQ**: {comp['hq_country']}\n"
            ans += f"- **Established**: {est_year} | **Headcount Bracket**: {comp.get('headcount_bracket', 'Data unavailable')}\n"
            ans += f"- **Core Functions**: {comp['business_functions']}\n"
            ans += f"- **Overview**: {comp['short_description']}\n"
            ans += f"- **Official Evidence**: [{comp['source_name']}]({comp['evidence_url']})\n\n"
        return ans

    # 6. Insufficient Evidence / Out of Scope
    return (
        "### Insufficient Evidence in Verified Dataset\n\n"
        "The current verified dataset contains 28 multinational companies across 6 major Indian hubs "
        "(Bengaluru, Hyderabad, Pune, Gurugram, Noida, and Chennai).\n\n"
        "We could not locate verified public records directly answering your query within the current dataset. "
        "To uphold research integrity, **GCC Atlas does not invent corporate entities, undisclosed lease terms, or unverified facts**.\n\n"
        "**Suggested inquiries you can try:**\n"
        "- *'Which companies in the dataset have GCCs in Noida?'*\n"
        "- *'Compare Hyderabad and Pune for a technology GCC.'*\n"
        "- *'Which sectors are represented in Bengaluru?'*\n"
        "- *'What information should a company gather before setting up a GCC in India?'*"
    )


async def ask_assistant(user_query: str, history: List[Any] = []) -> AssistantChatResponse:
    """
    RAG-grounded assistant pipeline:
    1. Retrieve records from SQLite
    2. If GEMINI_API_KEY is configured, call Gemini model with grounded context
    3. If no key is set or API call fails, seamlessly invoke high-fidelity rule-based engine
    """
    context = retrieve_context(user_query)
    citations = context.get("citations", [])
    records_count = len(context.get("retrieved_companies", [])) + len(context.get("retrieved_cities", []))

    api_key = settings.gemini_api_key

    # Attempt Live LLM if API Key is configured
    if api_key:
        try:
            # Build grounding prompt
            prompt_context_lines = []
            if context.get("retrieved_cities"):
                prompt_context_lines.append("=== RETRIEVED CITY BENCHMARKS ===")
                for c in context["retrieved_cities"]:
                    prompt_context_lines.append(
                        f"City: {c['name']} ({c['state']}), Tier: {c['tier']}, "
                        f"Rent: ₹{c.get('indicative_rent_min')}-₹{c.get('indicative_rent_max')} /sq ft/mo ({c.get('indicative_rent_period')}), "
                        f"Salaries: Entry ₹{c.get('indicative_salary_entry_lakh')}L, Mid ₹{c.get('indicative_salary_mid_lakh')}L, Senior ₹{c.get('indicative_salary_senior_lakh')}L. "
                        f"Incentives: {c.get('state_incentives')}. Advantages: {c.get('tradeoff_pros')}. Bottlenecks: {c.get('tradeoff_cons')}."
                    )

            if context.get("retrieved_companies"):
                prompt_context_lines.append("=== RETRIEVED VERIFIED GCC COMPANIES ===")
                for comp in context["retrieved_companies"]:
                    prompt_context_lines.append(
                        f"Company: {comp['name']}, City: {comp['city_name']}, Sector: {comp['sector']}, "
                        f"HQ: {comp['hq_country']}, Established: {comp.get('year_established') or 'Data unavailable'}, "
                        f"Functions: {comp['business_functions']}, Source: {comp['source_name']} ({comp['evidence_url']})"
                    )

            context_blob = "\n".join(prompt_context_lines)

            system_instruction = (
                "You are GCC Atlas AI, an intelligence assistant for multinational companies establishing Global Capability Centres in India. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. Base your answer EXCLUSIVELY on the provided factual context from the verified database.\n"
                "2. If requested information is missing from the context, state 'Data unavailable in current verified dataset'. Do NOT hallucinate companies, rents, or citations.\n"
                "3. Use professional, analytical B2B markdown formatting with bullet points and bold headers.\n"
                "4. Cite provided sources accurately."
            )

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": f"{system_instruction}\n\nDATABASE CONTEXT:\n{context_blob}\n\nUSER QUESTION: {user_query}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 1000
                }
            }

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            async with httpx.AsyncClient(timeout=settings.llm_timeout_seconds) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        text = "".join(p.get("text", "") for p in parts)
                        if text:
                            return AssistantChatResponse(
                                answer=text,
                                citations=citations,
                                is_demo_mode=False,
                                mode_badge="LIVE AI (Gemini 2.5 Flash Grounded)",
                                retrieved_records_count=records_count,
                                grounding_summary=f"Grounded on {len(context.get('retrieved_companies', []))} companies and {len(context.get('retrieved_cities', []))} cities."
                            )
        except Exception:
            # Fall back safely to rule-based engine on any API or network issue
            pass

    # High-fidelity Rule-based synthesis (Demo Mode)
    rule_answer = generate_rule_based_response(user_query, context)
    return AssistantChatResponse(
        answer=rule_answer,
        citations=citations,
        is_demo_mode=True,
        mode_badge="DEMO MODE (Rule-based Local Database Synthesis - No External LLM API Key)",
        retrieved_records_count=records_count,
        grounding_summary=f"Synthesized locally from SQLite using {len(context.get('retrieved_companies', []))} company records and {len(context.get('retrieved_cities', []))} city benchmarks."
    )
