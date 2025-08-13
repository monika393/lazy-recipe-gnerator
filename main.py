#!/usr/bin/env python3
"""
ChefAI - Smart Recipe Generator

A Streamlit web application that uses AI to analyze fridge photos and generate
personalized recipes based on available ingredients and cooking preferences.

Author: ChefAI Team
Version: 1.0.0
License: MIT
"""

import streamlit as st
import os
from typing import List, Dict, Any, Optional

# Import custom modules
from recipe_utils import detect_objects_detectron2, generate_recipes_from_prompt, get_common_fridge_ingredients

# Configure page settings
st.set_page_config(
    page_title="ChefAI - Smart Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide default Streamlit styling */
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    #stDecoration {display: none;}
    header[data-testid="stHeader"] {display: none;}
    
    /* Global styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding: 2rem 1rem 0rem 1rem;
        max-width: 1200px;
    }
    
    /* Modern header with gradient */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 3rem;
        color: white;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="25" r="1" fill="white" opacity="0.05"/><circle cx="50" cy="50" r="1" fill="white" opacity="0.08"/><circle cx="25" cy="75" r="1" fill="white" opacity="0.03"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-header * {
        position: relative;
        z-index: 1;
    }
    
    .logo {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
        font-weight: 400;
    }
    
    /* Modern card design */
    .section-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .section-card:hover {
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .section-card h2 {
        font-size: 1.75rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Step indicators */
    .step-indicator {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.75rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Image upload area */
    .upload-area {
        border: 2px dashed #d1d5db;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        background: #f9fafb;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #3b82f6;
        background: #eff6ff;
    }
    
    /* Selected ingredients display */
    .selected-ingredients {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(30, 41, 59, 0.2);
    }
    
    .selected-ingredients h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .selected-ingredients .ingredient-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .ingredient-tag {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f8fafc;
        padding: 0.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #64748b;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #1e293b;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Recipe generation section */
    .recipe-section {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 24px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 12px 48px rgba(15, 23, 42, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .recipe-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23dots)"/></svg>');
        pointer-events: none;
    }
    
    .recipe-section * {
        position: relative;
        z-index: 1;
    }
    
    .recipe-section h2 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .recipe-section p {
        font-size: 1.1rem;
        margin: 0;
        opacity: 0.9;
    }
    
    /* Recipe output styling */
    .recipe-output {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.04);
    }
    
    .recipe-output h2 {
        color: #1e293b;
        margin-bottom: 2rem;
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Individual recipe cards */
    .recipe-1, .recipe-2 {
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .recipe-1:hover, .recipe-2:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
    }
    
    .recipe-1 {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #0ea5e9;
        border-left: 4px solid #0ea5e9;
    }
    
    .recipe-1 h3, .recipe-1 h4, .recipe-1 strong {
        color: #0c4a6e;
    }
    
    .recipe-2 {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
        border: 1px solid #22c55e;
        border-left: 4px solid #22c55e;
    }
    
    .recipe-2 h3, .recipe-2 h4, .recipe-2 strong {
        color: #14532d;
    }
    
    /* Modern buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        min-width: 140px;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Main generate button */
    .main-generate-btn .stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 1.25rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        min-width: 220px;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(5, 150, 105, 0.3);
    }
    
    .main-generate-btn .stButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        box-shadow: 0 12px 40px rgba(5, 150, 105, 0.4);
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .stat-card h3 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-card p {
        font-size: 0.9rem;
        margin: 0;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Form styling */
    .stMultiSelect > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Status messages */
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        border: 1px solid #10b981;
        border-radius: 12px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        border: 1px solid #3b82f6;
        border-radius: 12px;
    }
    
    /* Recipe content formatting */
    .recipe-content {
        line-height: 1.7;
        font-size: 1rem;
        color: #374151;
    }
    
    .recipe-content h3 {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #1f2937;
    }
    
    .recipe-content h4 {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        color: #374151;
    }
    
    .recipe-content ul, .recipe-content ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .recipe-content li {
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        padding: 3rem 0;
        margin-top: 4rem;
        border-top: 1px solid #e2e8f0;
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 24px;
        margin: 2rem 0;
        border: 2px dashed #cbd5e0;
    }
    
    .empty-state h3 {
        font-size: 1.5rem;
        color: #64748b;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .empty-state p {
        color: #94a3b8;
        font-size: 1rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1.5rem;
        }
        
        .logo {
            font-size: 2.5rem;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .section-card {
            padding: 1.5rem;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)


def process_image(image_file) -> List[str]:
    """
    Process uploaded image and detect grocery ingredients using AI vision.
    
    This function saves the uploaded image temporarily and uses OpenAI's vision
    capabilities to identify grocery items and suggest cooking ingredients.
    
    Args:
        image_file: Streamlit uploaded file object containing the image
        
    Returns:
        List[str]: List of detected ingredient names
        
    Raises:
        Exception: If image processing fails, returns empty list
    """
    try:
        # Ensure uploads directory exists
        os.makedirs('uploads', exist_ok=True)
        
        # Save uploaded file temporarily
        image_path = os.path.join('uploads', image_file.name)
        with open(image_path, 'wb') as f:
            f.write(image_file.getbuffer())
        
        # Process image with AI vision
        detected_objects = detect_objects_detectron2(image_path)
        return detected_objects
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return []


def render_categorized_ingredients(common_ingredients: Dict[str, List[str]], key_prefix: str) -> List[str]:
    """
    Render ingredient selection interface organized by categories.
    
    Creates a tabbed interface where users can select ingredients from
    different categories like proteins, vegetables, etc.
    
    Args:
        common_ingredients: Dictionary mapping category names to ingredient lists
        key_prefix: Unique prefix for Streamlit widget keys to avoid conflicts
        
    Returns:
        List[str]: Combined list of selected ingredients from all categories
    """
    selected_ingredients = []
    
    # Create tabs for better organization
    tabs = st.tabs(list(common_ingredients.keys()))
    
    for i, (category, items) in enumerate(common_ingredients.items()):
        with tabs[i]:
            selected = st.multiselect(
                f"Select {category.lower()}:",
                items,
                key=f"{key_prefix}_{category}",
                help=f"Choose multiple {category.lower()} items"
            )
            selected_ingredients.extend(selected)
    
    return selected_ingredients


def format_recipe_content(recipe_text: str) -> str:
    """
    Format AI-generated recipe content with proper HTML structure and styling.
    
    Converts plain text recipe content into properly formatted HTML with
    different styling for Recipe 1 and Recipe 2, including structured
    ingredients lists and numbered instructions.
    
    Args:
        recipe_text: Raw recipe text from AI generation
        
    Returns:
        str: HTML-formatted recipe content with proper structure and styling
    """
    if not recipe_text:
        return recipe_text
    
    # Clean up the text and split into lines
    lines = recipe_text.replace('**Your AI-Generated Recipes:**', '').strip().split('\n')
    formatted_lines = []
    current_recipe = None
    in_ingredients = False
    in_instructions = False
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append('<br>')
            continue
            
        line_lower = line.lower()
        
        # Detect recipe headers
        if 'recipe 1' in line_lower:
            if current_recipe:
                formatted_lines.append('</div>')
            formatted_lines.append('<div class="recipe-1">')
            current_recipe = 1
            formatted_lines.append(f'<h3>{line}</h3>')
            in_ingredients = False
            in_instructions = False
            
        elif 'recipe 2' in line_lower:
            if current_recipe:
                formatted_lines.append('</div>')
            formatted_lines.append('<div class="recipe-2">')
            current_recipe = 2
            formatted_lines.append(f'<h3>{line}</h3>')
            in_ingredients = False
            in_instructions = False
            
        # Detect sections
        elif line_lower.startswith('name:'):
            formatted_lines.append(f'<h4>{line}</h4>')
            
        elif line_lower.startswith('ingredients:'):
            formatted_lines.append(f'<h4>{line}</h4>')
            formatted_lines.append('<ul>')
            in_ingredients = True
            in_instructions = False
            
        elif line_lower.startswith('instructions:'):
            if in_ingredients:
                formatted_lines.append('</ul>')
                in_ingredients = False
            formatted_lines.append(f'<h4>{line}</h4>')
            formatted_lines.append('<ol>')
            in_instructions = True
            
        elif line_lower.startswith('total time:'):
            if in_ingredients:
                formatted_lines.append('</ul>')
                in_ingredients = False
            if in_instructions:
                formatted_lines.append('</ol>')
                in_instructions = False
            formatted_lines.append(f'<h4>{line}</h4>')
            
        # Handle list items
        elif line.startswith('- ') and in_ingredients:
            formatted_lines.append(f'<li>{line[2:]}</li>')
            
        elif line and line[0].isdigit() and '.' in line and in_instructions:
            # Remove the number and period for cleaner list
            content = line.split('.', 1)[1].strip() if '.' in line else line
            formatted_lines.append(f'<li>{content}</li>')
            
        else:
            # Regular paragraph text
            if line:
                formatted_lines.append(f'<p>{line}</p>')
    
    # Close any open lists and recipe divs
    if in_ingredients:
        formatted_lines.append('</ul>')
    if in_instructions:
        formatted_lines.append('</ol>')
    if current_recipe:
        formatted_lines.append('</div>')
    
    return '\n'.join(formatted_lines)


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.
    
    Sets up persistent state variables to maintain user selections
    and processing status across page interactions.
    """
    if 'final_ingredients' not in st.session_state:
        st.session_state.final_ingredients = []
    if 'suggested_ingredients' not in st.session_state:
        st.session_state.suggested_ingredients = []
    if 'image_processed' not in st.session_state:
        st.session_state.image_processed = False


def render_header() -> None:
    """
    Render the main application header with branding.
    
    Displays the ChefAI logo, title, and tagline in a modern gradient design.
    """
    st.markdown("""
    <div class="main-header">
        <div class="logo">👨‍🍳</div>
        <h1>ChefAI</h1>
        <p>Transform your ingredients into culinary masterpieces with AI</p>
    </div>
    """, unsafe_allow_html=True)


def render_image_upload_section() -> Optional[Any]:
    """
    Render the image upload section and handle image processing.
    
    Allows users to upload fridge/pantry photos and processes them
    using AI vision to detect ingredients.
    
    Returns:
        Optional[Any]: Uploaded image file object or None
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2><span class="step-indicator">1</span>📸 Upload Your Fridge Photo</h2>', unsafe_allow_html=True)
    
    uploaded_image = st.file_uploader(
        "Drop your fridge or pantry photo here",
        type=['jpg', 'png', 'jpeg'],
        help="Upload a clear photo for AI ingredient detection"
    )
    
    if uploaded_image is not None:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.image(uploaded_image, caption="Your Kitchen Photo", use_container_width=True)
        
        with col2:
            # Process image only when needed
            if not st.session_state.image_processed or st.button("🔄 Re-analyze Photo", type="secondary"):
                with st.spinner("🤖 AI is analyzing your ingredients..."):
                    st.session_state.suggested_ingredients = process_image(uploaded_image)
                    st.session_state.image_processed = True
            
            # Display detection results
            if st.session_state.suggested_ingredients:
                st.success(f"✨ Detected {len(st.session_state.suggested_ingredients)} ingredients!")
                with st.expander("View detected ingredients", expanded=True):
                    for ingredient in st.session_state.suggested_ingredients:
                        st.write(f"• {ingredient}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_image


def render_ingredient_selection_section() -> tuple[List[str], List[str], List[str]]:
    """
    Render the ingredient selection interface.
    
    Provides three methods for ingredient selection:
    1. AI-detected ingredients from uploaded photo
    2. Common ingredients organized by category
    3. Custom ingredients via text input
    
    Returns:
        tuple[List[str], List[str], List[str]]: Three lists containing:
            - AI-selected ingredients
            - Common ingredients selected
            - Custom ingredients entered
    """
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2><span class="step-indicator">2</span>🥘 Select Your Ingredients</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🤖 AI Detected", "🏪 Common Items", "✏️ Custom List"])
    
    selected_ai = []
    selected_common = []
    custom_list = []
    
    # AI-detected ingredients tab
    with tab1:
        if st.session_state.suggested_ingredients:
            selected_ai = st.multiselect(
                "AI detected these ingredients in your photo:",
                st.session_state.suggested_ingredients,
                key="ai_ingredients",
                help="Select the ingredients you want to use"
            )
        else:
            st.info("🔍 Upload a photo above to see AI-detected ingredients here!")
    
    # Common ingredients tab
    with tab2:
        common_ingredients = get_common_fridge_ingredients()
        selected_common = render_categorized_ingredients(common_ingredients, "common")
    
    # Custom ingredients tab
    with tab3:
        custom_ingredients = st.text_area(
            "Add your own ingredients (comma-separated):",
            placeholder="olive oil, garlic, herbs, leftover chicken, rice...",
            height=120,
            key="custom_ingredients"
        )
        
        if custom_ingredients:
            custom_list = [item.strip() for item in custom_ingredients.split(',') if item.strip()]
    
    st.markdown('</div>', unsafe_allow_html=True)
    return selected_ai, selected_common, custom_list


def render_selected_ingredients_display(final_ingredients: List[str]) -> None:
    """
    Display selected ingredients in a visually appealing format.
    
    Shows all selected ingredients as styled tags with a count,
    providing visual feedback to users about their selections.
    
    Args:
        final_ingredients: List of all selected ingredient names
    """
    if not final_ingredients:
        return
        
    # Create ingredient tags
    ingredient_tags = ''.join([
        f'<span class="ingredient-tag">{ing}</span>' 
        for ing in final_ingredients
    ])
    
    st.markdown(f"""
    <div class="selected-ingredients">
        <h3>🎯 Your Selected Ingredients ({len(final_ingredients)})</h3>
        <div class="ingredient-list">
            {ingredient_tags}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stats_cards(final_ingredients: List[str], suggested_ingredients: List[str], 
                      selected_common: List[str], custom_list: List[str]) -> None:
    """
    Render statistics cards showing ingredient counts.
    
    Displays three cards showing total ingredients, AI-detected count,
    and manually added count for user awareness.
    
    Args:
        final_ingredients: All selected ingredients
        suggested_ingredients: AI-detected ingredients
        selected_common: Common ingredients selected
        custom_list: Custom ingredients entered
    """
    col1, col2, col3 = st.columns(3)
    
    # Calculate counts
    ai_selected = len([ing for ing in final_ingredients if ing in suggested_ingredients])
    manual_selected = len(selected_common) + len(custom_list)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{len(final_ingredients)}</h3>
            <p>Total Ingredients</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{ai_selected}</h3>
            <p>AI Detected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{manual_selected}</h3>
            <p>Manually Added</p>
        </div>
        """, unsafe_allow_html=True)


def render_recipe_generation_section(final_ingredients: List[str]) -> bool:
    """
    Render the recipe generation interface and handle recipe creation.
    
    Provides mood selection and recipe generation functionality,
    displaying results when recipes are generated.
    
    Args:
        final_ingredients: List of selected ingredients for recipe generation
        
    Returns:
        bool: True if recipe generation was triggered, False otherwise
    """
    # Recipe generation header
    st.markdown("""
    <div class="recipe-section">
        <h2><span class="step-indicator">3</span>🎯 Generate Your Recipes</h2>
        <p>Choose your cooking style and let AI create personalized recipes just for you!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recipe generation controls
    col1, col2 = st.columns([3, 2])
    
    with col1:
        mood_options = [
            "🚀 Quick & Easy (5-15 minutes)",
            "🏠 Comfort Food Classics",
            "🥗 Healthy & Nutritious", 
            "🍖 Hearty & Filling",
            "🌟 Creative & Gourmet",
            "👨‍👩‍👧‍👦 Family-Friendly"
        ]
        
        mood = st.selectbox(
            "What's your cooking mood today?",
            mood_options,
            help="This will influence the style and complexity of your recipes"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        st.markdown('<div class="main-generate-btn">', unsafe_allow_html=True)
        generate_button = st.button(
            "✨ Create My Recipes",
            help="Generate personalized recipes using your selected ingredients"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle recipe generation
    if generate_button:
        st.markdown('<div class="recipe-output">', unsafe_allow_html=True)
        
        with st.spinner("👨‍🍳 Crafting your personalized recipes..."):
            recipes = generate_recipes_from_prompt(final_ingredients, mood)
        
        st.markdown("## 📜 Your Personalized Recipe Collection")
        formatted_recipes = format_recipe_content(recipes)
        st.markdown(f'<div class="recipe-content">{formatted_recipes}</div>', unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 New Recipes", type="secondary"):
                with st.spinner("Creating fresh recipes..."):
                    new_recipes = generate_recipes_from_prompt(final_ingredients, mood)
                st.rerun()
        
        with col2:
            st.button("📱 Share", type="secondary", help="Share your recipes (coming soon!)")
        
        with col3:
            st.button("💾 Save", type="secondary", help="Save to your recipe collection (coming soon!)")
            
        with col4:
            st.button("🛒 Shopping List", type="secondary", help="Generate shopping list (coming soon!)")
        
        st.success("🎉 Bon appétit! Your personalized recipes are ready to cook!")
        st.markdown('</div>', unsafe_allow_html=True)
        return True
    
    return False


def render_empty_state() -> None:
    """
    Render empty state when no ingredients are selected.
    
    Displays a helpful message encouraging users to select ingredients
    or upload a photo to get started.
    """
    st.markdown("""
    <div class="empty-state">
        <h3>👆 Ready to get cooking?</h3>
        <p>Upload a photo or select ingredients above to discover amazing recipes tailored just for you!</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer() -> None:
    """
    Render the application footer with branding and credits.
    
    Displays professional footer with project information and attribution.
    """
    st.markdown("""
    <div class="footer">
        <p><strong>ChefAI</strong> • Powered by OpenAI & Streamlit • Made with ❤️ for food lovers</p>
    </div>
    """, unsafe_allow_html=True)


def main() -> None:
    """
    Main application entry point.
    
    Orchestrates the entire ChefAI application flow:
    1. Initialize session state
    2. Render header and navigation
    3. Handle image upload and processing
    4. Manage ingredient selection
    5. Generate and display recipes
    6. Provide user feedback and actions
    """
    # Initialize application state
    initialize_session_state()
    
    # Render main header
    render_header()
    
    # Step 1: Image Upload
    uploaded_image = render_image_upload_section()
    
    # Step 2: Ingredient Selection
    selected_ai, selected_common, custom_list = render_ingredient_selection_section()
    
    # Combine all selected ingredients
    st.session_state.final_ingredients = list(set(selected_ai + selected_common + custom_list))
    
    # Display selected ingredients and stats
    if st.session_state.final_ingredients:
        render_selected_ingredients_display(st.session_state.final_ingredients)
        render_stats_cards(
            st.session_state.final_ingredients, 
            st.session_state.suggested_ingredients,
            selected_common, 
            custom_list
        )
        
        # Step 3: Recipe Generation
        render_recipe_generation_section(st.session_state.final_ingredients)
    else:
        # Show empty state
        render_empty_state()
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()