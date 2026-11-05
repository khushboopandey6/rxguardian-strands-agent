# clinical_db.py - Real medicine information and safety rules
# I gathered these common medicine pairs from FDA guides and pharmacy tips
# so our agents have accurate health data to look at!

# List of medicines that should NOT be taken together (Drug Interactions)
DRUG_INTERACTIONS = [
    {
        "drugs": ["warfarin", "aspirin"],
        "severity": "HIGH",
        "why_it_happens": "Both drugs thin your blood in different ways. Taking both together can cause serious internal bleeding.",
        "simple_warning": "Warning! Taking Warfarin and Aspirin together makes your blood too thin and can cause dangerous bleeding in your stomach or head.",
        "what_to_do": "Do not take both together unless your doctor specifically told you to and is doing regular blood tests."
    },
    {
        "drugs": ["warfarin", "ibuprofen"],
        "severity": "HIGH",
        "why_it_happens": "Ibuprofen can irritate your stomach lining while Warfarin keeps blood from clotting.",
        "simple_warning": "Warning! Ibuprofen (Advil/Motrin) hurts your stomach lining and makes Warfarin's blood-thinning effect much stronger.",
        "what_to_do": "Avoid Ibuprofen completely while on blood thinners. Ask your doctor if Tylenol (Acetaminophen) is safe for your pain instead."
    },
    {
        "drugs": ["lisinopril", "spironolactone"],
        "severity": "HIGH",
        "why_it_happens": "Both pills stop your body from getting rid of potassium.",
        "simple_warning": "Danger! Both pills make potassium build up in your body. Too much potassium can make your heart beat irregularly.",
        "what_to_do": "Have your doctor check your blood potassium levels regularly and avoid salt substitutes made with potassium."
    },
    {
        "drugs": ["lisinopril", "ibuprofen"],
        "severity": "MODERATE",
        "why_it_happens": "Ibuprofen fights against blood pressure pills and makes kidneys work harder.",
        "simple_warning": "Caution: Ibuprofen cancels out the good work of Lisinopril, making your blood pressure go up and stressing your kidneys.",
        "what_to_do": "Try not to take Ibuprofen regularly. Check your blood pressure and tell your doctor if your feet swell."
    },
    {
        "drugs": ["metformin", "ibuprofen"],
        "severity": "MODERATE",
        "why_it_happens": "Frequent pain pills can slow down your kidneys, so metformin stays in your body too long.",
        "simple_warning": "Caution: Taking a lot of Ibuprofen can slow your kidneys down, making it hard to flush out Metformin safely.",
        "what_to_do": "Drink plenty of water and do not take pain pills for more than a few days without asking your doctor."
    },
    {
        "drugs": ["atorvastatin", "clarithromycin"],
        "severity": "HIGH",
        "why_it_happens": "This antibiotic stops your liver from breaking down the cholesterol medicine.",
        "simple_warning": "Warning! This antibiotic lets Atorvastatin build up to high levels, which can cause severe muscle damage.",
        "what_to_do": "Doctors usually pause the cholesterol pill while you are taking this antibiotic."
    }
]

# Foods that mess up how medicines work
FOOD_INTERACTIONS = [
    {
        "medicines": ["atorvastatin", "simvastatin", "amlodipine"],
        "food": "Grapefruit / Grapefruit Juice",
        "simple_warning": "Grapefruit blocks the enzyme that breaks down your medicine. It acts like taking 3 to 5 extra pills at once!",
        "what_to_do": "Do not drink grapefruit juice or eat grapefruit while taking this medicine."
    },
    {
        "medicines": ["warfarin"],
        "food": "Dark Green Vegetables (Spinach, Kale, Broccoli)",
        "simple_warning": "Green leafy vegetables have lots of Vitamin K, which fights against Warfarin and makes it stop working.",
        "what_to_do": "You can still eat greens, but keep the amount about the same every week so your medicine dose stays balanced."
    },
    {
        "medicines": ["lisinopril", "spironolactone", "losartan"],
        "food": "Salt Substitutes (Potassium Salt) & Too Many Bananas",
        "simple_warning": "Many 'low sodium' fake salts use potassium instead. Eating extra potassium with this pill can be dangerous for your heart.",
        "what_to_do": "Read food labels carefully and avoid salt substitutes that contain 'potassium chloride'."
    },
    {
        "medicines": ["metformin"],
        "food": "Alcohol (Heavy Drinking)",
        "simple_warning": "Heavy drinking with Metformin can cause dangerous low blood sugar and build up harmful acid in your blood.",
        "what_to_do": "Avoid binge drinking or having more than one light drink with food."
    }
]

