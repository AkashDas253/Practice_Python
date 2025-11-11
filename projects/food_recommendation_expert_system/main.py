# Food Recommendation Expert System using experta
import json
from experta import KnowledgeEngine, Fact, Rule, Field, MATCH

MENU_CONFIG_PATH = "menu_config.json"

class Preference(Fact):
    """User preferences for dish selection"""
    allergy = Field(list, mandatory=False)
    taste = Field(str, mandatory=False)
    type = Field(str, mandatory=False)
    region = Field(str, mandatory=False)

class Dish(Fact):
    """Dish fact for inference"""
    name = Field(str)
    ingredients = Field(list)
    taste = Field(list)
    type = Field(str)
    region = Field(str)

class FoodExpert(KnowledgeEngine):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu



    @Rule(Preference(allergy=MATCH.allergy, taste=MATCH.taste, type=MATCH.type, region=MATCH.region))
    def recommend_dishes(self, allergy, taste, type, region):
        recommendations = []
        for dish in self.menu:
            # Exclude dish if any allergy substring is present in any ingredient
            if allergy:
                found = False
                for a in allergy:
                    for ing in dish['ingredients']:
                        if a in ing:
                            found = True
                            break
                    if found:
                        break
                if found:
                    continue
            match_count = 0
            explanation = []
            if taste and taste in dish['taste']:
                match_count += 1
                explanation.append(f"taste matches '{taste}'")
            if type and dish['type'] == type:
                match_count += 1
                explanation.append(f"type matches '{type}'")
            if region and region in dish['region'].lower():
                match_count += 1
                explanation.append(f"region matches '{region}'")
            if match_count > 0 or (not taste and not type and not region):
                recommendations.append((dish, match_count, explanation))
        # Sort by match_count descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        if recommendations:
            print("Recommended dishes (ordered by match accuracy):")
            for dish, count, explanation in recommendations:
                print(f"- {dish['name']} (matches: {count})")
                print(f"  Ingredients: {', '.join(dish['ingredients'])}")
                print(f"  Taste: {', '.join(dish['taste'])}")
                print(f"  Type: {dish['type']}")
                print(f"  Region: {dish['region']}")
                if explanation:
                    print(f"  Reason: {', '.join(explanation)}")
                print()
        else:
            print("No suitable dishes found for your preferences.")

if __name__ == "__main__":
    with open(MENU_CONFIG_PATH, "r") as f:
        menu_data = json.load(f)["dishes"]

    print("Enter your preferences (leave blank to skip):")
    allergy_raw = input("Allergy (comma separated, ingredients to avoid): ").strip().lower()
    allergy = [a.strip() for a in allergy_raw.split(",") if a.strip()] if allergy_raw else []
    taste = input("Taste: ").strip().lower() or None
    type_ = input("Type (curry/snack/dessert): ").strip().lower() or None
    region = input("Region (Indian/Chinese/Italian): ").strip().lower() or None

    engine = FoodExpert(menu_data)
    engine.reset()
    engine.declare(Preference(allergy=allergy, taste=taste, type=type_, region=region))
    engine.run()
