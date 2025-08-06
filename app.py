from flask import Flask, render_template, request,redirect,url_for, make_response,json
import pandas as pd
import random
import difflib
import os
from datetime import datetime ,timedelta # For timestamp
from flask import make_response
from xhtml2pdf import pisa
from io import BytesIO
import requests



app = Flask(__name__)

# Function to get nutritional data from Open Food Facts API
def get_nutrition_data_from_open_food_facts(food_name):
    url = f'https://world.openfoodfacts.org/api/v0/product/{food_name}.json'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data.get('product'):
            product = data['product']
            nutriments = product.get('nutriments', {})

            return {
                'Food': food_name,
                'Calories': nutriments.get('energy-kcal_100g', 'N/A'),
                'Proteins': nutriments.get('proteins_100g', 'N/A'),
                'Fats': nutriments.get('fat_100g', 'N/A'),
                'Carbohydrates': nutriments.get('carbohydrates_100g', 'N/A'),
                'Fiber': nutriments.get('fiber_100g', 'N/A'),
            }
        else:
            return None  # No data found for the food item
    else:
        return None  # API call failed


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get user input
        age = int(request.form['age'])
        weight = int(request.form['weight'])
        height = float(request.form['height'])
        goal = request.form['goal'].lower()
        
        activity = request.form['activity'].lower()

        # Load food data
        food_df = pd.read_csv('diet_data.csv')
        recipe_df = pd.read_csv('indian_recipes.csv')

        # Clean column names
        food_df.columns = [col.strip() for col in food_df.columns]
        recipe_df.columns = [col.strip() for col in recipe_df.columns]

        # Filter based on goal
        if goal == 'gain':
            food_df = food_df.sort_values(by=['Calories', 'Proteins'], ascending=False)
        elif goal == 'loss':
            food_df = food_df.sort_values(by=['Calories', 'Fats'], ascending=True)
        elif goal == 'maintain':
            food_df = food_df.sort_values(by=['Fats', 'Carbohydrates'], ascending=True)

        # Pick meals
        breakfast_items = food_df[food_df['Breakfast'] == 1].head(3)
        lunch_items = food_df[food_df['Lunch'] == 1].head(3)
        dinner_items = food_df[food_df['Dinner'] == 1].head(3)

         # Fetch nutritional data for recommended food
        food_nutrition = []
        for food in breakfast_items['Food']:
            nutrition = get_nutrition_data_from_open_food_facts(food)
            if nutrition:
                food_nutrition.append(nutrition)

        # Combine food recommendations
        food = f"""
        🥣 <strong>Breakfast</strong>: {', '.join(breakfast_items['Food'])}<br>
        🍛 <strong>Lunch</strong>: {', '.join(lunch_items['Food'])}<br>
        🍽️ <strong>Dinner</strong>: {', '.join(dinner_items['Food'])}
        """

        # Nutrition details as a sample
        nutrition_details = ""
        for item in food_nutrition:
            nutrition_details += f"""
            <strong>{item['Food']}</strong><br>
            Calories: {item['Calories']}<br>
            Proteins: {item['Proteins']}<br>
            Fats: {item['Fats']}<br>
            Carbohydrates: {item['Carbohydrates']}<br>
            Fiber: {item['Fiber']}<br><br>
            """


   

        # Match recipe using fuzzy match
        all_recipes = recipe_df['TranslatedRecipeName'].dropna().tolist()
        first_food = breakfast_items.iloc[0]['Food']
        match = difflib.get_close_matches(first_food, all_recipes, n=1, cutoff=0.5)

        if match:
            chosen = recipe_df[recipe_df['TranslatedRecipeName'] == match[0]].iloc[0]
            ingredients = chosen.get('TranslatedIngredients') or chosen.get('Ingredients', '')
            steps = chosen.get('TranslatedInstructions') or chosen.get('Instructions', '')
            url = chosen.get('URL', '#')
            recipe = f"""
            <strong>🍽 {match[0]}</strong><br>
            <br><strong>Ingredients:</strong><br>{ingredients}
            <br><br><strong>Steps:</strong><br>{steps}
            <br><br><a href="{url}" target="_blank">🔗 View Full Recipe</a>
            """
        else:
            recipe = "⚠️ Recipe not found for the recommended food."

        # Fitness Tip
        fitness = {
            'low': "Start walking 30 mins daily or light yoga.",
            'medium': "Do 30-45 mins of mixed cardio & strength training.",
            'high': "Keep up with intense workouts. Focus on hydration and protein intake."
        }.get(activity, "Maintain a healthy routine.")

        # 🍽️ Meal Timings Logic
        activity = request.form.get('activity_level')
        activity_map = {
            'low': 0,
            'medium': 1,
            'high': 2
        }
        activity_level = activity_map.get(activity, 1)
      
        meal_timings = {
             0: {'Breakfast': '9:00 AM', 'Lunch': '1:30 PM', 'Snacks': '5:00 PM', 'Dinner': '8:30 PM'},
             1: {'Breakfast': '8:00 AM', 'Lunch': '1:00 PM', 'Snacks': '4:30 PM', 'Dinner': '8:00 PM'},
            2: {'Breakfast': '7:30 AM', 'Lunch': '12:30 PM', 'Snacks': '4:00 PM', 'Dinner': '7:30 PM'},
        }
        user_meal_timing = meal_timings[activity_level]

        # Water Reminder (based on user's weight)
        water_intake = weight * 0.033  # Rough estimate in liters
        water_reminder = f"Reminder: Drink {water_intake:.2f} liters of water today. Stay hydrated!"

          # ✅ Save user history to CSV
        history_entry = {
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Age': age,
            'Weight': weight,
            'Height': height,
            'Goal': goal,
            'Activity': activity,
            'Food': food,
            'Recipe': recipe,
            'Fitness': fitness,
            'MealTimings': json.dumps(meal_timings),
            'WaterReminder': water_reminder

        }

        history_df = pd.DataFrame([history_entry])
        
        try:
            existing_df = pd.read_csv('user_history.csv')
            header_flag = False if not existing_df.empty else True
            combined_df = pd.concat([existing_df, history_df], ignore_index=True)
        except FileNotFoundError:
            header_flag = True
            combined_df = history_df

        # ✅ Save updated history
        combined_df.to_csv('user_history.csv', index=False)

       

        return render_template("result.html", 
                               food=food,
                            #    recipe=recipe, 
                               fitness=fitness,
                               user_meal_timing = user_meal_timing,
                               water_reminder=water_reminder,
                               nutrition=food_nutrition)

    return render_template('home.html')  # Form page


@app.route('/download', methods=['POST'])
def download_pdf():
    food = request.form['food']
    recipe = request.form['recipe']
    fitness = request.form['fitness']

    html = render_template('pdf_template.html', food=food, recipe=recipe, fitness=fitness)
    
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    if pisa_status.err:
        return "PDF generation error!"

    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=diet_plan.pdf'
    return response

# ✅ Add the /history route here with search functionality
@app.route('/history', methods=['GET', 'POST'])
def history():
    search_query = request.form.get('search', '')
    
    try:
        history_df = pd.read_csv('user_history.csv')
        history_df.fillna("N/A", inplace=True)

        if search_query:
            history_df = history_df[history_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    except FileNotFoundError:
        history_df = pd.DataFrame(columns=["Timestamp", "Age", "Weight", "Height", "Goal", "Activity", "Food", "Recipe", "Fitness"])

    return render_template("history.html", history=history_df.to_dict(orient='records'))

# ✅ Add clear history functionality
@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        # Delete the history CSV file
        os.remove('user_history.csv')
    except FileNotFoundError:
        pass
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
