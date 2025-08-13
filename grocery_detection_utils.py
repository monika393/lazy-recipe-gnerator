#!/usr/bin/env python3
"""
Grocery Detection Utilities

Advanced computer vision utilities for detecting grocery items in images
using OpenAI's Vision API. Provides ingredient suggestions based on detected items.

Author: ChefAI Team
Version: 1.0.0
License: MIT
"""

import base64
import io
import json
import os
import cv2
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Grocery item categories for ingredient mapping
GROCERY_CLASSES = [
    'apple', 'banana', 'orange', 'carrot', 'broccoli', 'lettuce', 'tomato', 
    'potato', 'onion', 'bell_pepper', 'cucumber', 'spinach', 'garlic', 'ginger',
    'lemon', 'lime', 'avocado', 'strawberry', 'blueberry', 'grapes', 'pineapple',
    'watermelon', 'cantaloupe', 'peach', 'pear', 'plum', 'cherry', 'kiwi',
    'bread', 'milk', 'eggs', 'cheese', 'yogurt', 'butter', 'chicken', 'beef',
    'fish', 'shrimp', 'salmon', 'tuna', 'ham', 'bacon', 'sausage', 'tofu',
    'rice', 'pasta', 'cereal', 'oats', 'flour', 'sugar', 'salt', 'pepper',
    'oil', 'vinegar', 'soy_sauce', 'ketchup', 'mustard', 'mayonnaise',
    'water', 'juice', 'soda', 'beer', 'wine', 'coffee', 'tea',
    'soup', 'sauce', 'spices', 'herbs', 'nuts', 'beans', 'lentils'
]


