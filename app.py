from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_vision_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to load Google Gemini Pro Text API and get response
def get_gemini_text_response(input, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, prompt])
    return response.text

# Function to set up image for processing
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to calculate BMI and return the result
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return bmi

# Function to calculate daily calorie intake recommendation based on BMI
def calculate_daily_calories(bmi, age):
    bmr = 10 * weight + 6.25 * height - 5 * float(age) + 5  # Harris-Benedict equation for BMR
    activity_factor = 1.2  # Sedentary activity level (can be adjusted based on lifestyle)
    daily_calories = bmr * activity_factor
    return daily_calories

# Initialize Streamlit app
st.set_page_config(page_title="🌈 NutriSense AI")

# Front page
st.title("🌟 Welcome to NutriSense AI 🌟")
st.markdown("---")

st.header("🍏 About NutriSense AI 🍎")
st.write("""
NutriSense AI is an intelligent nutrition and wellness assistant powered by artificial intelligence. It provides various tools and features to help you maintain a healthy lifestyle through proper nutrition. From calculating your BMI to Recommending Indian Lifestyle to cure the disease or giving suggestions based on the user's concern , NutriSense AI has got you covered.

With the help of cutting-edge AI technology, NutriSense AI aims to revolutionize the way you approach nutrition, making it easier for you to make informed decisions about your diet and overall well-being.
""")
st.markdown("---")

st.header("🥦 Why Good Nutrition Matters 🥑")
st.write("""
Good nutrition plays a crucial role in maintaining overall health and well-being. It provides essential nutrients that support bodily functions, promote growth and development, and reduce the risk of chronic diseases. A balanced diet rich in fruits, vegetables, lean proteins, and whole grains can help you:

- Maintain a healthy weight
- Boost your immune system
- Improve energy levels
- Enhance mental clarity and focus
- Prevent and manage various health conditions
""")
st.markdown("---")

st.header("🔍 Understanding BMI and Calories 🔥")
st.write("""
**Body Mass Index (BMI):** BMI is a measure of body fat based on your weight and height. It is used to classify individuals into different weight categories, such as underweight, normal weight, overweight, and obese. Calculating your BMI can help assess your risk of developing weight-related health issues.

**Calories:** Calories are units of energy derived from the food and beverages we consume. They are essential for fueling our bodies and supporting various physiological functions. Monitoring calorie intake is important for maintaining a healthy weight and meeting nutritional needs.
""")
st.markdown("---")

st.header("💡 How NutriSense AI Can Help 💪")
st.write("""
NutriSense AI leverages advanced AI algorithms to provide personalized nutrition recommendations tailored to your specific needs and goals. Whether you're looking to lose weight, gain muscle, or improve overall health, NutriSense AI offers a range of features to help you achieve your objectives:

- **BMI Calculator:** Quickly calculate your BMI to assess your weight status and health risk.
- **Diet Chart Generator:** Generate customized diet charts based on your daily calorie intake and dietary preferences.
- **Calorie Advisor:** Get expert advice on calorie intake and nutritional content by analyzing food images.
- **AI Recipe Generator:** Discover delicious and nutritious recipes curated by AI, perfect for your dietary requirements.
- **Lifestyle Recommendation:** Receive personalized lifestyle recommendations based on your health concerns or diseases, including activities like pranayama, yogic kriyas, mudras, eating habits, and sleeping schedule.

With NutriSense AI, achieving your health and fitness goals has never been easier!
""")
st.markdown("---")

st.header("❓ FAQs ❓")
st.write("""
**Q: Is NutriSense AI free to use?**
A: Yes, NutriSense AI is completely free to use. Simply navigate to the desired feature from the sidebar and start exploring!

**Q: How accurate are the nutrition recommendations provided by NutriSense AI?**
A: While NutriSense AI strives to provide accurate and helpful recommendations, it's important to consult with a healthcare professional or nutritionist for personalized advice tailored to your specific needs and circumstances.

**Q: Can I trust the AI-generated recipes to be healthy and nutritious?**
A: NutriSense AI's recipe generator is trained on a diverse dataset of recipes to ensure variety and balance. However, it's always a good idea to review the ingredients and nutritional information before preparing any recipe to ensure it aligns with your dietary goals and restrictions.
""")
st.markdown("---")

# Sidebar
st.sidebar.title("🌈 Features 🌈")
selected_option = st.sidebar.radio("Select an option", ["BMI Calculator", "Diet Chart Generator", "Calorie Advisor", "AI Recipe Generator", "Lifestyle Recommendation"])

# Main content
if selected_option == "Calorie Advisor":
    st.subheader("🍽️ Calorie Advisor 📊")
    
    # File uploader for image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    # Display uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Button to trigger calorie calculation
    if st.button("Tell me the total calories"):
        if uploaded_file is not None:
            image_data = input_image_setup(uploaded_file)
            input_prompt = """
            You are a nutrition expert. Please provide details of the food items in the image to calculate the total calories. ALso tell about carbohydrates,fats, fiber , cholestrol , proteins, vitamins, minerals, etc...basically decribe the amount of each nutrient the image contains
            Please format the input as follows:
            1. Item 1 - No. of calories
            2. Item 2 - No. of calories
            ----
            ----
            """
            response = get_gemini_vision_response("", image_data, input_prompt)
            st.subheader("Response:")
            st.write(response)
            
            # Add answer to input prompt
            answer_prompt = "Can you provide more details about these food items and who should eat and who should avoid, like for which diseases it would benefit and which diseases it is recommended by doctors to avoid?"
            answer_response = get_gemini_text_response(response, answer_prompt)
            st.write(answer_response)
        else:
            st.warning("Please upload an image to proceed.")

