# =========================================================
# 🌐 FeelTrip India — Multilingual Travel Planner (Colab)
# =========================================================
# Uses ONE combined dataset: feeltrip_combined.csv
# Columns: Place, Viewpoint, Entry Ticket (₹), Hotel Name, Budget Category,
#          Hotel Cost Per Night (₹), Restaurant Name, Avg Bill (₹),
#          Menu Dishes, Dish Prices (₹)
# 576 rows across 33 places — built by cleaning + recombining your
# original dataset (fixed inconsistent hotel categories, deduplicated
# viewpoints/hotels/restaurants, then merged into one file).

# %% [1] Install dependencies
!pip install pandas gradio deep-translator --quiet

# %% [2] Imports
import pandas as pd
import gradio as gr
from deep_translator import GoogleTranslator

# %% [3] Load the dataset
# --- Option A: upload directly in Colab ---
# from google.colab import files
# uploaded = files.upload()  # select feeltrip_combined.csv
# df = pd.read_csv("feeltrip_combined.csv")

# --- Option B: from Google Drive ---
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv("/content/drive/MyDrive/feeltrip_combined.csv")
df.columns = [c.strip() for c in df.columns]

# %% [4] Language setup — deep-translator uses standard Google codes,
# which already match the keys below.
lang_choices = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "ml": "Malayalam",
    "kn": "Kannada",
    "gu": "Gujarati",
    "mr": "Marathi",
    "bn": "Bengali",
}

def translate_text(text, target_lang):
    if target_lang == "en" or not text.strip():
        return text
    try:
        chunks = [text[i:i + 4500] for i in range(0, len(text), 4500)]
        translated = [GoogleTranslator(source="en", target=target_lang).translate(c) for c in chunks]
        return "".join(translated)
    except Exception as e:
        return f"{text}\n\n[Translation unavailable: {e}]"

# %% [5] Helpers
def safe_int(value, default=0):
    try:
        if pd.isnull(value):
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_str(value, default="N/A"):
    return default if pd.isnull(value) else str(value)

