#!/usr/bin/env python3
"""
Test script for recipe generation functionality
Tests various ingredient combinations and moods to validate GPT-J output
"""

from recipe_utils import generate_recipes_from_prompt
import time

def test_recipe_generation():
    """Test recipe generation with predefined ingredients and moods."""
    
    print("🧪 RECIPE GENERATION TEST SUITE")
    print("=" * 80)
    print("Testing GPT-J 6B model with various ingredient combinations...")
    print("=" * 80)
    
    # Test cases: (ingredients, mood, description)
    test_cases = [
        (
            ["chicken", "onions", "garlic", "cheese"],
            "Quick & Easy (5-15 minutes)",
            "Basic protein + aromatics + dairy"
        ),
        (
            ["eggs", "milk", "spinach", "cheese"],
            "Healthy & Light",
            "Breakfast/brunch ingredients"
        ),
        (
            ["potatoes", "carrots", "onions"],
            "Comfort Food", 
            "Vegetable-only comfort meal"
        ),
        (
            ["yogurt", "honey", "apples", "oats"],
            "Creative & Adventurous",
            "Unusual combination test"
        ),
        (
            ["pasta", "tomatoes", "garlic", "cheese"],
            "Kid-Friendly",
            "Classic Italian-style ingredients"
        )
    ]
    
    results = []
    
    for i, (ingredients, mood, description) in enumerate(test_cases, 1):
        print(f"\n{'='*20} TEST CASE {i} {'='*20}")
        print(f"📝 Description: {description}")
        print(f"🥘 Ingredients: {', '.join(ingredients)}")
        print(f"😊 Mood: {mood}")
        print(f"⏱️  Starting generation at {time.strftime('%H:%M:%S')}")
        
        try:
            start_time = time.time()
            
            # Generate recipes
            recipes = generate_recipes_from_prompt(ingredients, mood)
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            print(f"\n✅ GENERATION COMPLETED in {generation_time:.1f} seconds")
            print("=" * 80)
            print("📄 FINAL RECIPE OUTPUT:")
            print("=" * 80)
            print(recipes)
            print("=" * 80)
            
            # Evaluate output quality
            quality_score = evaluate_recipe_quality(recipes, ingredients)
            print(f"🏆 Quality Score: {quality_score}/10")
            
            results.append({
                'test_case': i,
                'description': description,
                'ingredients': ingredients,
                'mood': mood,
                'generation_time': generation_time,
                'quality_score': quality_score,
                'output_length': len(recipes),
                'success': quality_score >= 6  # Consider 6+ as success
            })
            
        except Exception as e:
            print(f"❌ ERROR in test case {i}: {str(e)}")
            results.append({
                'test_case': i,
                'description': description,
                'ingredients': ingredients,
                'mood': mood,
                'generation_time': 0,
                'quality_score': 0,
                'output_length': 0,
                'success': False,
                'error': str(e)
            })
        
        print(f"\n{'='*60}")
        
        # Add delay between tests to prevent overloading
        if i < len(test_cases):
            print("⏳ Waiting 10 seconds before next test...")
            time.sleep(10)
    
    # Print summary
    print_test_summary(results)

def evaluate_recipe_quality(recipe_text, expected_ingredients):
    """
    Simple quality evaluation of generated recipes.
    Returns score out of 10.
    """
    score = 0
    text_lower = recipe_text.lower()
    
    # Check if all ingredients are mentioned (3 points)
    ingredient_mentions = sum(1 for ing in expected_ingredients if ing.lower() in text_lower)
    score += (ingredient_mentions / len(expected_ingredients)) * 3
    
    # Check for cooking terms (2 points)
    cooking_terms = ['heat', 'cook', 'add', 'stir', 'pan', 'minutes', 'oil', 'season', 'serve']
    cooking_mentions = sum(1 for term in cooking_terms if term in text_lower)
    score += min(cooking_mentions / 5, 1) * 2  # Up to 2 points
    
    # Check for recipe structure (2 points)
    has_recipe_name = 'recipe' in text_lower or any(word in text_lower for word in ['bowl', 'skillet', 'mix', 'scramble'])
    has_instructions = any(num in text_lower for num in ['1.', '2.', '3.', 'first', 'then', 'next'])
    score += has_recipe_name * 1
    score += has_instructions * 1
    
    # Check length and completeness (2 points)
    if len(recipe_text) > 200:
        score += 1
    if len(recipe_text) > 400:
        score += 1
    
    # Check for bad content (deduct points)
    bad_phrases = ['click on', 'download', 'website', 'button', 'app', 'program']
    has_bad_content = any(phrase in text_lower for phrase in bad_phrases)
    if has_bad_content:
        score -= 5
    
    # Check for repetitive content (deduct points)
    lines = recipe_text.split('\n')
    unique_lines = set(lines)
    if len(lines) > 5 and len(unique_lines) < len(lines) * 0.7:  # More than 30% repetition
        score -= 2
    
    return max(0, min(10, round(score, 1)))

def print_test_summary(results):
    """Print a summary of all test results."""
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed tests: {len(failed_tests)}")
    
    if successful_tests:
        avg_quality = sum(r['quality_score'] for r in successful_tests) / len(successful_tests)
        avg_time = sum(r['generation_time'] for r in successful_tests) / len(successful_tests)
        print(f"📈 Average quality score: {avg_quality:.1f}/10")
        print(f"⏱️  Average generation time: {avg_time:.1f} seconds")
    
    print("\nDetailed Results:")
    print("-" * 80)
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"Test {result['test_case']}: {status} | Quality: {result['quality_score']}/10 | Time: {result.get('generation_time', 0):.1f}s")
        print(f"   {result['description']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        print()

def quick_test():
    """Quick test with just one ingredient combination."""
    print("🚀 QUICK RECIPE TEST")
    print("=" * 50)
    
    ingredients = ["chicken", "cheese", "onions"]
    mood = "Quick & Easy (5-15 minutes)"
    
    print(f"Testing: {', '.join(ingredients)} - {mood}")
    
    try:
        recipes = generate_recipes_from_prompt(ingredients, mood)
        print("\n📄 Generated Recipes:")
        print("=" * 50)
        print(recipes)
        print("=" * 50)
        
        quality = evaluate_recipe_quality(recipes, ingredients)
        print(f"Quality Score: {quality}/10")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        test_recipe_generation() 