class GroceryObjectDetector:
    """
    Advanced grocery item detection using OpenAI Vision API.
    
    Provides comprehensive ingredient detection and suggestion capabilities
    for recipe generation applications.
    """
    
    def __init__(self, model_source: str = "openai_vision", confidence_threshold: float = 0.4):
        """
        Initialize the grocery object detector.
        
        Args:
            model_source: Detection model to use ("openai_vision" supported)
            confidence_threshold: Minimum confidence for detections (0.0-1.0)
            
        Raises:
            ValueError: If unsupported model_source is provided
            Exception: If OpenAI client initialization fails
        """
        self.model_source = model_source
        self.confidence_threshold = confidence_threshold
        
        if model_source == "openai_vision":
            try:
                self.client = OpenAI()
                # Use GPT-4o specifically for vision tasks (required for image analysis)
                self.model_name = "gpt-4o"
                logger.info(f"Initialized OpenAI Vision detector with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                raise
        else:
            raise ValueError(f"Unsupported model source: {model_source}")
    
    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 string for OpenAI Vision API.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            str: Base64 encoded image string
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            IOError: If image cannot be read or encoded
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                logger.debug(f"Successfully encoded image: {image_path}")
                return encoded_string
        except FileNotFoundError:
            logger.error(f"Image file not found: {image_path}")
            raise
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            raise
    
    def detect_grocery_items(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Detect grocery items in an image using OpenAI Vision API.
        
        Analyzes the image to identify food items, groceries, and cooking ingredients
        with detailed descriptions and confidence levels.
        
        Args:
            image_path: Path to the image file to analyze
            
        Returns:
            List[Dict[str, Any]]: List of detected items with metadata:
                - name: Item name/description
                - confidence: Detection confidence (0.0-1.0)
                - category: Item category (e.g., "vegetable", "protein")
                - description: Detailed description
                
        Raises:
            Exception: If detection fails, returns empty list
        """
        try:
            # Encode image for API
            base64_image = self._encode_image(image_path)
            
            # Construct detailed prompt for comprehensive detection
            prompt = """
            Analyze this image and identify ALL grocery items, food ingredients, and cooking supplies visible.
            
            Look carefully at:
            - Fresh produce (fruits, vegetables)
            - Packaged foods and containers
            - Bottles and jars (sauces, condiments, beverages)
            - Dairy products and proteins
            - Pantry items and spices
            - Any branded products (read labels when visible)
            
            Be thorough and specific. For example:
            - Instead of just "bottle", identify "olive oil bottle" or "soy sauce bottle"
            - Instead of "vegetable", specify "red bell pepper" or "fresh broccoli"
            - Include brand names when clearly visible
            - Look in all areas of the image, including background items
            
            Return a JSON array with 10-15 items (if available) in this exact format:
            [
                {
                    "name": "specific item name",
                    "confidence": 0.95,
                    "category": "category type",
                    "description": "detailed description"
                }
            ]
            
            Categories should be: vegetable, fruit, protein, dairy, pantry, condiment, beverage, spice, other
            """
            
            logger.info(f"Analyzing image with OpenAI Vision: {image_path}")
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"  # Use high detail for better accuracy
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1200,  # Increased for detailed responses
                temperature=0.2,  # Lower temperature for more focused results
            )
            
            # Extract and parse response
            content = response.choices[0].message.content
            logger.debug(f"Raw OpenAI response: {content}")
            
            # Parse JSON response
            detections = self._parse_vision_response(content)
            
            # Filter by confidence threshold
            filtered_detections = [
                detection for detection in detections 
                if detection.get('confidence', 0) >= self.confidence_threshold
            ]
            
            logger.info(f"Detected {len(filtered_detections)} items above confidence threshold {self.confidence_threshold}")
            return filtered_detections
            
        except Exception as e:
            logger.error(f"Error in grocery detection: {e}")
            return []
    
    def _parse_vision_response(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse OpenAI Vision API response into structured detections.
        
        Extracts JSON data from the API response, handling various response formats
        and providing fallback parsing for malformed JSON.
        
        Args:
            content: Raw response content from OpenAI Vision API
            
        Returns:
            List[Dict[str, Any]]: Parsed detection results
        """
        try:
            # Try to find JSON in the response
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = content[json_start:json_end]
                detections = json.loads(json_str)
                
                # Validate and normalize detection format
                normalized_detections = []
                for detection in detections:
                    if isinstance(detection, dict) and 'name' in detection:
                        normalized_detection = {
                            'name': detection.get('name', 'unknown'),
                            'confidence': float(detection.get('confidence', 0.5)),
                            'category': detection.get('category', 'other'),
                            'description': detection.get('description', detection.get('name', 'unknown'))
                        }
                        normalized_detections.append(normalized_detection)
                
                logger.info(f"Successfully parsed {len(normalized_detections)} detections")
                return normalized_detections
            else:
                logger.warning("No JSON array found in response, attempting text parsing")
                return self._parse_text_response(content)
                
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {e}, attempting text parsing")
            return self._parse_text_response(content)
        except Exception as e:
            logger.error(f"Error parsing vision response: {e}")
            return []
    
    def _parse_text_response(self, content: str) -> List[Dict[str, Any]]:
        """
        Fallback parser for non-JSON responses from Vision API.
        
        Attempts to extract item names from plain text responses when
        JSON parsing fails.
        
        Args:
            content: Raw text content from API response
            
        Returns:
            List[Dict[str, Any]]: Basic detection results from text parsing
        """
        logger.warning("Using fallback text parsing - JSON format preferred")
        return []  # Return empty list instead of hardcoded fallbacks
    
    def get_ingredient_suggestions(self, detections: List[Dict[str, Any]]) -> List[str]:
        """
        Convert detected items into cooking ingredient suggestions.
        
        Transforms raw detection results into a clean list of ingredients
        suitable for recipe generation, with filtering and normalization.
        
        Args:
            detections: List of detection results from detect_grocery_items()
            
        Returns:
            List[str]: Clean list of ingredient names for cooking
        """
        if not detections:
            logger.warning("No detections provided for ingredient suggestions")
            return []
        
        ingredients = []
        seen_ingredients = set()  # Avoid duplicates
        
        for detection in detections:
            item_name = detection.get('name', '').lower().strip()
            category = detection.get('category', 'other').lower()
            
            if not item_name:
                continue
            
            # Clean and normalize ingredient name
            clean_name = self._normalize_ingredient_name(item_name)
            
            # Filter out non-food items and generic terms
            if self._is_valid_ingredient(clean_name, category):
                if clean_name not in seen_ingredients:
                    ingredients.append(clean_name)
                    seen_ingredients.add(clean_name)
        
        # Sort by relevance (prioritize common cooking ingredients)
        ingredients.sort(key=lambda x: self._get_ingredient_priority(x))
        
        logger.info(f"Generated {len(ingredients)} ingredient suggestions")
        return ingredients[:15]  # Limit to top 15 suggestions
    
    def _normalize_ingredient_name(self, name: str) -> str:
        """
        Normalize ingredient name for cooking use.
        
        Cleans and standardizes ingredient names by removing unnecessary
        descriptors and converting to standard cooking terminology.
        
        Args:
            name: Raw ingredient name from detection
            
        Returns:
            str: Normalized ingredient name
        """
        # Remove common non-essential words
        remove_words = [
            'fresh', 'organic', 'bottle', 'jar', 'can', 'package', 'container',
            'bag', 'box', 'carton', 'tube', 'frozen', 'canned', 'dried'
        ]
        
        words = name.lower().split()
        filtered_words = [word for word in words if word not in remove_words]
        
        # Join and clean
        clean_name = ' '.join(filtered_words).strip()
        
        # Handle special cases
        ingredient_mappings = {
            'bell pepper': 'bell peppers',
            'red pepper': 'red bell pepper',
            'green pepper': 'green bell pepper',
            'yellow pepper': 'yellow bell pepper',
            'soy sauce': 'soy sauce',
            'olive oil': 'olive oil',
            'cooking oil': 'cooking oil',
            'vegetable oil': 'vegetable oil',
        }
        
        return ingredient_mappings.get(clean_name, clean_name)
    
    def _is_valid_ingredient(self, name: str, category: str) -> bool:
        """
        Check if detected item is a valid cooking ingredient.
        
        Filters out non-food items, packaging, and overly generic terms
        to ensure only useful cooking ingredients are suggested.
        
        Args:
            name: Normalized ingredient name
            category: Item category from detection
            
        Returns:
            bool: True if item is a valid cooking ingredient
        """
        if len(name) < 2:  # Too short
            return False
        
        # Filter out generic/unhelpful terms
        invalid_terms = {
            'unknown', 'other', 'mixed', 'variety', 'assorted', 'generic',
            'food', 'item', 'product', 'thing', 'stuff', 'container',
            'package', 'wrapper', 'label', 'brand'
        }
        
        if name in invalid_terms:
            return False
        
        # Accept food-related categories
        food_categories = {
            'vegetable', 'fruit', 'protein', 'dairy', 'pantry', 
            'condiment', 'spice', 'herb', 'grain', 'legume'
        }
        
        return category in food_categories or any(word in name for word in [
            'oil', 'sauce', 'spice', 'herb', 'salt', 'pepper', 'vinegar'
        ])
    
    def _get_ingredient_priority(self, ingredient: str) -> int:
        """
        Get priority score for ingredient sorting.
        
        Assigns priority scores to ingredients to sort them by usefulness
        in cooking, with common/versatile ingredients getting higher priority.
        
        Args:
            ingredient: Ingredient name
            
        Returns:
            int: Priority score (lower = higher priority)
        """
        # High priority ingredients (common in many recipes)
        high_priority = {
            'onion', 'garlic', 'tomato', 'potato', 'carrot', 'bell pepper',
            'olive oil', 'salt', 'pepper', 'eggs', 'butter', 'cheese'
        }
        
        # Medium priority ingredients
        medium_priority = {
            'chicken', 'beef', 'fish', 'rice', 'pasta', 'bread', 'milk',
            'lettuce', 'spinach', 'broccoli', 'lemon', 'lime'
        }
        
        if ingredient in high_priority:
            return 1
        elif ingredient in medium_priority:
            return 2
        else:
            return 3
    
    def _get_fallback_detections(self) -> List[Dict[str, Any]]:
        """
        Get fallback detections when AI vision fails.
        
        Previously provided hardcoded fallback ingredients, now returns
        empty list to rely solely on AI detection.
        
        Returns:
            List[Dict[str, Any]]: Empty list (no fallback ingredients)
        """
        logger.warning("No fallback ingredients provided - relying on AI model only.")
        return [] 