from mensa.models import Mensa

categories = ["Vegan", "Vegetarian", "Pork",
              "Beef", "Poultry", "Alcohol", "Fish"]
additives = ["Dyed", "Preservatives", "Antioxidants", "Flavor enhancers", "Sulphurated", "Blackened", "Waxed",
             "Phosphate", "Sweeteners", "Phenylalanine source"]
allergies = ["Gluten", "Spelt", "Barley", "Oats", "Kamut", "Rye", "Wheat", "Crustaceans", "Egg", "Fish",
             "Peanuts", "Soy", "Milk", "Nuts", "Almonds", "Hazelnuts", "Walnuts", "Cashews", "Pecans",
             "Brazil nuts", "Pistachios", "Macadamias", "Celery", "Mustard", "Sesame", "Lupines", "Molluscs",
             "Sulfur dioxide"]

canteens = [
    Mensa(name_id="bistro-denkpause", name="Bistro Denkpause", street="Corrensstr.", houseNumber="25", zipCode=48149,
          city="Münster", startTime="11:30", endTime="14:15", lat=51.96836, lon=7.594853),
    Mensa(name_id="mensa-da-vinci", name="Mensa Da Vinci", street="Leonardo-Campus", houseNumber="8", zipCode=48149,
          city="Münster", startTime="11:30", endTime="14:00", lat=51.975033, lon=7.602068),
    Mensa(name_id="bistro-katholische-hochschule", name="Bistro Katholische Hochschule", street="Piusallee",
          houseNumber="89", zipCode=48147, city="Münster", startTime="11:30", endTime="13:45", lat=0, lon=0),
    Mensa(name_id="bistro-durchblick", name="Bistro Durchblick", street="Fliednerstr.", houseNumber="21", zipCode=48149,
          city="Münster", startTime="11:30", endTime="13:30", lat=51.963451, lon=7.594432),
    Mensa(name_id="bistro-frieden", name="Bistro Frieden", street="Scharnhorststr.", houseNumber="100", zipCode=48151,
          city="Münster", startTime="08:00", endTime="13:45", lat=51.9507932, lon=7.6079902),
    Mensa(name_id="bistro-kabu", name="Bistro KaBu", street="Domplatz", houseNumber="21", zipCode=48143, city="Münster",
          startTime="11:00", endTime="14:00", lat=51.962632, lon=7.625869),
    Mensa(name_id="bistro-oeconomicum", name="Bistro Oeconomicum", street="Universitätsstr.", houseNumber="14",
          zipCode=48143, city="Münster", startTime="07:30", endTime="18:00", lat=51.9622951, lon=7.6209285),
    Mensa(name_id="hier-und-jetzt", name="Hier und Jetzt", street="Bismarckallee", houseNumber="11", zipCode=48151,
          city="Münster", startTime="11:30", endTime="14:30", lat=51.955540, lon=7.616978),
    # ALSO 17:00-21:00 ._. ; we'll ignore that for now
    Mensa(name_id="mensa-am-aasee", name="Mensa am Aasee", street="Bismarckallee", houseNumber="11", zipCode=48151,
          city="Münster", startTime="11:45", endTime="14:30", lat=51.95559, lon=7.617199),
    Mensa(name_id="mensa-am-ring", name="Mensa am Ring", street="Domagkstr.", houseNumber="61", zipCode=48149,
          city="Münster", startTime="11:30", endTime="14:00", lat=51.965806, lon=7.600138),
    Mensa(name_id="mensa-bispinghof", name="Mensa Bispinghof", street="Bispinghof", houseNumber="9-14", zipCode=48149,
          city="Münster", startTime="11:00", endTime="14:30", lat=51.960372, lon=7.619707)
]

search_params = {
    'q': None,
    'num': 10,
}