elif selected_option == "BMI Calculator":
    st.subheader("📏 BMI Calculator ⚖️")
    
    # Text inputs for user's weight and height
    weight_kg = st.text_input("Body Weight in kg:", key="weight_input")
    height_cm = st.text_input("Body Height in cm:", key="height_input")
    age = st.text_input("Age in years:", key="age_input")
    
    # Button to calculate BMI
    if st.button("Calculate BMI"):
        if weight_kg and height_cm and age:
            weight = float(weight_kg)
            height = float(height_cm)
            age = float(age)
            bmi = calculate_bmi(weight, height)
            st.write(f"Your BMI is: {bmi:.2f}")
            if bmi < 18.5:
                st.write("Weight Status: Underweight")
            elif 18.5 <= bmi < 25:
                st.write("Weight Status: Normal weight")
            elif 25 <= bmi < 30:
                st.write("Weight Status: Overweight")
            else:
                st.write("Weight Status: Obese")

            # Calculate daily calorie intake recommendation
            if bmi >= 18.5:  # Only calculate for non-underweight individuals
                daily_calories = calculate_daily_calories(bmi, age)
                st.write(f"Recommended Daily Calorie Intake: {daily_calories:.2f} calories")
                # Store the calculated daily calorie intake in session state
                st.session_state['daily_calories'] = daily_calories
            else:
                st.write("As you are underweight, it's recommended to consult with a healthcare professional for personalized advice on calorie intake.")
        else:
            st.warning("Please enter both weight, height, and age to calculate BMI.")

elif selected_option == "Diet Chart Generator":
    st.subheader("📋 Diet Chart Generator 🍽️")
    
    # Retrieve daily calorie intake from session state
    if 'daily_calories' in st.session_state:
        daily_calories = st.session_state['daily_calories']
    else:
        daily_calories = None
    
    # Text input for user's daily calorie intake
    daily_calories_input = st.text_input("Enter your daily calorie intake (in calories):", key="daily_calories_input", value=daily_calories)
    
    # Button to generate diet chart text
    if st.button("Generate Diet Chart Text"):
        if daily_calories_input:
            # Generate diet chart based on daily calorie intake
            diet_chart_prompt = """
            You are an expert Indian Dietician who is aware about Importance of Indian Millets , Indian super foods and different Indian delicacy where your task is to generate a balanced pure vegetarian Balanced Indian diet chart which should have complete nutritional value and  also include Millets and Ancient Indian super foods for a week or 7 days
            based on the daily calorie intake provided by the user.
            Daily Calorie Intake: {}
            """.format(daily_calories_input)
            diet_chart_text = get_gemini_text_response(daily_calories_input, diet_chart_prompt)
            st.subheader("Diet Chart Text:")
            st.write(diet_chart_text)
        else:
            st.warning("Please enter your daily calorie intake to generate the diet chart.")

elif selected_option == "AI Recipe Generator":
    st.subheader("🍲 AI Recipe Generator 🍽️")
    
    # Text input for dish name or description
    dish_input = st.text_input("Enter Dish Name or Description:", key="dish_input")
    
    # File uploader for dish image
    uploaded_dish_image = st.file_uploader("Upload Dish Image (Optional)...", type=["jpg", "jpeg", "png"])
    
    # Button to generate recipe
    if st.button("Generate Recipe"):
        if dish_input or uploaded_dish_image:
            if uploaded_dish_image:
                dish_image_data = input_image_setup(uploaded_dish_image)
                recipe_prompt = """
                You are a professional chef. Please provide a recipe for the dish in the image.
                Include ingredients, cooking instructions, and estimated cooking time.
                """
                recipe = get_gemini_vision_response(dish_input, dish_image_data, recipe_prompt)
            else:
                recipe_prompt = """
                You are a professional chef. Please provide a recipe for '{}'.
                Include ingredients, cooking instructions, and estimated cooking time.
                """.format(dish_input)
                recipe = get_gemini_text_response(dish_input, recipe_prompt)
            
            st.subheader("Generated Recipe:")
            st.write(recipe)
        else:
            st.warning("Please enter a dish name or upload an image to generate the recipe.")

elif selected_option == "Lifestyle Recommendation":
    st.subheader("🌱 Lifestyle Recommendation 🌱")
    
    # Text input for user's health concern or disease
    health_concern = st.text_input("Enter your health concern or disease:")
    
    # Button to generate lifestyle recommendation
    if st.button("Generate Lifestyle Recommendation"):
        if health_concern:
            lifestyle_prompt = """
            You are an Indian Wellness expert who remain up to date on the newest nutrition research and advancements by reading Indian ancient and scientific publications on a regular basis, attending continuing education courses and seminars, and engaging in professional development programmes.. Please provide lifestyle recommendations for someone with {}.
            Include activities such as pranayama, yogic kriyas, mudras, eating habits, and sleeping schedule. You can also mention about Nani/Dadi maa home remedies for that concern or disease .
            Also tell the importance of slow cooking in earthen pots as they They help retain the nutrients in the food, ensuring that the food is healthy and nutritious.Also share some facts like drinking water in copper utensuls and other well known ancient indian lifestyle fatcs to keep a healthy body and mind do not mention everytime, only mention if it is realted to the concern added by ht user .....
            """.format(health_concern)
            lifestyle_recommendation = get_gemini_text_response(health_concern, lifestyle_prompt)
            st.subheader("Lifestyle Recommendation:")
            st.write(lifestyle_recommendation)
        else:
            st.warning("Please enter your health concern or disease to generate the lifestyle recommendation.")