# %% [6] Travel planning logic — no repeated viewpoints across the trip
def generate_travel_plan(place, budget, num_people, trip_days, target_lang):
    if not place or not str(place).strip():
        return translate_text("Please enter a place name.", target_lang)

    try:
        budget = float(budget)
        num_people = int(num_people)
        trip_days = int(trip_days)
    except (ValueError, TypeError):
        return translate_text("Please enter valid numbers for budget, people, and days.", target_lang)

    if num_people <= 0 or trip_days <= 0:
        return translate_text("Number of people and trip days must be at least 1.", target_lang)

    place_key = place.lower().strip()
    place_rows = df[df["Place"].str.lower().str.strip() == place_key]
    if place_rows.empty:
        known_places = ", ".join(sorted(df["Place"].unique())[:10])
        return translate_text(
            f"Sorry, we couldn't find that location in our database. Try one of: {known_places}...",
            target_lang,
        )

    # Derive unique viewpoints, hotels, restaurants for this place from the combined table.
    vps = place_rows[["Viewpoint", "Entry Ticket (₹)"]].drop_duplicates(subset=["Viewpoint"]).reset_index(drop=True)
    hotels = place_rows[["Hotel Name", "Budget Category", "Hotel Cost Per Night (₹)"]].drop_duplicates(subset=["Hotel Name"]).reset_index(drop=True)
    rests = place_rows[["Restaurant Name", "Avg Bill (₹)", "Menu Dishes", "Dish Prices (₹)"]].drop_duplicates(subset=["Restaurant Name"]).reset_index(drop=True)
    hotels_sorted = hotels.sort_values("Hotel Cost Per Night (₹)")

    days_available = min(trip_days, len(vps))

    def build_plan_for_hotel(hotel_row):
        hotel_cost = safe_int(hotel_row["Hotel Cost Per Night (₹)"], 1000) if hotel_row is not None else 1000
        hotel_name = safe_str(hotel_row["Hotel Name"]) if hotel_row is not None else "Not available"
        hotel_type = safe_str(hotel_row["Budget Category"]) if hotel_row is not None else "N/A"

        days = []
        running_total = 0
        for day in range(1, days_available + 1):
            vp_row = vps.iloc[day - 1]
            entry_fee = safe_int(vp_row["Entry Ticket (₹)"], 0)

            if not rests.empty:
                rest_row = rests.iloc[(day - 1) % len(rests)]  # rotate restaurants
                rest_name = safe_str(rest_row["Restaurant Name"])
                food_cost = safe_int(rest_row["Avg Bill (₹)"], 0)
                dishes = safe_str(rest_row["Menu Dishes"])
                dish_prices = safe_str(rest_row["Dish Prices (₹)"])
            else:
                rest_name, food_cost, dishes, dish_prices = "Not available", 0, "N/A", "N/A"

            day_cost = (entry_fee + food_cost) * num_people
            running_total += day_cost

            days.append({
                "day": day,
                "viewpoint": vp_row["Viewpoint"],
                "entry_fee": entry_fee,
                "restaurant": rest_name,
                "food_cost": food_cost,
                "dishes": dishes,
                "dish_prices": dish_prices,
                "day_cost": day_cost,
            })

        total_cost = running_total + hotel_cost * days_available
        return days, hotel_name, hotel_type, hotel_cost, total_cost

    chosen = None
    if not hotels_sorted.empty:
        for _, hrow in hotels_sorted.iterrows():
            days, hotel_name, hotel_type, hotel_cost, total_cost = build_plan_for_hotel(hrow)
            if total_cost <= budget:
                chosen = (days, hotel_name, hotel_type, hotel_cost, total_cost)
                break
        if chosen is None:
            chosen = build_plan_for_hotel(hotels_sorted.iloc[0])
    else:
        chosen = build_plan_for_hotel(None)

    days, hotel_name, hotel_type, hotel_cost, total_cost = chosen

    day_blocks = []
    for d in days:
        day_blocks.append(f"""📅 Day {d['day']}
🌄 Visiting: {d['viewpoint']} (Entry Fee: ₹{d['entry_fee']})
🍽 Restaurant: {d['restaurant']} (Avg Bill: ₹{d['food_cost']})
🍛 Dishes: {d['dishes']} → ₹{d['dish_prices']}
👥 People: {num_people}
💸 Day Cost (entry + food, for all people): ₹{d['day_cost']}""")

    summary = f"""🧳 Trip Summary
📍 Destination: {place.title()}
🏨 Hotel (for the whole stay): {hotel_name} [{hotel_type}] — ₹{hotel_cost}/night
📅 Days planned: {days_available} of {trip_days} requested
💰 Total trip cost (hotel + all days' entry & food): ₹{total_cost:.0f}
💵 Remaining budget: ₹{budget - total_cost:.0f}"""

    if total_cost > budget:
        summary += f"\n⚠️ This plan exceeds your budget by ₹{total_cost - budget:.0f} — try raising the budget."
    if days_available < trip_days:
        summary += (
            f"\n⚠️ {place.title()} only has {len(vps)} unique places to visit, so we could "
            f"only plan {days_available} no-repeat day(s) instead of {trip_days}."
        )

    output_text = "\n\n".join(day_blocks) + "\n\n" + summary
    return translate_text(output_text, target_lang)

# %% [7] Gradio interface
demo = gr.Interface(
    fn=generate_travel_plan,
    inputs=[
        gr.Textbox(label="📍 Enter Place", placeholder="e.g. Agra"),
        gr.Number(label="💰 Total Budget (₹)", value=10000),
        gr.Number(label="👥 Number of People", value=2),
        gr.Number(label="📅 Trip Days", value=2),
        gr.Dropdown(
            label="🗣 Select Language",
            choices=list(lang_choices.keys()),
            value="en",
        ),
    ],
    outputs=gr.Textbox(label="Your Itinerary", lines=25),
    title="FeelTrip India 🌏",
    description="Multilingual Travel Planner – no repeated viewpoints across your trip.",
)

demo.launch(share=True, debug=True)
