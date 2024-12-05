import pandas as pd
import random
from flask import session

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            print("CSV file is empty. Generating fake data...")
            return generate_fake_data()
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return generate_fake_data()
    except pd.errors.EmptyDataError:
        print("Empty data in CSV file. Generating fake data...")
        return generate_fake_data()
 
def generate_fake_data():
    """Generates fake house data."""
    locations = ["City Center", "Beachfront", "Mountain View"]
    prices = [50, 100, 150]
    descriptions = [
        "Cozy apartment in the heart of the city.",
        "Beautiful beachfront villa with stunning views.",
        "Charming cabin nestled in the mountains.",
    ]
    images = ["image1.jpg", "image2.jpg", "image3.jpg"]

    df = pd.DataFrame(columns=["Location", "Price", "Description", "Image"])

    for _ in range(10):
        location = random.choice(locations)
        price = random.choice(prices)
        description = descriptions[prices.index(price)]
        image = images[prices.index(price)]
        df = df.append(
            {"Location": location, "Price": price, "Description": description, "Image": image},
            ignore_index=True,
        )

    return df

def optimize_feed(df, clicked_house_id):
   
    if df.empty:
        print("DataFrame is empty. Cannot optimize feed.")
        return df

    clicked_house = df.loc[df['id'] == clicked_house_id]

    # Calculate similarity scores based on location and price
    
    df['PriceDifference'] = abs(df['Price'] - clicked_house['Price'].values[0])

    # Sort by similarity and return the top N results
    return df.sort_values(by='PriceDifference')

def calculate_similarity(row, clicked_house):
    if clicked_house.empty:
        return 0

    # Assuming clicked_house is a single-row DataFrame
    clicked_location = clicked_house['Location'].values[0]
    clicked_price = clicked_house['Price'].values[0]

    location_similarity = int(row['Location'] == clicked_location)
    price_similarity = 1 - abs(row['Price'] - clicked_price) / max(row['Price'], clicked_price)

    return location_similarity + price_similarity

def generate_fake_data(num_houses=100, filename="houses.csv"):
    locations = ["City Center", "Beachfront", "Mountain View", "Suburban", "Rural"]
    amenities = ["Wi-Fi", "Breakfast Included", "Parking", "Pool", "Gym"]
    categories = ["Non-Veg", "Veg"]

    data = []
    for i in range(1, num_houses + 1):
        location = random.choice(locations)
        price = random.randint(100, 10000)
        description = f"A {random.choice(['cozy', 'spacious', 'modern'])} {location} house with {random.choice(amenities)}."
        image = f"image_{random.randint(1, 10)}.jpg"
        category = random.choice(categories)
        data.append([i, location, price, description, image, category])

    df = pd.DataFrame(data, columns=["id", "Location", "Price", "Description", "Image", "Category"])
    df.to_csv(filename, index=False)

    print(f"Fake data saved to {filename}")
    return df