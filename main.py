import streamlit as st
import pandas as pd
import numpy as np
import re
import json
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure Gemini API
def configure_gemini():
    """
    Configure the Gemini API with your API key
    """
    # You'll need to get an API key from Google AI Studio
    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        st.sidebar.warning("Please add your Gemini API key to secrets.toml")
        api_key = st.sidebar.text_input("Or enter your Gemini API key here:", type="password")
        if not api_key:
            st.stop()

    # Configure the Gemini API
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def analyze_with_gemini(model, case_details, user_evidence, user_strategy):
    """
    Use Gemini API to analyze the case, evidence, and strategy
    """
    # Prepare the prompt for Gemini
    prompt = f"""
    You are a legal expert AI specialized in analyzing legal cases and predicting outcomes.
    Please analyze the following case details, evidence, and legal strategy to predict the outcome 
    and provide strategic recommendations.

    ## Case Details:
    {case_details}

    ## Evidence Items:
    {json.dumps(user_evidence, indent=2)}

    ## Legal Strategy:
    {user_strategy}

    Provide a detailed analysis including:
    1. Win probability percentage (between 0 and 100)
    2. Outcome analysis with key positive and negative factors
    3. Evidence analysis with strengths, weaknesses, and improvement suggestions
    4. Strategy analysis with strengths, gaps, and effectiveness
    5. Comparable case analysis (if applicable)
    6. Judicial considerations
    7. Strategic recommendations ordered by priority

    Format your response as a JSON object with the following structure:
    {{
        "win_probability": {{
            "win_probability": float,
            "base_case_probability": float,
            "evidence_contribution": float,
            "strategy_contribution": float
        }},
        "outcome_analysis": {{
            "outcome_category": string,
            "outcome_description": string,
            "key_positive_factors": [string],
            "key_negative_factors": [string],
            "judicial_considerations": [string]
        }},
        "evidence_analysis": {{
            "evidence_items": [
                {{
                    "description": string,
                    "type": string,
                    "strength_score": float,
                    "category": string,
                    "improvement_suggestions": [string]
                }}
            ],
            "overall_score": float,
            "overall_category": string,
            "portfolio_gaps": [string],
            "portfolio_strengths": [string]
        }},
        "strategy_analysis": {{
            "primary_strategy": string,
            "secondary_strategy": string,
            "strategy_scores": object,
            "strategy_balance": string,
            "strategy_gaps": [string],
            "strategy_effectiveness": string
        }},
        "similar_cases": [
            {{
                "title": string,
                "similarity": float,
                "outcome": string,
                "key_factors": [string],
                "evidence_strength": string,
                "strategy_used": string
            }}
        ],
        "recommendations": [
            {{
                "category": string,
                "priority": string,
                "recommendation": string,
                "rationale": string
            }}
        ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        # Extract the JSON part from the response
        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        json_str = response.text[json_start:json_end]

        # Parse the JSON response
        result = json.loads(json_str)
        return result
    except Exception as e:
        st.error(f"Error in Gemini API: {str(e)}")
        # Fallback to the original analysis function if Gemini API fails
        return analyze_user_evidence_and_strategy(case_details, user_evidence, user_strategy)

def extract_case_facts(case_details):
    """
    Extract key facts from case details
    """
    # For dict input, extract the facts field
    if isinstance(case_details, dict):
        case_text = case_details.get("facts", "")
    else:
        case_text = str(case_details)
        
    # Simple implementation - in a real system, this could use NLP to extract entities and facts
    facts = []
    
    # Split by sentences and extract potential facts
    sentences = re.split(r'[.!?]', case_text)
    for sentence in sentences:
        if len(sentence.strip()) > 10:  # Ignore very short sentences
            facts.append(sentence.strip())
    
    return facts

def find_similar_cases(case_facts):
    """
    Find similar cases from a database using TF-IDF and cosine similarity
    """
    # In a real implementation, this would query a database of cases
    # For demo purposes, we'll return mock similar cases
    
    # Mock database of cases
    mock_cases = [
        {
            "title": "Smith v. Johnson (2020)",
            "facts": "Plaintiff alleged breach of contract when defendant failed to deliver goods on time.",
            "outcome": "Favorable settlement",
            "evidence_strength": "Strong documentary evidence",
            "strategy_used": "Focus on contract terms and damages",
            "key_factors": ["Clear contract terms", "Documented timeline", "Quantifiable damages"]
        },
        {
            "title": "Williams v. City Council (2019)",
            "facts": "Challenge to municipal ordinance on constitutional grounds.",
            "outcome": "Partially successful",
            "evidence_strength": "Mixed precedent support",
            "strategy_used": "Constitutional rights approach",
            "key_factors": ["Procedural due process", "Similar precedent cases", "Expert testimony"]
        },
        {
            "title": "Estate of Roberts v. Medical Center (2021)",
            "facts": "Medical malpractice claim related to surgical complications.",
            "outcome": "Loss at trial",
            "evidence_strength": "Contradictory expert testimony",
            "strategy_used": "Technical medical arguments",
            "key_factors": ["Conflicting expert opinions", "Pre-existing conditions", "Informed consent documentation"]
        },
        {
            "title": "Thompson v. Insurance Co. (2022)",
            "facts": "Denial of coverage claim based on policy exclusion.",
            "outcome": "Win through summary judgment",
            "evidence_strength": "Clear policy documentation",
            "strategy_used": "Strict policy interpretation",
            "key_factors": ["Policy language clarity", "Industry standards", "Documented communications"]
        },
        {
            "title": "Garcia Family Trust v. Developer (2021)",
            "facts": "Property dispute over easement rights and boundary lines.",
            "outcome": "Settlement after discovery",
            "evidence_strength": "Historical survey evidence",
            "strategy_used": "Historical documentation approach",
            "key_factors": ["Survey records", "Witness testimony", "Pattern of use"]
        }
    ]
    
    # For demo purposes, assign random similarity scores
    similar_cases = []
    for case in mock_cases:
        # In a real implementation, we would calculate actual similarity scores
        similarity = np.random.uniform(0.3, 0.9)
        similar_case = case.copy()
        similar_case["similarity"] = similarity
        similar_cases.append(similar_case)
    
    # Sort by similarity
    similar_cases.sort(key=lambda x: x["similarity"], reverse=True)
    return similar_cases

def assess_evidence_strength(user_evidence):
    """
    Assess the strength of evidence items provided by the user.
    """
    # Process each evidence item
    evidence_items = []
    overall_score = 0
    
    for item in user_evidence:
        # Calculate a strength score based on reliability and relevance
        strength_score = (item["reliability"] + item["relevance"]) * 10  # Scale to 0-100
        
        # Determine evidence type
        evidence_type = categorize_evidence_type(item["description"])
        
        # Categorize strength
        category = categorize_evidence_strength(strength_score)
        
        # Generate improvement suggestions
        suggestions = suggest_evidence_improvements(item, evidence_type, strength_score)
        
        # Add to the evidence items list
        evidence_items.append({
            "description": item["description"],
            "type": evidence_type,
            "strength_score": strength_score,
            "category": category,
            "improvement_suggestions": suggestions
        })
        
        # Add to overall score
        overall_score += strength_score
    
    # Calculate average
    if user_evidence:
        overall_score = overall_score / len(user_evidence)
    else:
        overall_score = 0
    
    # Categorize overall strength
    overall_category = categorize_evidence_strength(overall_score)
    
    # Identify portfolio gaps and strengths
    portfolio_gaps = identify_evidence_gaps(evidence_items)
    portfolio_strengths = identify_evidence_strengths(evidence_items)
    
    return {
        "evidence_items": evidence_items,
        "overall_score": overall_score,
        "overall_category": overall_category,
        "portfolio_gaps": portfolio_gaps,
        "portfolio_strengths": portfolio_strengths
    }

def categorize_evidence_type(description):
    """
    Determine the type of evidence based on its description
    """
    description = description.lower()
    
    # Check for document types
    if any(word in description for word in ["contract", "agreement", "document", "letter", "email", "record", "report", "file"]):
        return "documentary"
    
    # Check for testimony types
    elif any(word in description for word in ["witness", "testimony", "statement", "deposition", "interview"]):
        return "testimonial"
    
    # Check for physical evidence
    elif any(word in description for word in ["physical", "exhibit", "photograph", "video", "recording", "object"]):
        return "physical"
    
    # Check for expert evidence
    elif any(word in description for word in ["expert", "opinion", "analysis", "report", "evaluation"]):
        return "expert"
    
    # Default to "other"
    return "other"

def categorize_evidence_strength(score):
    """
    Categorize evidence strength based on score
    """
    if score >= 80:
        return "Very Strong"
    elif score >= 70:
        return "Strong"
    elif score >= 60:
        return "Moderate"
    elif score >= 50:
        return "Acceptable"
    else:
        return "Weak"

def suggest_evidence_improvements(item, evidence_type, strength_score):
    """
    Suggest improvements for evidence based on its type and strength score
    """
    suggestions = []
    
    # General suggestions based on strength
    if strength_score < 50:
        suggestions.append("Consider if this evidence is worth presenting or needs significant strengthening")
    
    # Type-specific suggestions
    if evidence_type == "documentary":
        if item["reliability"] < 4:
            suggestions.append("Verify document authenticity and chain of custody")
        if item["relevance"] < 4:
            suggestions.append("Clarify direct connection between this document and case issues")
            
    elif evidence_type == "testimonial":
        if item["reliability"] < 4:
            suggestions.append("Prepare witness thoroughly and anticipate credibility challenges")
        if item["relevance"] < 4:
            suggestions.append("Focus testimony on directly relevant facts")
            
    elif evidence_type == "physical":
        if item["reliability"] < 4:
            suggestions.append("Ensure proper authentication and chain of custody documentation")
        
    elif evidence_type == "expert":
        if item["reliability"] < 4:
            suggestions.append("Reinforce expert's qualifications and methodology")
        if item["relevance"] < 4:
            suggestions.append("Connect expert opinion more directly to case facts")
    
    # Add general suggestion if none specific
    if not suggestions:
        suggestions.append("Continue to integrate this evidence effectively with your overall strategy")
        
    return suggestions

def identify_evidence_gaps(evidence_items):
    """
    Identify gaps in the evidence portfolio
    """
    gaps = []
    
    # Check evidence type distribution
    evidence_types = [item["type"] for item in evidence_items]
    
    # Check for missing evidence types
    if "documentary" not in evidence_types:
        gaps.append("No documentary evidence present - consider adding documentation to strengthen case")
    
    if "testimonial" not in evidence_types:
        gaps.append("No witness testimony included - consider adding witness statements to support facts")
    
    if "expert" not in evidence_types:
        gaps.append("No expert evidence provided - consider if expert opinion would strengthen your position")
    
    # Check for weak areas
    weak_items = [item for item in evidence_items if item["strength_score"] < 60]
    if len(weak_items) > len(evidence_items) / 2:
        gaps.append("More than half of evidence items are rated weak or acceptable - strengthen key elements")
    
    # Add general gap analysis if no specific gaps
    if not gaps and len(evidence_items) < 3:
        gaps.append("Limited overall evidence portfolio - consider adding more supporting evidence")
    
    return gaps

def identify_evidence_strengths(evidence_items):
    """
    Identify strengths in the evidence portfolio
    """
    strengths = []
    
    # Check for strong evidence
    strong_items = [item for item in evidence_items if item["strength_score"] >= 70]
    if strong_items:
        strengths.append(f"Portfolio includes {len(strong_items)} strong evidence items")
    
    # Check for diverse evidence types
    evidence_types = set(item["type"] for item in evidence_items)
    if len(evidence_types) >= 3:
        strengths.append("Diverse evidence types provide multiple angles of support")
    
    # Check for overall portfolio size
    if len(evidence_items) >= 5:
        strengths.append("Substantial evidence portfolio size adds cumulative weight")
    
    # Add general strength if none specific
    if not strengths:
        strengths.append("Consider building on existing evidence to create stronger portfolio")
    
    return strengths

def categorize_strategy(strategy_text):
    """
    Categorize and analyze the legal strategy based on text description
    """
    strategy_text = strategy_text.lower()
    
    # Identify primary strategy approach
    strategy_keywords = {
        "procedural": ["procedural", "process", "motion to dismiss", "summary judgment", "jurisdiction"],
        "substantive": ["substantive", "merits", "elements", "statutory", "precedent"],
        "settlement": ["settlement", "negotiation", "mediation", "resolution", "compromise"],
        "aggressive": ["aggressive", "challenge", "attack", "counter", "offensive"],
        "defensive": ["defensive", "mitigate", "limit", "reduce", "protect"]
    }
    
    # Count keyword matches for each strategy type
    strategy_scores = {}
    for strategy, keywords in strategy_keywords.items():
        score = sum(1 for keyword in keywords if keyword in strategy_text)
        strategy_scores[strategy] = score
    
    # Determine primary and secondary strategies
    sorted_strategies = sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True)
    primary_strategy = sorted_strategies[0][0] if sorted_strategies[0][1] > 0 else "undefined"
    secondary_strategy = sorted_strategies[1][0] if len(sorted_strategies) > 1 and sorted_strategies[1][1] > 0 else ""
    
    # Assess strategy balance
    strategy_balance = assess_strategy_balance(strategy_scores)
    
    # Identify strategy gaps
    strategy_gaps = identify_strategy_gaps(strategy_scores, strategy_text)
    
    # Assess strategy effectiveness based on the strategy scores
    max_score = max(strategy_scores.values()) if strategy_scores else 0
    if max_score >= 3:
        strategy_effectiveness = "Well-defined approach with clear direction"
    elif max_score >= 1:
        strategy_effectiveness = "Identifiable approach but could be more clearly articulated"
    else:
        strategy_effectiveness = "Strategy lacks clear direction or focus"
    
    return {
        "primary_strategy": primary_strategy,
        "secondary_strategy": secondary_strategy,
        "strategy_scores": strategy_scores,
        "strategy_balance": strategy_balance,
        "strategy_gaps": strategy_gaps,
        "strategy_effectiveness": strategy_effectiveness
    }

def assess_strategy_balance(strategy_scores):
    """
    Assess the balance of the strategy based on scores
    """
    total_score = sum(strategy_scores.values())
    if total_score == 0:
        return "Undefined strategy"
    
    # Check if one strategy dominates
    max_score = max(strategy_scores.values())
    if max_score / total_score > 0.7:
        return "Heavily weighted toward one approach"
    
    # Check if well-balanced
    top_two = sorted(strategy_scores.values(), reverse=True)[:2]
    if len(top_two) > 1 and top_two[0] > 0 and top_two[1] > 0:
        return "Balanced approach with complementary strategies"
    
    return "Moderately focused approach"

def identify_strategy_gaps(strategy_scores, strategy_text):
    """
    Identify gaps in the legal strategy
    """
    gaps = []
    
    # Check for minimal strategy scores
    if max(strategy_scores.values()) < 2:
        gaps.append("Strategy lacks clear definition - consider more explicit strategic planning")
    
    # Check for specific strategy elements
    if strategy_scores.get("procedural", 0) == 0:
        gaps.append("Consider adding procedural strategy elements")
    
    if strategy_scores.get("substantive", 0) == 0:
        gaps.append("Consider strengthening substantive legal arguments")
    
    if strategy_scores.get("settlement", 0) == 0 and "settlement" not in strategy_text:
        gaps.append("No settlement strategy defined - consider fallback positions")
    
    # Length-based assessment
    if len(strategy_text) < 100:
        gaps.append("Strategy description is brief - consider more detailed planning")
    
    # Add general gap if none found
    if not gaps:
        gaps.append("Consider contingency planning for unexpected developments")
        
    return gaps

def calculate_win_probability(similar_cases, evidence_strength, strategy_approach):
    """
    Calculate win probability based on similar cases, evidence strength and strategy approach
    """
    # Base case probability from similar cases
    if similar_cases:
        # Calculate base probability from similar cases
        win_outcomes = sum(1 for case in similar_cases[:3] if "win" in case["outcome"].lower() 
                          or "favorable" in case["outcome"].lower() 
                          or "success" in case["outcome"].lower())
        base_probability = (win_outcomes / min(3, len(similar_cases))) * 100
    else:
        base_probability = 50  # Default to 50% if no similar cases
    
    # Evidence contribution (-20 to +20 points)
    evidence_contribution = (evidence_strength["overall_score"] - 50) * 0.4
    
    # Strategy contribution (-15 to +15 points)
    strategy_scores = strategy_approach["strategy_scores"]
    max_strategy_score = max(strategy_scores.values()) if strategy_scores else 0
    strategy_effectiveness = 50 + (max_strategy_score * 10)
    strategy_contribution = (strategy_effectiveness - 50) * 0.3
    
    # Calculate final probability
    win_probability = base_probability + evidence_contribution + strategy_contribution
    
    # Ensure probability is between 0 and 100
    win_probability = max(0, min(100, win_probability))
    
    return {
        "win_probability": round(win_probability),
        "base_case_probability": round(base_probability),
        "evidence_contribution": round(evidence_contribution, 1),
        "strategy_contribution": round(strategy_contribution, 1)
    }

def generate_outcome_analysis(win_probability, similar_cases, evidence_strength, strategy_approach):
    """
    Generate a detailed analysis of the predicted outcome
    """
    probability = win_probability["win_probability"]
    
    # Determine outcome category
    if probability >= 80:
        outcome_category = "Highly Favorable"
        outcome_description = "Strong likelihood of a favorable outcome with clear advantages across multiple factors."
    elif probability >= 65:
        outcome_category = "Moderately Favorable"
        outcome_description = "Good prospects for a favorable outcome, though some areas of vulnerability exist."
    elif probability >= 45:
        outcome_category = "Balanced"
        outcome_description = "Case could go either way, with relatively equal strengths and weaknesses."
    elif probability >= 30:
        outcome_category = "Challenging"
        outcome_description = "Significant hurdles exist, though partial success may be possible with strategic improvements."
    else:
        outcome_category = "Highly Challenging"
        outcome_description = "Substantial barriers to success with the current approach and evidence."
    
    # Generate key positive factors
    positive_factors = []
    
    # Add evidence-based factors
    if evidence_strength["overall_score"] >= 70:
        positive_factors.append("Strong overall evidence portfolio")
    
    strong_items = [item for item in evidence_strength["evidence_items"] if item["strength_score"] >= 70]
    if strong_items:
        positive_factors.append(f"Presence of {len(strong_items)} strong evidence items")
    
    # Add strategy-based factors
    if strategy_approach["strategy_effectiveness"].startswith("Well-defined"):
        positive_factors.append("Clear strategic direction with focused approach")
    
    # Add similar case factors
    favorable_cases = [case for case in similar_cases[:3] 
                      if "win" in case["outcome"].lower() or "favorable" in case["outcome"].lower()]
    if favorable_cases:
        positive_factors.append(f"{len(favorable_cases)} similar cases with favorable outcomes")
    
    # Ensure at least one positive factor
    if not positive_factors:
        positive_factors.append("Case presents opportunity for targeted strategic improvements")
    
    # Generate key negative factors
    negative_factors = []
    
    # Add evidence-based factors
    if evidence_strength["overall_score"] < 60:
        negative_factors.append("Evidence portfolio lacks sufficient strength")
    
    weak_items = [item for item in evidence_strength["evidence_items"] if item["strength_score"] < 50]
    if weak_items:
        negative_factors.append(f"Presence of {len(weak_items)} weak evidence items")
    
    # Add strategy-based factors
    if strategy_approach["strategy_gaps"]:
        negative_factors.append(f"Strategy gaps in {strategy_approach['strategy_gaps'][0].split('-')[0]}")
    
    # Add similar case factors
    unfavorable_cases = [case for case in similar_cases[:3] 
                        if "loss" in case["outcome"].lower() or "unfavorable" in case["outcome"].lower()]
    if unfavorable_cases:
        negative_factors.append(f"{len(unfavorable_cases)} similar cases with unfavorable outcomes")
    
    # Ensure at least one negative factor
    if not negative_factors:
        negative_factors.append("Case requires sustained attention to maintain advantages")
    
    # Generate judicial considerations
    judicial_considerations = [
        "Judicial interpretation of key statutes may impact case outcome",
        "Court's disposition toward similar cases in this jurisdiction",
        "Potential for procedural versus substantive resolution",
        "Judicial calendar and time constraints may affect strategy timelines",
        "Court's historical approach to comparable evidence portfolios"
    ]
    
    return {
        "outcome_category": outcome_category,
        "outcome_description": outcome_description,
        "key_positive_factors": positive_factors,
        "key_negative_factors": negative_factors,
        "judicial_considerations": judicial_considerations
    }

def generate_strategic_recommendations(win_probability, similar_cases, evidence_strength, strategy_approach, user_evidence):
    """
    Generate strategic recommendations based on the analysis
    """
    recommendations = []
    
    # Evidence recommendations
    if evidence_strength["portfolio_gaps"]:
        for i, gap in enumerate(evidence_strength["portfolio_gaps"]):
            priority = "Critical" if i == 0 and win_probability["win_probability"] < 60 else "High"
            recommendations.append({
                "category": "Evidence",
                "priority": priority,
                "recommendation": f"Address evidence gap: {gap.split('-')[0]}",
                "rationale": f"Strengthening this area would directly improve case probability by addressing: {gap}"
            })
    
    # Check for weak evidence items that need improvement
    weak_items = [item for item in evidence_strength["evidence_items"] if item["strength_score"] < 60]
    if weak_items:
        recommendations.append({
            "category": "Evidence",
            "priority": "High" if win_probability["win_probability"] < 70 else "Moderate",
            "recommendation": f"Strengthen {len(weak_items)} weak evidence items",
            "rationale": "Vulnerabilities in these evidence items could be exploited by opposing counsel"
        })
    
    # Strategy recommendations
    if strategy_approach["strategy_gaps"]:
        for i, gap in enumerate(strategy_approach["strategy_gaps"]):
            priority = "Critical" if i == 0 and "lacks clear definition" in gap else "High"
            recommendations.append({
                "category": "Strategy",
                "priority": priority,
                "recommendation": f"Refine strategy: {gap.split('-')[0]}",
                "rationale": f"Strategic improvement would strengthen approach by addressing: {gap}"
            })
    
    # Case comparison recommendations
    if similar_cases:
        successful_case = next((case for case in similar_cases if "win" in case["outcome"].lower()), None)
        if successful_case:
            recommendations.append({
                "category": "Case Comparison",
                "priority": "Moderate",
                "recommendation": f"Align approach with successful case: {successful_case['title']}",
                "rationale": f"This similar case succeeded using {successful_case['strategy_used']}"
            })
    
    # Generic improvement recommendations
    if len(user_evidence) < 3:
        recommendations.append({
            "category": "Evidence",
            "priority": "High",
            "recommendation": "Expand evidence portfolio with additional supporting items",
            "rationale": "Current evidence base is limited; additional evidence would strengthen overall position"
        })
    
    if win_probability["win_probability"] < 50:
        recommendations.append({
            "category": "Settlement",
            "priority": "High",
            "recommendation": "Develop strong fallback settlement position",
            "rationale": "Given current win probability, a strategic settlement approach is advisable"
        })
    
    # Prepare for opposing arguments
    recommendations.append({
        "category": "Preparation",
        "priority": "Enhancement",
        "recommendation": "Anticipate and prepare counters to opposing arguments",
        "rationale": "Proactive preparation for opposing theories strengthens overall position"
    })
    
    return recommendations

def analyze_user_evidence_and_strategy(case_details, user_evidence, user_strategy):
    """
    Analyze user's evidence and legal strategy against the case details
    to predict potential outcomes.
    
    Parameters:
    case_details (dict): The user's case details
    user_evidence (list): List of evidence items provided by user
    user_strategy (str): User's current legal strategy
    
    Returns:
    dict: Prediction analysis results
    """
    # Extract key elements from user inputs
    evidence_strength = assess_evidence_strength(user_evidence)
    strategy_approach = categorize_strategy(user_strategy)
    case_facts = extract_case_facts(case_details)
    
    # Find similar cases using TF-IDF and cosine similarity
    similar_cases = find_similar_cases(case_facts)
    
    # Calculate predicted outcome probabilities
    win_probability = calculate_win_probability(
        similar_cases, 
        evidence_strength, 
        strategy_approach
    )
    
    # Generate detailed analysis
    outcome_analysis = generate_outcome_analysis(
        win_probability, 
        similar_cases, 
        evidence_strength, 
        strategy_approach
    )
    
    # Generate recommendations
    recommendations = generate_strategic_recommendations(
        win_probability,
        similar_cases,
        evidence_strength,
        strategy_approach,
        user_evidence
    )
    
    return {
        "win_probability": win_probability,
        "outcome_analysis": outcome_analysis,
        "evidence_analysis": evidence_strength,
        "strategy_analysis": strategy_approach,
        "similar_cases": similar_cases[:5],  # Top 5 similar cases
        "recommendations": recommendations
    }

# Main application function
def main():
    st.set_page_config(
        page_title="Legal Case Prediction Tool",
        page_icon="⚖️",
        layout="wide"
    )
    
    st.title("⚖️ Legal Case Prediction Analysis Tool")
    st.markdown("""
    This application helps legal professionals analyze cases and predict potential outcomes 
    by evaluating case details, evidence strength, and legal strategy.
    """)
    
    # Initialize session state for evidence items if not exists
    if 'evidence_items' not in st.session_state:
        st.session_state.evidence_items = []
        
    # Clear button in sidebar
    st.sidebar.title("Actions")
    if st.sidebar.button("Clear All Data"):
        st.session_state.evidence_items = []
        st.rerun()
    
    # Sidebar: Gemini toggle
    st.sidebar.title("Model Settings")
    use_gemini = st.sidebar.checkbox("Use Gemini AI", value=True, 
                                    help="Enable Gemini AI for enhanced predictions.")
    
    # Load Gemini model if selected
    model = None
    if use_gemini:
        try:
            model = configure_gemini()
            st.sidebar.success("✅ Gemini API configured successfully.")
        except Exception as e:
            st.sidebar.error(f"⚠️ Gemini configuration failed: {e}")
            use_gemini = False

    # Case Details
    with st.expander("📝 Case Details", expanded=True):
        case_title = st.text_input("Case Title / Description")
        case_type = st.selectbox("Case Type", 
                                ["Select a case type...", "Criminal", "Civil", "Constitutional", "Tax", "Family", "Corporate", "Labor"])
        case_details = st.text_area("Case Facts (Detailed)", height=150)

    # Evidence Section
    with st.expander("🧾 Evidence Portfolio", expanded=True):
        st.write("Add evidence items (existing or planned).")
        
        # Display current evidence
        if st.session_state.evidence_items:
            st.markdown("### Current Evidence:")
            for i, item in enumerate(st.session_state.evidence_items):
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.markdown(f"**{i+1}.** {item['description']}")
                with col2:
                    st.markdown(f"Reliability: {item['reliability']}/5")
                with col3:
                    st.markdown(f"Relevance: {item['relevance']}/5")
                    
                # Add delete button for each evidence item
                if st.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.evidence_items.pop(i)
                    st.rerun()
                st.markdown("---")

        # Form to add new evidence
        with st.form("evidence_form"):
            st.markdown("### Add New Evidence")
            new_evidence = st.text_area("Evidence Description", height=100, 
                                        placeholder="Describe the evidence item in detail...")
            col1, col2 = st.columns(2)
            with col1:
                reliability = st.slider("Reliability (1-5)", 1, 5, 3, 
                                      help="How reliable is this evidence? 1=Low, 5=High")
            with col2:
                relevance = st.slider("Relevance (1-5)", 1, 5, 3,
                                    help="How relevant is this evidence to your case? 1=Low, 5=High")
            
            # Submit button for evidence form
            evidence_submitted = st.form_submit_button("Add Evidence")
            
            if evidence_submitted and new_evidence:
                st.session_state.evidence_items.append({
                    "description": new_evidence,
                    "reliability": reliability,
                    "relevance": relevance
                })
                st.rerun()

    # Legal Strategy Section
    with st.expander("📊 Legal Strategy", expanded=True):
        strategy = st.text_area("Describe your current legal strategy", height=150,
                              placeholder="Detail your approach, including procedural strategy, substantive arguments, settlement considerations, etc.")

    # Analysis Button
    analyze_button = st.button("🔍 Analyze Case", type="primary", use_container_width=True)
    
    # Perform analysis when button is clicked
    if analyze_button:
        # Validate inputs
        if not case_details or not strategy or not st.session_state.evidence_items:
            st.error("Please complete all sections: Case Details, Evidence Portfolio, and Legal Strategy.")
        else:
            with st.spinner("Analyzing your case..."):
                # Prepare case data for analysis
                case_data = {
                    "title": case_title,
                    "type": case_type,
                    "facts": case_details
                }
                
                # Analyze using either Gemini or fallback function
                if use_gemini and model:
                    analysis_results = analyze_with_gemini(model, case_data, st.session_state.evidence_items, strategy)
                else:
                    analysis_results = analyze_user_evidence_and_strategy(case_data, st.session_state.evidence_items, strategy)
                
                # Display results
                st.success("Analysis Complete!")
                
                # Win Probability Section
                st.markdown("## 📈 Outcome Prediction")
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.metric("Win Probability", f"{analysis_results['win_probability']['win_probability']}%")
                    st.caption(f"{analysis_results['outcome_analysis']['outcome_category']}: {analysis_results['outcome_analysis']['outcome_description']}")
                    
                with col2:
                    st.metric("Base Case Probability", f"{analysis_results['win_probability']['base_case_probability']}%")
                    st.caption("From similar case outcomes")
                    
                with col3:
                    evidence_effect = analysis_results['win_probability']['evidence_contribution']
                    strategy_effect = analysis_results['win_probability']['strategy_contribution']
                    
                    if evidence_effect >= 0:
                        st.metric("Evidence Effect", f"+{evidence_effect}%")
                    else:
                        st.metric("Evidence Effect", f"{evidence_effect}%")
                        
                    if strategy_effect >= 0:
                        st.metric("Strategy Effect", f"+{strategy_effect}%")
                    else:
                        st.metric("Strategy Effect", f"{strategy_effect}%")
                
                # Key factors
                st.markdown("### Key Factors")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Positive Factors")
                    for factor in analysis_results['outcome_analysis']['key_positive_factors']:
                        st.markdown(f"✅ {factor}")
                        
                with col2:
                    st.markdown("#### Negative Factors")
                    for factor in analysis_results['outcome_analysis']['key_negative_factors']:
                        st.markdown(f"⚠️ {factor}")
                
                # Evidence Analysis
                st.markdown("## 🧾 Evidence Analysis")
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"Overall Portfolio Strength: **{analysis_results['evidence_analysis']['overall_category']}** ({analysis_results['evidence_analysis']['overall_score']:.1f}/100)")
                    
                with col2:
                    # Small pie chart of evidence types could go here in a real implementation
                    pass
                
                # Evidence table
                st.markdown("### Evidence Items")
                for item in analysis_results['evidence_analysis']['evidence_items']:
                    col1, col2, col3 = st.columns([3, 1, 2])
                    
                    with col1:
                        st.markdown(f"**{item['description'][:50]}{'...' if len(item['description']) > 50 else ''}**")
                        st.caption(f"Type: {item['type']}")
                        
                    with col2:
                        # Color based on strength
                        color = "green" if item['strength_score'] >= 70 else "orange" if item['strength_score'] >= 50 else "red"
                        st.markdown(f"<span style='color:{color};font-weight:bold;'>{item['category']}</span>", unsafe_allow_html=True)
                        st.caption(f"Score: {item['strength_score']:.1f}/100")
                        
                    with col3:
                        if item['improvement_suggestions']:
                            st.caption("Suggestion:")
                            st.markdown(f"✏️ {item['improvement_suggestions'][0]}")
                    
                    st.markdown("---")
                
                # Portfolio gaps and strengths
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Portfolio Gaps")
                    for gap in analysis_results['evidence_analysis']['portfolio_gaps']:
                        st.markdown(f"🔍 {gap}")
                        
                with col2:
                    st.markdown("#### Portfolio Strengths")
                    for strength in analysis_results['evidence_analysis']['portfolio_strengths']:
                        st.markdown(f"💪 {strength}")
                
                # Strategy Analysis
                st.markdown("## 📊 Strategy Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Primary Approach:** {analysis_results['strategy_analysis']['primary_strategy'].title()}")
                    if analysis_results['strategy_analysis']['secondary_strategy']:
                        st.markdown(f"**Secondary Approach:** {analysis_results['strategy_analysis']['secondary_strategy'].title()}")
                    st.markdown(f"**Balance:** {analysis_results['strategy_analysis']['strategy_balance']}")
                    
                with col2:
                    st.markdown("#### Strategy Effectiveness")
                    st.markdown(f"⚡ {analysis_results['strategy_analysis']['strategy_effectiveness']}")
                    
                    st.markdown("#### Strategy Gaps")
                    for gap in analysis_results['strategy_analysis']['strategy_gaps']:
                        st.markdown(f"⚠️ {gap}")
                
                # Similar Cases
                st.markdown("## 📚 Similar Cases")
                
                # Create tabs for each similar case
                if analysis_results['similar_cases']:
                    tabs = st.tabs([f"{case['title']}" for case in analysis_results['similar_cases'][:3]])
                    
                    for i, tab in enumerate(tabs):
                        case = analysis_results['similar_cases'][i]
                        with tab:
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown(f"**Outcome:** {case['outcome']}")
                                st.markdown(f"**Similarity:** {case['similarity']:.2f}/1.0")
                                
                            with col2:
                                st.markdown("**Key Factors:**")
                                for factor in case['key_factors']:
                                    st.markdown(f"• {factor}")
                                    
                            st.markdown(f"**Evidence Strength:** {case['evidence_strength']}")
                            st.markdown(f"**Strategy Used:** {case['strategy_used']}")
                
                # Strategic Recommendations
                st.markdown("## 📋 Strategic Recommendations")
                
                # Group recommendations by priority
                critical_recs = [r for r in analysis_results['recommendations'] if r['priority'] == 'Critical']
                high_recs = [r for r in analysis_results['recommendations'] if r['priority'] == 'High']
                other_recs = [r for r in analysis_results['recommendations'] if r['priority'] not in ['Critical', 'High']]
                
                # Display critical recommendations
                if critical_recs:
                    st.markdown("### 🚨 Critical Priority")
                    for rec in critical_recs:
                        st.markdown(f"**{rec['category']}: {rec['recommendation']}**")
                        st.markdown(f"_{rec['rationale']}_")
                        st.markdown("---")
                
                # Display high priority recommendations
                if high_recs:
                    st.markdown("### ⚠️ High Priority")
                    for rec in high_recs:
                        st.markdown(f"**{rec['category']}: {rec['recommendation']}**")
                        st.markdown(f"_{rec['rationale']}_")
                        st.markdown("---")
                
                # Display other recommendations
                if other_recs:
                    st.markdown("### 📝 Additional Recommendations")
                    for rec in other_recs:
                        st.markdown(f"**{rec['category']} ({rec['priority']}): {rec['recommendation']}**")
                        st.markdown(f"_{rec['rationale']}_")
                        st.markdown("---")
                
                # Judicial considerations
                st.markdown("### ⚖️ Judicial Considerations")
                for consideration in analysis_results['outcome_analysis']['judicial_considerations']:
                    st.markdown(f"• {consideration}")

# Run the app
if __name__ == "__main__":
    main()