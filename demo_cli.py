"""Command-line demo: classify a food image and estimate calories.

Usage:
    python3 demo_cli.py <image_path> [--portions 1.5] [--top-k 3]
"""
import argparse
import sys

from food_classifier import predict
from calorie_estimator import get_nutrition, pretty_name


def main():
    parser = argparse.ArgumentParser(
        description="Food recognition and calorie estimation (CLI demo)"
    )
    parser.add_argument("image", help="Path to a food image file")
    parser.add_argument("--portions", type=float, default=1.0,
                        help="Number of servings (default: 1.0)")
    parser.add_argument("--top-k", type=int, default=3,
                        help="Show top-k predictions (default: 3)")
    args = parser.parse_args()

    try:
        results = predict(args.image, top_k=args.top_k)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\n🔍 Top predictions:")
    for i, (label, conf) in enumerate(results, 1):
        print(f"  {i}. {pretty_name(label)} — {conf * 100:.1f}%")

    top_label = results[0][0]
    nutrition = get_nutrition(top_label, portions=args.portions)
    print("\n🔥 Calorie estimation:")
    if nutrition:
        print(f"  Food:      {nutrition['name']}")
        print(f"  Serving:   {nutrition['serving']} x {args.portions}")
        print(f"  Calories:  {nutrition['calories']} kcal")
        print(f"  Protein:   {nutrition['protein_g']} g")
        print(f"  Carbs:     {nutrition['carbs_g']} g")
        print(f"  Fat:       {nutrition['fat_g']} g")
    else:
        print("  Nutrition data not available for this food.")


if __name__ == "__main__":
    main()
