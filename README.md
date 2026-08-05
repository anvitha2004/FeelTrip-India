# 🌏 FeelTrip India – Multilingual Travel Planner

An AI-powered multilingual travel planner that generates personalized travel itineraries based on destination, budget, number of travelers, and trip duration. The application recommends tourist attractions, hotels, restaurants, and estimates total trip expenses while supporting multiple Indian languages.

## ✨ Features

* 📍 Personalized travel itinerary generation
* 💰 Budget-based hotel recommendations
* 🏨 Hotel suggestions with budget categories
* 🍽 Restaurant recommendations with average meal costs
* 🌄 Unique sightseeing locations without repetition
* 💸 Automatic trip cost estimation
* 🌐 Multilingual support using Google Translate
* 🖥 Interactive web interface built with Gradio

## 🛠 Tech Stack

* Python
* Pandas
* Gradio
* Deep Translator (Google Translate API)
* Google Colab

## 📂 Dataset

The project uses a custom travel dataset (`feeltrip_combined.csv`) containing **576 records** across **33 tourist destinations**.

Dataset includes:

* Place
* Viewpoint
* Entry Ticket Price
* Hotel Name
* Budget Category
* Hotel Cost Per Night
* Restaurant Name
* Average Bill
* Menu Dishes
* Dish Prices

## 🚀 How It Works

1. Enter a destination.
2. Provide your total budget.
3. Enter the number of travelers.
4. Specify the number of trip days.
5. Select your preferred language.
6. The application generates a complete day-wise itinerary with:

   * Tourist attractions
   * Hotel recommendation
   * Restaurant suggestions
   * Estimated daily expenses
   * Total trip cost
   * Remaining budget

## 📸 Sample Output

```
📅 Day 1
🌄 Visiting: Taj Mahal
🍽 Restaurant: Pinch of Spice
👥 People: 2
💸 Day Cost: ₹1800

📅 Day 2
🌄 Visiting: Agra Fort
🍽 Restaurant: Esphahan
👥 People: 2
💸 Day Cost: ₹2200

🧳 Trip Summary
Destination: Agra
Hotel: Hotel Atulyaa Taj
Total Cost: ₹7800
Remaining Budget: ₹2200
```

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/FeelTrip-India.git
```

Install the required libraries:

```bash
pip install pandas gradio deep-translator
```

Run the application:

```bash
python app.py
```

or execute the notebook in Google Colab.

## 📁 Project Structure

```
FeelTrip-India/
│── feeltrip_combined.csv
│── FeelTrip_India.ipynb
│── README.md
```

## 🔮 Future Enhancements

* Google Maps integration
* Weather forecast support
* Hotel ratings and reviews
* Route optimization
* Real-time hotel booking APIs
* AI-based personalized recommendations
* Voice-assisted travel planning

## 👩‍💻 Author

**Anvitha Dandamudi**

Computer Science Engineering | AI & NLP Enthusiast

---

If you find this project useful, consider giving it a ⭐ on GitHub.
