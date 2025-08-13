#!/usr/bin/env python3
"""
Grocery Detection Testing Utility

Test script for validating OpenAI Vision API integration and grocery detection
capabilities. Used for debugging and verifying AI model performance.

Author: ChefAI Team
Version: 1.0.0
License: MIT
"""

import os
from typing import List, Optional
from grocery_detection_utils import GroceryObjectDetector


def test_api_key() -> bool:
    """
    Test if OpenAI API key is properly configured.
    
    Checks for the presence of OPENAI_API_KEY environment variable
    and provides feedback on configuration status.
    
    Returns:
        bool: True if API key is configured, False otherwise
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("💡 Make sure you have a .env file with your OpenAI API key")
        return False
    
    print("✅ OpenAI API key found")
    print(f"🔑 API key preview: {api_key[:10]}...{api_key[-4:]}")
    return True


def find_test_images() -> List[str]:
    """
    Find available test images for grocery detection testing.
    
    Searches for common image file extensions in the uploads directory
    and returns a list of available test images.
    
    Returns:
        List[str]: List of available test image file paths
    """
    test_image_paths = [
        "uploads/frdge.jpeg",
        "uploads/frdge2.jpeg", 
        "uploads/test.jpg",
        "uploads/sample.jpg",
        "test_image.jpg"
    ]
    
    available_images = []
    for path in test_image_paths:
        if os.path.exists(path):
            available_images.append(path)
            print(f"📸 Found test image: {path}")
    
    if not available_images:
        print("⚠️ No test images found in the following locations:")
        for path in test_image_paths:
            print(f"   - {path}")
        print("\n💡 Add a test image to one of these locations to run detection tests")
    
    return available_images


def test_grocery_detection(image_path: str) -> None:
    """
    Test grocery detection on a single image file.
    
    Initializes the grocery detector, processes the image, and displays
    detailed results including raw detections and ingredient suggestions.
    
    Args:
        image_path: Path to the test image file
    """
    print(f"\n{'='*60}")
    print(f"🧪 Testing Grocery Detection on: {image_path}")
    print(f"{'='*60}")
    
    try:
        # Initialize detector with OpenAI Vision
        print("🔧 Initializing GroceryObjectDetector...")
        detector = GroceryObjectDetector(
            model_source="openai_vision",
            confidence_threshold=0.4
        )
        
        # Test detection
        print("🔍 Running grocery item detection...")
        detections = detector.detect_grocery_items(image_path)
        
        # Display raw detection results
        print(f"\n📊 Raw Detection Results ({len(detections)} items):")
        print("-" * 50)
        
        if detections:
            for i, detection in enumerate(detections, 1):
                print(f"{i:2d}. {detection.get('name', 'Unknown')}")
                print(f"    Category: {detection.get('category', 'other')}")
                print(f"    Confidence: {detection.get('confidence', 0.0):.2f}")
                print(f"    Description: {detection.get('description', 'N/A')}")
                print()
        else:
            print("   No items detected")
        
        # Test ingredient suggestions
        print("🥘 Generating ingredient suggestions...")
        suggestions = detector.get_ingredient_suggestions(detections)
        
        print(f"\n🎯 Ingredient Suggestions ({len(suggestions)} items):")
        print("-" * 50)
        
        if suggestions:
            for i, ingredient in enumerate(suggestions, 1):
                print(f"{i:2d}. {ingredient}")
        else:
            print("   No ingredient suggestions generated")
        
        # Summary statistics
        print(f"\n📈 Detection Summary:")
        print(f"   Total detections: {len(detections)}")
        print(f"   Ingredient suggestions: {len(suggestions)}")
        
        if detections:
            avg_confidence = sum(d.get('confidence', 0) for d in detections) / len(detections)
            print(f"   Average confidence: {avg_confidence:.2f}")
            
            # Category breakdown
            categories = {}
            for detection in detections:
                category = detection.get('category', 'other')
                categories[category] = categories.get(category, 0) + 1
            
            print(f"   Categories detected: {', '.join(f'{cat}({count})' for cat, count in categories.items())}")
        
    except Exception as e:
        print(f"❌ Error during grocery detection test: {e}")
        print("💡 Check your OpenAI API key and internet connection")


def run_comprehensive_test() -> None:
    """
    Run comprehensive grocery detection tests.
    
    Performs complete testing workflow including:
    1. API key validation
    2. Test image discovery
    3. Detection testing on all available images
    4. Results summary and recommendations
    """
    print("🧪 ChefAI Grocery Detection Test Suite")
    print("=" * 60)
    
    # Test API key configuration
    print("\n🔑 Step 1: Testing API Configuration")
    if not test_api_key():
        print("\n❌ Cannot proceed without valid OpenAI API key")
        print("📝 Please set up your .env file with OPENAI_API_KEY")
        return
    
    # Find test images
    print("\n📸 Step 2: Finding Test Images")
    test_images = find_test_images()
    
    if not test_images:
        print("\n⚠️ No test images available for detection testing")
        print("📝 Add test images to run detection validation")
        return
    
    # Test detection on each image
    print("\n🔍 Step 3: Running Detection Tests")
    total_detections = 0
    total_suggestions = 0
    
    for image_path in test_images:
        try:
            # Run detection test
            detector = GroceryObjectDetector()
            detections = detector.detect_grocery_items(image_path)
            suggestions = detector.get_ingredient_suggestions(detections)
            
            total_detections += len(detections)
            total_suggestions += len(suggestions)
            
            # Quick summary for this image
            print(f"\n📊 {os.path.basename(image_path)}: {len(detections)} detections, {len(suggestions)} suggestions")
            
        except Exception as e:
            print(f"❌ Failed to process {image_path}: {e}")
    
    # Final summary
    print(f"\n🎯 Test Suite Summary:")
    print(f"   Images tested: {len(test_images)}")
    print(f"   Total detections: {total_detections}")
    print(f"   Total suggestions: {total_suggestions}")
    
    if total_detections > 0:
        print("✅ Grocery detection system is working!")
    else:
        print("⚠️ No items detected - check image quality or API configuration")
    
    print("\n💡 Tips for better detection:")
    print("   - Use clear, well-lit photos")
    print("   - Ensure items are visible and not obscured")
    print("   - Include a variety of grocery items")
    print("   - Avoid blurry or low-resolution images")


def main() -> None:
    """
    Main entry point for the grocery detection test utility.
    
    Provides an interactive interface for testing grocery detection
    capabilities with available test images.
    """
    try:
        # Run comprehensive test suite
        run_comprehensive_test()
        
        # Offer detailed testing for specific images
        test_images = find_test_images()
        if test_images:
            print(f"\n🔬 Detailed Testing Available")
            print("Run individual tests with specific images:")
            for i, image_path in enumerate(test_images, 1):
                print(f"   python test_grocery_detection.py --image {image_path}")
            
            # If user wants to see detailed results for first image
            if len(test_images) > 0:
                print(f"\n🎯 Running detailed test on first available image...")
                test_grocery_detection(test_images[0])
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please check your configuration and try again")


if __name__ == "__main__":
    main() 