# Health conditions where certain medicines can cause organ damage
ORGAN_WARNINGS = [
    {
        "condition_keywords": ["kidney", "ckd", "renal"],
        "bad_medicines": ["ibuprofen", "naproxen", "aleve", "advil"],
        "organ": "Kidneys",
        "severity": "HIGH",
        "simple_warning": "Your kidneys are already working hard. Ibuprofen reduces blood flow to your kidneys and can damage them further."
    },
    {
        "condition_keywords": ["liver", "cirrhosis", "hepatitis"],
        "bad_medicines": ["acetaminophen", "tylenol", "paracetamol"],
        "organ": "Liver",
        "severity": "HIGH",
        "simple_warning": "Your liver processes Tylenol. Taking too much when you have liver trouble can cause severe liver injury."
    },
    {
        "condition_keywords": ["heart failure", "weak heart"],
        "bad_medicines": ["ibuprofen", "naproxen"],
        "organ": "Heart",
        "severity": "HIGH",
        "simple_warning": "Pain pills like Ibuprofen make your body hold onto extra salt and water, which strains a weak heart."
    }
]

# Easy English guide for each medicine (written so anyone in the family can understand)
MEDICINE_INFO = {
    "metformin": {
        "name": "Metformin (Glucophage)",
        "say_it_like": "met-FOR-min",
        "what_it_does": "It helps your body use its natural insulin so sugar does not build up in your blood.",
        "how_to_take": "Take it with a meal so you do not get an upset stomach.",
        "foods_to_skip": ["Heavy alcohol"],
        "warning_signs": ["Bad stomach cramps with vomiting", "Feeling very cold, weak, or having trouble catching your breath"]
    },
    "lisinopril": {
        "name": "Lisinopril (Zestril / Prinivil)",
        "say_it_like": "lye-SIN-oh-pril",
        "what_it_does": "It relaxes your blood vessels like unkinking a garden hose, so your heart does not have to pump so hard.",
        "how_to_take": "Take 1 pill each morning with a glass of water.",
        "foods_to_skip": ["Salt substitutes made with potassium (like NoSalt)"],
        "warning_signs": ["Swelling of your lips, tongue, or throat (call 911 right away)", "Feeling super dizzy when standing up", "Dry cough that won't go away"]
    },
    "atorvastatin": {
        "name": "Atorvastatin (Lipitor)",
        "say_it_like": "a-TOR-va-stat-in",
        "what_it_does": "It slows down the cholesterol factory in your liver to keep your heart arteries clean and open.",
        "how_to_take": "Take once a day, usually in the evening with dinner or at bedtime.",
        "foods_to_skip": ["Grapefruit and grapefruit juice"],
        "warning_signs": ["Unexplained muscle aches or pain that feels like you ran a marathon", "Dark brown urine"]
    },
    "warfarin": {
        "name": "Warfarin (Coumadin)",
        "say_it_like": "WAR-far-in",
        "what_it_does": "It thins your blood so dangerous blood clots don't form in your legs, heart, or lungs.",
        "how_to_take": "Take at the exact same time every evening. Keep your diet of green veggies steady.",
        "foods_to_skip": ["Sudden huge changes in green salads/spinach", "Cranberry juice in large amounts"],
        "warning_signs": ["Bleeding that won't stop after pressing for 10 minutes", "Black or bloody stool", "Huge unexplained purple bruises"]
    },
    "ibuprofen": {
        "name": "Ibuprofen (Advil / Motrin)",
        "say_it_like": "eye-byoo-PRO-fen",
        "what_it_does": "It brings down swelling, cools fevers, and helps ease joint or muscle aches.",
        "how_to_take": "Always take with food or milk. Do not take it every day for more than a week without asking a doctor.",
        "foods_to_skip": ["Alcohol (makes stomach ulcers much more likely)"],
        "warning_signs": ["Burning stomach ache", "Throwing up something that looks like coffee grounds"]
    },
    "spironolactone": {
        "name": "Spironolactone (Aldactone)",
        "say_it_like": "speer-ON-oh-LAK-tone",
        "what_it_does": "It is a water pill that helps your body pee out extra salt and water while keeping healthy potassium.",
        "how_to_take": "Take it in the morning so you don't have to get up at night to use the bathroom.",
        "foods_to_skip": ["Potassium salt substitutes"],
        "warning_signs": ["Muscle weakness or tingling", "Heart feeling like it is fluttering"]
    },
    "aspirin": {
        "name": "Aspirin (Bayer / Baby Aspirin)",
        "say_it_like": "ASS-per-in",
        "what_it_does": "It stops tiny blood parts called platelets from sticking together, protecting against heart attacks.",
        "how_to_take": "Take once a day with a glass of water and food.",
        "foods_to_skip": ["Alcohol"],
        "warning_signs": ["Easy bruising", "Ringing in your ears", "Stomach pain"]
    }
}
