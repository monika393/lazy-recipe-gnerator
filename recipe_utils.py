#!/usr/bin/env python3
"""
Recipe Generation Utilities

Core utilities for ChefAI recipe generation system, including:
- OpenAI-powered recipe generation
- Ingredient detection and processing
- Common ingredient categorization

Author: ChefAI Team
Version: 1.0.0
License: MIT
"""

import torch
import cv2
from openai import OpenAI
import numpy as np
import re
import os
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
from grocery_detection_utils import GroceryObjectDetector
import logging

# Load environment variables from .env file
load_dotenv()

# Suppress excessive logging
logging.getLogger('ultralytics').setLevel(logging.WARNING)


def load_recipe_prompt() -> str:
    """
    Load the recipe generation prompt template from file.
    
    Reads the AI prompt template that provides structured instructions
    for recipe generation, including format requirements and constraints.
    
    Returns:
        str: The recipe prompt template with placeholders for ingredients and mood
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        IOError: If the file cannot be read
    """
    prompt_path = 'prompts/recipe_prompt.txt'
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Recipe prompt file not found at {prompt_path}")
        raise
    except IOError as e:
        logging.error(f"Error reading recipe prompt file: {e}")
        raise


def get_common_fridge_ingredients() -> Dict[str, List[str]]:
    """
    Return categorized list of common refrigerator and pantry ingredients.
    
    Provides a comprehensive list of ingredients organized by category
    to help users select items that may not be detected by AI vision.
    
    Returns:
        Dict[str, List[str]]: Dictionary mapping category names to ingredient lists
        
    Categories include:
        - Proteins: Meat, dairy, eggs, plant-based proteins
        - Vegetables: Fresh vegetables and aromatics
        - Fruits: Common fruits and citrus
        - Pantry: Grains, oils, and basic staples
        - Condiments: Sauces, spices, and flavor enhancers
    """
    return {
        "Proteins": [
            "eggs", "chicken", "beef", "fish", "tofu", 
            "cheese", "yogurt", "milk"
        ],
        "Vegetables": [
            "tomatoes", "onions", "carrots", "bell peppers", 
            "lettuce", "spinach", "broccoli", "potatoes"
        ],
        "Fruits": [
            "apples", "bananas", "oranges", "berries", 
            "lemons", "limes"
        ],
        "Pantry": [
            "bread", "rice", "pasta", "flour", "oil", 
            "salt", "pepper", "garlic"
        ],
        "Condiments": [
            "butter", "mayonnaise", "ketchup", "mustard", 
            "soy sauce", "hot sauce"
        ]
    }


def detect_objects_detectron2(image_path: str) -> List[str]:
    """
    Detect grocery items in uploaded image using AI vision.
    
    Uses OpenAI's vision capabilities through the GroceryObjectDetector
    to identify food items and suggest cooking ingredients.
    
    Args:
        image_path: Path to the uploaded image file
        
    Returns:
        List[str]: List of detected ingredient names suitable for cooking
        
    Raises:
        Exception: If detection fails, returns empty list with error logging
    """
    try:
        # Initialize grocery-specific detector with OpenAI vision
        detector = GroceryObjectDetector(
            model_source="openai_vision",
            confidence_threshold=0.4
        )
        
        # Detect grocery items using AI vision
        detections = detector.detect_grocery_items(image_path)
        
        # Extract ingredient suggestions from detections
        suggested_ingredients = detector.get_ingredient_suggestions(detections)
        
        # Log detection results
        print(f"🔍 Detected {len(detections)} objects, suggested {len(suggested_ingredients)} ingredients")
        
        return suggested_ingredients[:10]  # Limit to top 10 suggestions
        
    except Exception as e:
        print(f"Grocery detection error: {e}")
        print("⚠️ No fallback ingredients provided - relying on AI model only.")
        return []


def generate_recipes_from_prompt(ingredients: List[str], mood: str) -> str:
    """
    Generate personalized recipes using OpenAI based on ingredients and mood.
    
    Creates two different recipes using the provided ingredients, tailored
    to the user's cooking mood/preference. Uses cost-optimized model selection.
    
    Args:
        ingredients: List of available ingredients to use in recipes
        mood: User's cooking mood/preference (e.g., "Quick & Easy", "Comfort Food")
        
    Returns:
        str: Formatted string containing two personalized recipes with:
            - Recipe names
            - Ingredient lists
            - Step-by-step instructions
            - Cooking times
            
    Raises:
        Exception: If recipe generation fails, returns error message
    """
    try:
        # Create ingredient list string
        ingredient_list = ', '.join(ingredients)
        
        # Load and format the prompt template
        prompt_template = load_recipe_prompt()
        formatted_prompt = prompt_template.format(
            ingredients=ingredient_list, 
            mood=mood
        )
        
        print("🤖 Generating recipes using OpenAI...")
        print("=" * 80)
        print("📝 PROMPT:")
        print("=" * 80)
        print(formatted_prompt)
        print("=" * 80)
        
        # Initialize OpenAI client
        client = OpenAI()
        # Use cost-effective model for text-only recipe generation
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        print(f"🤖 Using model: {model_name}")
        
        # Generate recipes using OpenAI
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional chef who writes clear, concise, practical recipes."
                },
                {
                    "role": "user", 
                    "content": formatted_prompt
                },
            ],
            temperature=0.7,      # Balanced creativity and consistency
            max_tokens=800,       # Sufficient for two detailed recipes
            top_p=0.9,           # Focus on high-probability tokens
        )
        
        # Extract and clean the generated content
        result = (response.choices[0].message.content or "").strip()
        
        print("\n" + "=" * 80)
        print("🤖 RESPONSE:")
        print("=" * 80)
        print(result)
        print("=" * 80)
        
        return f"**Your AI-Generated Recipes:**\n\n{result}"
        
    except Exception as e:
        error_msg = f"Error generating recipes: {str(e)}"
        print(f"❌ {error_msg}")
        return f"**Error:** {error_msg}\n\nPlease try again or check your OpenAI API configuration."




