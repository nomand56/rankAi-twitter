#!/usr/bin/env python3
import os
import datetime
import feedparser
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from openai import OpenAI

# ─── Load & validate env ─────────────────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY     = os.getenv("OPENAI_API_KEY")
RSS_FEED_URL       = os.getenv("RSS_FEED_URL")
GMAIL_ADDRESS      = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TO_EMAIL           = os.getenv("TO_EMAIL")

for var in [
    "OPENAI_API_KEY",
    "RSS_FEED_URL",
    "GMAIL_ADDRESS",
    "GMAIL_APP_PASSWORD",
    "TO_EMAIL"
]:
    if not globals()[var]:
        raise RuntimeError(f"Missing env var: {var}")

# ─── 1. Fetch today’s top AI headline ──────────────────────────────────────────
feed = feedparser.parse(RSS_FEED_URL)
top_headline = feed.entries[0].title

# ─── 2. Build your OpenRouter prompts ────────────────────────────────────────
SYSTEM = """
Context for theRankAI:
The proliferation of Artificial Intelligence tools presents both immense opportunity and significant challenge. Users, from individuals to businesses, struggle to identify the most suitable AI solutions amidst a crowded and often opaque market characterized by complex features, confusing pricing models, and unreliable claims. This white paper introduces the AI Tool Navigator, a revolutionary platform designed to democratize access to AI by providing users with a single, highly relevant, and trustworthy tool recommendation based on simple natural language input. By leveraging advanced Natural Language Processing, a sophisticated ranking and recommendation engine, and a commitment to transparency, the AI Tool Navigator eliminates complexity and unexpected costs, empowering users to effortlessly find the right AI tool for their specific needs, completely free of charge.

1. The Challenge: The Paradox of Choice in the AI Tool Ecosystem

The rapid advancements in Artificial Intelligence have led to an explosion in the number and variety of AI tools available. These tools offer capabilities ranging from content generation and data analysis to image recognition and automation. However, this abundance has created a significant barrier for potential users:

Overwhelming Complexity: The sheer volume of tools makes it difficult to explore and understand the nuances of each offering. Users are often faced with extensive directories requiring technical knowledge to navigate effectively.
Difficulty in Matching Needs to Tools: Users know what they want to achieve ("generate social media posts," "transcribe an interview") but struggle to translate that need into the specific features and capabilities of available AI tools.
Opaque and Unexpected Costs: Many tools employ complex pricing models, often starting with free trials or limited free tiers that quickly lead to unexpected charges once the user is invested in the platform or exceeds hidden usage limits. This lack of transparency erodes trust.
Unverified Claims and Hype: The competitive nature of the AI market can lead to exaggerated marketing claims that do not align with a tool's actual performance or capabilities, resulting in user frustration and wasted effort.
Time Consumption: The process of researching, comparing, testing, and evaluating multiple tools to find the right fit is time-consuming and inefficient for individuals and organizations alike.
This complex landscape hinders the broader adoption of AI and prevents users from easily leveraging its transformative potential to solve their specific problems.

2. The Solution: The AI Tool Navigator

The AI Tool Navigator is conceived as the intuitive solution to the AI tool discovery problem. Our core philosophy is to make finding and using the right AI tool "way easier" by providing a direct and trustworthy path. We achieve this through a unique combination of user-centric design and intelligent backend systems, offered completely free to the end-user.

The central tenet of the AI Tool Navigator is its ability to understand a user's need expressed in natural language and instantly provide a single, highly relevant, and vetted AI tool recommendation. This eliminates the need for users to browse endless lists, understand technical jargon, or worry about hidden costs.

3. How it Works: A Seamless Blend of NLP and Intelligent Recommendation

The AI Tool Navigator's functionality is powered by a sophisticated architecture designed for both power and simplicity:

Natural Language Processing (NLP) Engine: At the forefront is a robust NLP engine capable of accurately interpreting diverse user queries expressed in everyday language. This engine identifies the user's core intent (the task), key objects (the type of content, data, etc.), and crucial constraints (e.g., budget, required integrations, desired output format, technical skill level).
Comprehensive and Vetted Tool Database: We maintain a meticulously curated database of AI tools. Each tool profile goes beyond basic information, including:
Detailed feature breakdown mapped to specific tasks.
Granular pricing model information (free tier limits, trial specifics, paid plan costs and inclusions, credit system details).
Required integrations and technical specifications.
Target user audience and ease of use assessment.
Aggregated user feedback and reports on performance and claim accuracy.
Internal verification notes regarding claimed capabilities.
Sophisticated Ranking and Recommendation Engine: This is the intelligence that drives the single recommendation. It utilizes a multi-factor ranking algorithm that considers:
Semantic Relevance: How well the tool's capabilities align with the user's parsed natural language query.
Constraint Matching: Filtering based on explicit user constraints (e.g., "free," "integrates with X").
Trustworthiness Score: A composite score based on transparent pricing information, positive user feedback regarding claim accuracy and performance, and internal vetting results. Tools with hidden costs or unverified claims are penalized or filtered out.
User Context (Optional & Privacy-Preserving): Anonymized data on past user interactions or saved preferences can subtly influence recommendations for returning users.
Trend Awareness: Integration of trend forecasting data (as described in theRankAI concept) can inform recommendations, highlighting relevant emerging tools where appropriate.
Ease of Use Scoring: Considering the tool's general reputation for user-friendliness, particularly relevant if the NLP infers a beginner user.
Single Recommendation Output: Based on the ranking, the system presents the single highest-scoring tool.
"Why This Tool?" Explanation: Crucially, the recommendation includes a concise explanation justifying the choice. This highlights the specific features that match the user's need, addresses any relevant constraints (especially regarding cost transparency), and provides confidence in the recommendation.
Continuous Validation and Feedback Loop: The system is designed to learn and improve. User interactions (e.g., clicking on the recommendation, providing feedback) and reports on misleading tools feed back into the ranking algorithm and tool database, ensuring recommendations become increasingly accurate and trustworthy over time.
4. Key Features Driving Ease of Use and Trust

The AI Tool Navigator is built around features that prioritize the user experience and build trust:

Effortless Natural Language Search: The core interface is a simple text bar where users type their need as they would ask a colleague.
Instant, Single Recommendation: No lists, no complex filters, just the most relevant tool presented immediately.
Absolute Free Access for Users: The platform is and will remain completely free for end-users, removing any financial barrier to discovery.
Transparent Cost Information: For every recommended tool, clear information about its pricing model, including free tier limitations and trial specifics, is presented upfront in an easy-to-understand format.
Claim Verification and Trust Scores: Our internal vetting process and integration of user feedback on performance help users avoid tools with exaggerated or false claims. Warnings or lower trust scores are applied to tools with reported issues.
Interactive Clarification: If a user's query is ambiguous, the system engages in a simple, conversational clarification step to ensure the recommendation is precise.
Concise Tool Summaries: Information about the recommended tool is presented in a brief, digestible format, focusing on how it directly addresses the user's specific need.
Easy Reporting Mechanism: Users can easily flag tools with misleading information or hidden costs, contributing to the platform's data accuracy and trustworthiness.
5. Addressing the Pain Points Directly

The AI Tool Navigator is purpose-built to tackle the core problems in the AI tool market:

Solving Overwhelm: By providing a single recommendation, we eliminate the need for users to sift through hundreds or thousands of options.
Bridging the Gap Between Need and Tool: The natural language interface removes the technical translation layer, allowing users to express their problem directly.
Eliminating Hidden Costs: Our commitment to transparent pricing disclosure and vetting process ensures users are informed about potential costs before they invest time in a tool.
Combating False Claims: The vetting process and reliance on user feedback help to highlight or filter out tools that do not perform as advertised, saving users frustration.
Saving Time: The instant, relevant recommendation drastically reduces the time spent on tool discovery and evaluation.
6. The Underlying Strength: Leveraging theRankAI Foundation

The AI Tool Navigator builds upon the foundational strengths envisioned in theRankAI concept, including:

Intelligent Ranking and Recommendation: The core engine benefits from the principles of sophisticated ranking algorithms to ensure the "best" tool is truly identified based on multiple factors.
Trend Forecasting: Integrating insights into emerging AI tool trends allows the Navigator to recommend cutting-edge solutions where relevant to user needs.
Budget Customization: While the Navigator emphasizes free tools, the underlying capability to understand and filter by budget remains a powerful component for more complex or enterprise-level needs, ensuring recommendations align with financial constraints.
Validation by User Success: The feedback loops and tracking of recommendation effectiveness are critical for the continuous improvement and accuracy of the recommendation engine.
7. Future Vision

As the AI landscape evolves, so too will the AI Tool Navigator. Future enhancements could include:

Expansion of the tool database to include an even wider range of specialized AI tools.
More nuanced understanding of complex multi-step user workflows.
Integration with user workflows via browser extensions or APIs (while maintaining the free and easy core).
Development of aggregated insights into AI tool performance and user satisfaction based on platform data (anonymized and aggregated).
8. Conclusion

The AI Tool Navigator represents a significant step forward in making Artificial Intelligence accessible and usable for everyone. By prioritizing an effortless user experience, eliminating costs for the user, and building a foundation of transparency and trust, we aim to become the go-to platform for anyone seeking to leverage the power of AI to solve their problems. In a world of increasing AI complexity, the AI Tool Navigator offers a simple, reliable, and free path to finding the right tool, empowering users to unlock the full potential of artificial intelligence.
- theRankAI is a free dashboard that ranks, reviews, and one‑click‑launches 4,000+ AI tools.







You are an elite SaaS growth copywriter who has helped >100 startups reach 50k followers
in under a year. You understand persuasion, virality loops, platform algorithms,
and tone calibration for technical but approachable brands.
"""
USER = f"""
You are a helpful AI assistant tasked with generating social media content for a *personal* account. The goal is to share something the account holder (USER) is genuinely excited about and involved with: theRankAI, a free dashboard that ranks, reviews, and one-click-launches 4,000+ AI tools.

Leverage the core messages and themes from the previous brand content (struggle finding AI, ease of use, freeness, trust/vetting, productivity focus, one-click launch), but translate them into an authentic, personal, and conversational voice suitable for sharing with friends, colleagues, and connections.

Focus on:
- Expressing personal excitement about theRankAI.
- Briefly explaining *why* the USER believes in this product or was involved in its development (e.g., they personally experienced the problem of finding AI tools).
- Highlighting the key benefits (easy to find, free, one-click launch, great for productivity) from a personal perspective ("I love how easy it is," "It's been a game-changer for me," "We made it free because...").
- Encouraging others to check it out in a low-pressure, genuine way.

Avoid:
- Formal marketing language ("revolutionary," "industry-leading," etc.) unless used ironically.
- Highly structured multi-tweet threads that feel like a campaign.
- Overly aggressive calls to action.

Context:
- Date: {datetime.datetime.utcnow():%Y-%m-%d}
- Weekly theme: “Productivity AI”
- Product angle: “One‑click launch of any AI tool”

Deliver:
1.  **Twitter posts:** 2-3 individual tweets (not a thread) that share personal excitement and key benefits, suitable for a personal feed. Keep them concise.
2.  **LinkedIn update:** A personal update (approx. 150-300 words) sharing the excitement, the personal "why," and highlighting the value for professional connections, particularly regarding productivity. Include a question to encourage engagement.

Inject personality and make it sound like a genuine share from an individual, not a company announcement. Ensure a link to theRankAI is included naturally.


Context for seperate newletter content:
- Date: {datetime.datetime.utcnow():%Y-%m-%d}
- Top AI news: {top_headline}
- Weekly theme: “Productivity AI”
- Product angle: “One‑click launch of any AI tool”
# 


"""

# ─── 3. Call OpenRouter (GPT‑4.1‑nano) ────────────────────────────────────────
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENAI_API_KEY)
resp = client.chat.completions.create(
    model="openai/gpt-4.1-nano",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": USER}
    ]
)
content_pack = resp.choices[0].message.content

# ─── 4. Send mail via Gmail SMTP ──────────────────────────────────────────────
today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
msg = MIMEText(content_pack)
msg["Subject"] = f"theRankAI Daily Content Pack — {today_str}"
msg["From"]    = GMAIL_ADDRESS
msg["To"]      = TO_EMAIL

print("GMAIL_ADDRESS     =", GMAIL_ADDRESS)
print("GMAIL_APP_PASSWORD=", GMAIL_APP_PASSWORD)
with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    smtp.send_message(msg)

print("✅ Content pack generated and emailed via Gmail SMTP.")
