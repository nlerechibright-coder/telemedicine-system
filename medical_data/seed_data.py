"""
Seed data for the medical_data app.

This module contains the initial dataset of symptoms, conditions, and
condition-symptom rules used to populate the database for demonstration.

To expand the dataset, simply append new dictionaries to the lists below.
The seed_medical_data management command will pick them up automatically.

NOTE: This data is for demonstration/educational purposes only and does not
represent clinically validated medical rules.
"""

# =============================================================================
# SYMPTOMS
# =============================================================================
# Each symptom has: name, description, is_red_flag, emergency_message
# Red-flag symptoms MUST have a non-empty emergency_message.

SYMPTOMS = [
    # --- Red Flag / Emergency Symptoms ---
    {
        'name': 'Severe chest pain',
        'description': 'Intense pain or pressure in the chest, possibly radiating to arms, neck, or jaw.',
        'is_red_flag': True,
        'emergency_message': 'Severe chest pain can indicate a heart attack or other life-threatening condition. Call emergency services immediately.',
    },
    {
        'name': 'Sudden severe headache',
        'description': 'An extremely intense headache that appears suddenly, often described as the worst headache of my life.',
        'is_red_flag': True,
        'emergency_message': 'A sudden severe headache could indicate a stroke or brain hemorrhage. Seek emergency medical care immediately.',
    },
    {
        'name': 'Severe difficulty breathing',
        'description': 'Inability to breathe properly, gasping for air, or feeling of suffocation.',
        'is_red_flag': True,
        'emergency_message': 'Severe difficulty breathing is a medical emergency. Call emergency services or go to the nearest hospital immediately.',
    },
    {
        'name': 'Loss of consciousness',
        'description': 'Fainting or complete loss of awareness.',
        'is_red_flag': True,
        'emergency_message': 'Loss of consciousness requires immediate emergency medical attention. Call emergency services.',
    },
    {
        'name': 'Severe uncontrolled bleeding',
        'description': 'Heavy bleeding that does not stop with direct pressure.',
        'is_red_flag': True,
        'emergency_message': 'Uncontrolled bleeding is a medical emergency. Apply direct pressure and seek emergency care immediately.',
    },
    {
        'name': 'Thoughts of self-harm',
        'description': 'Thoughts of hurting oneself or ending ones life.',
        'is_red_flag': True,
        'emergency_message': 'If you are having thoughts of self-harm, please reach out for help immediately. Contact a crisis helpline or go to the nearest emergency room.',
    },
    {
        'name': 'Sudden confusion or disorientation',
        'description': 'Abrupt inability to think clearly, recognize people or places, or speak coherently.',
        'is_red_flag': True,
        'emergency_message': 'Sudden confusion may indicate a stroke or other serious neurological emergency. Seek immediate medical care.',
    },
    {
        'name': 'High fever with stiff neck',
        'description': 'High temperature combined with inability to bend the neck forward.',
        'is_red_flag': True,
        'emergency_message': 'High fever with a stiff neck may indicate meningitis. Seek emergency medical care immediately.',
    },
    {
        'name': 'Seizures',
        'description': 'Uncontrolled electrical disturbance in the brain causing changes in behavior, movements, or consciousness.',
        'is_red_flag': True,
        'emergency_message': 'Seizures require immediate medical attention. If this is a first-time seizure or lasts more than 5 minutes, call emergency services.',
    },
    {
        'name': 'Severe abdominal pain',
        'description': 'Intense pain in the abdomen that is sudden and severe.',
        'is_red_flag': True,
        'emergency_message': 'Severe abdominal pain may indicate a surgical emergency such as appendicitis. Seek immediate medical care.',
    },

    # --- General Symptoms ---
    {
        'name': 'Fever',
        'description': 'Elevated body temperature above the normal range.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Headache',
        'description': 'Pain in the head or upper neck.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Fatigue',
        'description': 'Persistent tiredness or exhaustion not relieved by rest.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Weakness',
        'description': 'Lack of physical strength or energy.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Body aches',
        'description': 'Generalized muscle pain and discomfort.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Chills',
        'description': 'Feeling of coldness often accompanied by shivering.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Sweating',
        'description': 'Excessive perspiration.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Loss of appetite',
        'description': 'Reduced desire to eat.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Weight loss',
        'description': 'Unintentional decrease in body weight.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Weight gain',
        'description': 'Unintentional increase in body weight.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Respiratory Symptoms ---
    {
        'name': 'Cough',
        'description': 'Sudden expulsion of air from the lungs.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Sore throat',
        'description': 'Pain or irritation in the throat.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Runny nose',
        'description': 'Excessive nasal discharge.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Nasal congestion',
        'description': 'Stuffy or blocked nose.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Sneezing',
        'description': 'Sudden involuntary expulsion of air through the nose.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Shortness of breath',
        'description': 'Difficulty breathing or feeling out of breath.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Wheezing',
        'description': 'High-pitched whistling sound when breathing.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Chest tightness',
        'description': 'Feeling of constriction or pressure in the chest.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Gastrointestinal Symptoms ---
    {
        'name': 'Nausea',
        'description': 'Feeling of sickness with an urge to vomit.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Vomiting',
        'description': 'Forceful expulsion of stomach contents through the mouth.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Diarrhea',
        'description': 'Frequent loose or watery bowel movements.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Abdominal pain',
        'description': 'Pain felt in the belly area.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Bloating',
        'description': 'Feeling of fullness and swelling in the abdomen.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Constipation',
        'description': 'Infrequent or difficult bowel movements.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Heartburn',
        'description': 'Burning sensation in the chest, usually after eating.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Acid reflux',
        'description': 'Backflow of stomach acid into the esophagus.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Neurological Symptoms ---
    {
        'name': 'Dizziness',
        'description': 'Feeling lightheaded or unsteady.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Numbness',
        'description': 'Loss of sensation in a body part.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Tingling',
        'description': 'Pins-and-needles sensation.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Blurred vision',
        'description': 'Lack of sharpness of vision.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Memory problems',
        'description': 'Difficulty remembering things.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Tremors',
        'description': 'Involuntary shaking of a body part.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Musculoskeletal Symptoms ---
    {
        'name': 'Joint pain',
        'description': 'Discomfort or ache in a joint.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Back pain',
        'description': 'Pain felt in the back.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Muscle pain',
        'description': 'Pain in the muscles.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Joint stiffness',
        'description': 'Reduced ability to move a joint freely.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Swelling',
        'description': 'Enlargement of a body part due to fluid accumulation.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Skin Symptoms ---
    {
        'name': 'Skin rash',
        'description': 'Visible change in skin texture or color.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Itching',
        'description': 'Uncomfortable sensation causing the desire to scratch.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Skin redness',
        'description': 'Red or inflamed appearance of the skin.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Bruising',
        'description': 'Discoloration of the skin due to bleeding underneath.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Dry skin',
        'description': 'Skin lacking normal moisture.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Urinary Symptoms ---
    {
        'name': 'Frequent urination',
        'description': 'Need to urinate more often than usual.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Painful urination',
        'description': 'Burning or pain during urination.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Blood in urine',
        'description': 'Presence of blood in the urine.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Dark urine',
        'description': 'Urine that is darker than normal in color.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Mental/Emotional Symptoms ---
    {
        'name': 'Anxiety',
        'description': 'Feeling of worry, nervousness, or unease.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Depressed mood',
        'description': 'Persistent feeling of sadness or loss of interest.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Insomnia',
        'description': 'Difficulty falling or staying asleep.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Irritability',
        'description': 'Easily annoyed or angered.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Mood swings',
        'description': 'Rapid or extreme changes in mood.',
        'is_red_flag': False,
        'emergency_message': '',
    },

    # --- Other Symptoms ---
    {
        'name': 'Increased thirst',
        'description': 'Excessive feeling of needing to drink fluids.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Increased hunger',
        'description': 'Excessive feeling of needing to eat.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Pale skin',
        'description': 'Skin appearing lighter than usual.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Swollen lymph nodes',
        'description': 'Enlarged lymph glands.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Night sweats',
        'description': 'Excessive sweating during sleep.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Palpitations',
        'description': 'Awareness of rapid or irregular heartbeat.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Swollen legs',
        'description': 'Fluid buildup causing swelling in the legs.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Cold hands and feet',
        'description': 'Unusually cold extremities.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Sensitivity to light',
        'description': 'Discomfort or pain in the eyes when exposed to light.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Ear pain',
        'description': 'Pain in the ear.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Hearing loss',
        'description': 'Reduced ability to hear.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Runny or itchy eyes',
        'description': 'Watery, irritated eyes.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Loss of smell',
        'description': 'Reduced or absent ability to smell.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Loss of taste',
        'description': 'Reduced or absent ability to taste.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Muscle cramps',
        'description': 'Sudden involuntary muscle contractions.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Hair loss',
        'description': 'Thinning or loss of hair.',
        'is_red_flag': False,
        'emergency_message': '',
    },
    {
        'name': 'Brittle nails',
        'description': 'Nails that break or chip easily.',
        'is_red_flag': False,
        'emergency_message': '',
    },
]


# =============================================================================
# CONDITIONS
# =============================================================================
# Each condition has: name, description, article_titles (list of KB article titles to try linking)

CONDITIONS = [
    {
        'name': 'Malaria',
        'description': 'A mosquito-borne infectious disease caused by Plasmodium parasites.',
        'article_titles': ['Understanding Malaria', 'Malaria Prevention'],
    },
    {
        'name': 'Influenza',
        'description': 'A contagious respiratory illness caused by influenza viruses.',
        'article_titles': ['Understanding the Flu', 'Flu Prevention'],
    },
    {
        'name': 'Common Cold',
        'description': 'A viral infection of the upper respiratory tract.',
        'article_titles': ['Managing the Common Cold'],
    },
    {
        'name': 'Pneumonia',
        'description': 'An infection that inflames the air sacs in one or both lungs.',
        'article_titles': ['Understanding Pneumonia'],
    },
    {
        'name': 'Typhoid Fever',
        'description': 'A bacterial infection caused by Salmonella typhi.',
        'article_titles': ['Typhoid Fever Basics'],
    },
    {
        'name': 'Dengue Fever',
        'description': 'A mosquito-borne tropical disease causing flu-like symptoms.',
        'article_titles': ['Dengue Fever Guide'],
    },
    {
        'name': 'Gastroenteritis',
        'description': 'Inflammation of the stomach and intestines, usually from infection.',
        'article_titles': ['Managing Gastroenteritis'],
    },
    {
        'name': 'Hypertension',
        'description': 'A condition in which blood pressure is consistently too high.',
        'article_titles': ['Understanding High Blood Pressure'],
    },
    {
        'name': 'Type 2 Diabetes',
        'description': 'A chronic condition affecting how the body processes blood sugar.',
        'article_titles': ['Living with Type 2 Diabetes'],
    },
    {
        'name': 'Asthma',
        'description': 'A condition in which airways narrow, swell, and produce extra mucus.',
        'article_titles': ['Asthma Management'],
    },
    {
        'name': 'Migraine',
        'description': 'A neurological condition causing intense, debilitating headaches.',
        'article_titles': ['Understanding Migraines'],
    },
    {
        'name': 'Tension Headache',
        'description': 'A dull, aching headache often described as a tight band around the head.',
        'article_titles': ['Managing Tension Headaches'],
    },
    {
        'name': 'Gastritis',
        'description': 'Inflammation of the stomach lining.',
        'article_titles': ['Gastritis Overview'],
    },
    {
        'name': 'GERD',
        'description': 'Gastroesophageal reflux disease - chronic acid reflux.',
        'article_titles': ['Understanding GERD'],
    },
    {
        'name': 'Peptic Ulcer',
        'description': 'A sore on the lining of the stomach or small intestine.',
        'article_titles': ['Peptic Ulcer Information'],
    },
    {
        'name': 'Urinary Tract Infection',
        'description': 'An infection in any part of the urinary system.',
        'article_titles': ['UTI Prevention and Treatment'],
    },
    {
        'name': 'Iron Deficiency Anemia',
        'description': 'A condition where blood lacks adequate healthy red blood cells due to insufficient iron.',
        'article_titles': ['Understanding Anemia'],
    },
    {
        'name': 'Allergic Rhinitis',
        'description': 'An allergic response causing sneezing, congestion, and itchy eyes.',
        'article_titles': ['Managing Allergies'],
    },
    {
        'name': 'Depression',
        'description': 'A mood disorder causing persistent feelings of sadness and loss of interest.',
        'article_titles': ['Understanding Depression'],
    },
    {
        'name': 'Generalized Anxiety Disorder',
        'description': 'A condition characterized by excessive, uncontrollable worry.',
        'article_titles': ['Managing Anxiety'],
    },
    {
        'name': 'Insomnia',
        'description': 'A sleep disorder making it hard to fall or stay asleep.',
        'article_titles': ['Improving Sleep'],
    },
    {
        'name': 'Osteoarthritis',
        'description': 'The most common form of arthritis, causing joint pain and stiffness.',
        'article_titles': ['Living with Osteoarthritis'],
    },
    {
        'name': 'Rheumatoid Arthritis',
        'description': 'An autoimmune disorder causing joint inflammation.',
        'article_titles': ['Understanding Rheumatoid Arthritis'],
    },
    {
        'name': 'Hypothyroidism',
        'description': 'A condition where the thyroid gland does not produce enough hormones.',
        'article_titles': ['Thyroid Health'],
    },
    {
        'name': 'Hyperthyroidism',
        'description': 'A condition where the thyroid gland produces too much hormone.',
        'article_titles': ['Thyroid Health'],
    },
    {
        'name': 'Epilepsy',
        'description': 'A neurological disorder characterized by recurrent seizures.',
        'article_titles': ['Understanding Epilepsy'],
    },
    {
        'name': 'Tuberculosis',
        'description': 'A potentially serious infectious bacterial disease affecting the lungs.',
        'article_titles': ['TB Awareness'],
    },
    {
        'name': 'Chickenpox',
        'description': 'A highly contagious viral infection causing an itchy rash.',
        'article_titles': ['Chickenpox Guide'],
    },
    {
        'name': 'Measles',
        'description': 'A highly contagious viral disease causing fever and a distinctive rash.',
        'article_titles': ['Measles Prevention'],
    },
    {
        'name': 'Chronic Kidney Disease',
        'description': 'A long-term condition where the kidneys do not work as well as they should.',
        'article_titles': ['Kidney Health'],
    },
    {
        'name': 'Coronary Artery Disease',
        'description': 'A condition where the heart blood vessels become narrowed or blocked.',
        'article_titles': ['Heart Health'],
    },
    {
        'name': 'Chronic Obstructive Pulmonary Disease',
        'description': 'A group of lung conditions that block airflow and make breathing difficult.',
        'article_titles': ['Understanding COPD'],
    },
]


# =============================================================================
# CONDITION-SYMPTOM RULES
# =============================================================================
# Each rule has: condition_name, symptom_name, weight (1-10), is_core (bool), notes

CONDITION_SYMPTOM_RULES = [
    # --- Malaria ---
    {'condition_name': 'Malaria', 'symptom_name': 'Fever', 'weight': 8, 'is_core': True, 'notes': 'Hallmark symptom'},
    {'condition_name': 'Malaria', 'symptom_name': 'Chills', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Malaria', 'symptom_name': 'Sweating', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Malaria', 'symptom_name': 'Headache', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Malaria', 'symptom_name': 'Body aches', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Malaria', 'symptom_name': 'Fatigue', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Malaria', 'symptom_name': 'Nausea', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Malaria', 'symptom_name': 'Vomiting', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Influenza ---
    {'condition_name': 'Influenza', 'symptom_name': 'Fever', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Influenza', 'symptom_name': 'Body aches', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Influenza', 'symptom_name': 'Fatigue', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Influenza', 'symptom_name': 'Cough', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Influenza', 'symptom_name': 'Sore throat', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Influenza', 'symptom_name': 'Headache', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Influenza', 'symptom_name': 'Chills', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Influenza', 'symptom_name': 'Runny nose', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Common Cold ---
    {'condition_name': 'Common Cold', 'symptom_name': 'Runny nose', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Common Cold', 'symptom_name': 'Nasal congestion', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Common Cold', 'symptom_name': 'Sore throat', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Common Cold', 'symptom_name': 'Sneezing', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Common Cold', 'symptom_name': 'Cough', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Common Cold', 'symptom_name': 'Headache', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Common Cold', 'symptom_name': 'Fatigue', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Pneumonia ---
    {'condition_name': 'Pneumonia', 'symptom_name': 'Cough', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Pneumonia', 'symptom_name': 'Fever', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Pneumonia', 'symptom_name': 'Shortness of breath', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Pneumonia', 'symptom_name': 'Chest tightness', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Pneumonia', 'symptom_name': 'Fatigue', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Pneumonia', 'symptom_name': 'Sweating', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Pneumonia', 'symptom_name': 'Chills', 'weight': 5, 'is_core': False, 'notes': ''},

    # --- Typhoid Fever ---
    {'condition_name': 'Typhoid Fever', 'symptom_name': 'Fever', 'weight': 9, 'is_core': True, 'notes': 'Prolonged high fever'},
    {'condition_name': 'Typhoid Fever', 'symptom_name': 'Headache', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Typhoid Fever', 'symptom_name': 'Abdominal pain', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Typhoid Fever', 'symptom_name': 'Weakness', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Typhoid Fever', 'symptom_name': 'Loss of appetite', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Typhoid Fever', 'symptom_name': 'Diarrhea', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Typhoid Fever', 'symptom_name': 'Constipation', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Dengue Fever ---
    {'condition_name': 'Dengue Fever', 'symptom_name': 'Fever', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'Dengue Fever', 'symptom_name': 'Headache', 'weight': 7, 'is_core': True, 'notes': 'Often behind eyes'},
    {'condition_name': 'Dengue Fever', 'symptom_name': 'Body aches', 'weight': 7, 'is_core': True, 'notes': 'Breakbone fever'},
    {'condition_name': 'Dengue Fever', 'symptom_name': 'Skin rash', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Dengue Fever', 'symptom_name': 'Nausea', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Dengue Fever', 'symptom_name': 'Fatigue', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Dengue Fever', 'symptom_name': 'Bruising', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Gastroenteritis ---
    {'condition_name': 'Gastroenteritis', 'symptom_name': 'Diarrhea', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'Gastroenteritis', 'symptom_name': 'Vomiting', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Gastroenteritis', 'symptom_name': 'Nausea', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Gastroenteritis', 'symptom_name': 'Abdominal pain', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Gastroenteritis', 'symptom_name': 'Fever', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Gastroenteritis', 'symptom_name': 'Bloating', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Hypertension ---
    {'condition_name': 'Hypertension', 'symptom_name': 'Headache', 'weight': 4, 'is_core': False, 'notes': 'Often asymptomatic'},
    {'condition_name': 'Hypertension', 'symptom_name': 'Dizziness', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Hypertension', 'symptom_name': 'Blurred vision', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Hypertension', 'symptom_name': 'Chest tightness', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Hypertension', 'symptom_name': 'Fatigue', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Type 2 Diabetes ---
    {'condition_name': 'Type 2 Diabetes', 'symptom_name': 'Increased thirst', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Type 2 Diabetes', 'symptom_name': 'Frequent urination', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Type 2 Diabetes', 'symptom_name': 'Increased hunger', 'weight': 5, 'is_core': True, 'notes': ''},
    {'condition_name': 'Type 2 Diabetes', 'symptom_name': 'Fatigue', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Type 2 Diabetes', 'symptom_name': 'Blurred vision', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Type 2 Diabetes', 'symptom_name': 'Weight loss', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Type 2 Diabetes', 'symptom_name': 'Tingling', 'weight': 3, 'is_core': False, 'notes': 'Neuropathy'},

    # --- Asthma ---
    {'condition_name': 'Asthma', 'symptom_name': 'Wheezing', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Asthma', 'symptom_name': 'Shortness of breath', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Asthma', 'symptom_name': 'Chest tightness', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Asthma', 'symptom_name': 'Cough', 'weight': 6, 'is_core': True, 'notes': 'Especially at night'},

    # --- Migraine ---
    {'condition_name': 'Migraine', 'symptom_name': 'Headache', 'weight': 9, 'is_core': True, 'notes': 'Severe, one-sided'},
    {'condition_name': 'Migraine', 'symptom_name': 'Nausea', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Migraine', 'symptom_name': 'Sensitivity to light', 'weight': 7, 'is_core': True, 'notes': 'Photophobia'},
    {'condition_name': 'Migraine', 'symptom_name': 'Blurred vision', 'weight': 4, 'is_core': False, 'notes': 'Aura'},
    {'condition_name': 'Migraine', 'symptom_name': 'Vomiting', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Tension Headache ---
    {'condition_name': 'Tension Headache', 'symptom_name': 'Headache', 'weight': 9, 'is_core': True, 'notes': 'Band-like'},
    {'condition_name': 'Tension Headache', 'symptom_name': 'Fatigue', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Tension Headache', 'symptom_name': 'Irritability', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Gastritis ---
    {'condition_name': 'Gastritis', 'symptom_name': 'Abdominal pain', 'weight': 7, 'is_core': True, 'notes': 'Upper abdomen'},
    {'condition_name': 'Gastritis', 'symptom_name': 'Nausea', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Gastritis', 'symptom_name': 'Bloating', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Gastritis', 'symptom_name': 'Loss of appetite', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Gastritis', 'symptom_name': 'Vomiting', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- GERD ---
    {'condition_name': 'GERD', 'symptom_name': 'Heartburn', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'GERD', 'symptom_name': 'Acid reflux', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'GERD', 'symptom_name': 'Chest tightness', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'GERD', 'symptom_name': 'Nausea', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'GERD', 'symptom_name': 'Bloating', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Peptic Ulcer ---
    {'condition_name': 'Peptic Ulcer', 'symptom_name': 'Abdominal pain', 'weight': 8, 'is_core': True, 'notes': 'Burning pain'},
    {'condition_name': 'Peptic Ulcer', 'symptom_name': 'Heartburn', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Peptic Ulcer', 'symptom_name': 'Nausea', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Peptic Ulcer', 'symptom_name': 'Bloating', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Peptic Ulcer', 'symptom_name': 'Loss of appetite', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Urinary Tract Infection ---
    {'condition_name': 'Urinary Tract Infection', 'symptom_name': 'Painful urination', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'Urinary Tract Infection', 'symptom_name': 'Frequent urination', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Urinary Tract Infection', 'symptom_name': 'Abdominal pain', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Urinary Tract Infection', 'symptom_name': 'Fever', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Urinary Tract Infection', 'symptom_name': 'Blood in urine', 'weight': 5, 'is_core': False, 'notes': ''},

    # --- Iron Deficiency Anemia ---
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Fatigue', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Weakness', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Pale skin', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Shortness of breath', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Dizziness', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Cold hands and feet', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Brittle nails', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Iron Deficiency Anemia', 'symptom_name': 'Hair loss', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Allergic Rhinitis ---
    {'condition_name': 'Allergic Rhinitis', 'symptom_name': 'Sneezing', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Allergic Rhinitis', 'symptom_name': 'Runny nose', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Allergic Rhinitis', 'symptom_name': 'Nasal congestion', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Allergic Rhinitis', 'symptom_name': 'Runny or itchy eyes', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Allergic Rhinitis', 'symptom_name': 'Itching', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Depression ---
    {'condition_name': 'Depression', 'symptom_name': 'Depressed mood', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'Depression', 'symptom_name': 'Fatigue', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Depression', 'symptom_name': 'Insomnia', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Depression', 'symptom_name': 'Loss of appetite', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Depression', 'symptom_name': 'Weight loss', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Depression', 'symptom_name': 'Weight gain', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Depression', 'symptom_name': 'Memory problems', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Generalized Anxiety Disorder ---
    {'condition_name': 'Generalized Anxiety Disorder', 'symptom_name': 'Anxiety', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'Generalized Anxiety Disorder', 'symptom_name': 'Insomnia', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Generalized Anxiety Disorder', 'symptom_name': 'Irritability', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Generalized Anxiety Disorder', 'symptom_name': 'Fatigue', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Generalized Anxiety Disorder', 'symptom_name': 'Muscle pain', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Generalized Anxiety Disorder', 'symptom_name': 'Palpitations', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Insomnia ---
    {'condition_name': 'Insomnia', 'symptom_name': 'Insomnia', 'weight': 10, 'is_core': True, 'notes': ''},
    {'condition_name': 'Insomnia', 'symptom_name': 'Fatigue', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Insomnia', 'symptom_name': 'Irritability', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Insomnia', 'symptom_name': 'Memory problems', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Osteoarthritis ---
    {'condition_name': 'Osteoarthritis', 'symptom_name': 'Joint pain', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'Osteoarthritis', 'symptom_name': 'Joint stiffness', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Osteoarthritis', 'symptom_name': 'Swelling', 'weight': 5, 'is_core': False, 'notes': ''},

    # --- Rheumatoid Arthritis ---
    {'condition_name': 'Rheumatoid Arthritis', 'symptom_name': 'Joint pain', 'weight': 9, 'is_core': True, 'notes': 'Symmetrical'},
    {'condition_name': 'Rheumatoid Arthritis', 'symptom_name': 'Joint stiffness', 'weight': 8, 'is_core': True, 'notes': 'Morning stiffness'},
    {'condition_name': 'Rheumatoid Arthritis', 'symptom_name': 'Swelling', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Rheumatoid Arthritis', 'symptom_name': 'Fatigue', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Rheumatoid Arthritis', 'symptom_name': 'Fever', 'weight': 3, 'is_core': False, 'notes': 'Low-grade'},

    # --- Hypothyroidism ---
    {'condition_name': 'Hypothyroidism', 'symptom_name': 'Fatigue', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Hypothyroidism', 'symptom_name': 'Weight gain', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Hypothyroidism', 'symptom_name': 'Cold hands and feet', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Hypothyroidism', 'symptom_name': 'Dry skin', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Hypothyroidism', 'symptom_name': 'Hair loss', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Hypothyroidism', 'symptom_name': 'Constipation', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Hypothyroidism', 'symptom_name': 'Depressed mood', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Hyperthyroidism ---
    {'condition_name': 'Hyperthyroidism', 'symptom_name': 'Weight loss', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Hyperthyroidism', 'symptom_name': 'Palpitations', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Hyperthyroidism', 'symptom_name': 'Anxiety', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Hyperthyroidism', 'symptom_name': 'Sweating', 'weight': 6, 'is_core': True, 'notes': ''},
    {'condition_name': 'Hyperthyroidism', 'symptom_name': 'Irritability', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Hyperthyroidism', 'symptom_name': 'Tremors', 'weight': 5, 'is_core': False, 'notes': ''},

    # --- Epilepsy ---
    {'condition_name': 'Epilepsy', 'symptom_name': 'Seizures', 'weight': 10, 'is_core': True, 'notes': ''},
    {'condition_name': 'Epilepsy', 'symptom_name': 'Memory problems', 'weight': 3, 'is_core': False, 'notes': ''},
    {'condition_name': 'Epilepsy', 'symptom_name': 'Headache', 'weight': 3, 'is_core': False, 'notes': 'Post-ictal'},

    # --- Tuberculosis ---
    {'condition_name': 'Tuberculosis', 'symptom_name': 'Cough', 'weight': 9, 'is_core': True, 'notes': 'Persistent over 3 weeks'},
    {'condition_name': 'Tuberculosis', 'symptom_name': 'Night sweats', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Tuberculosis', 'symptom_name': 'Weight loss', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Tuberculosis', 'symptom_name': 'Fever', 'weight': 6, 'is_core': False, 'notes': 'Low-grade'},
    {'condition_name': 'Tuberculosis', 'symptom_name': 'Fatigue', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Tuberculosis', 'symptom_name': 'Chest tightness', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Chickenpox ---
    {'condition_name': 'Chickenpox', 'symptom_name': 'Skin rash', 'weight': 9, 'is_core': True, 'notes': 'Itchy blisters'},
    {'condition_name': 'Chickenpox', 'symptom_name': 'Itching', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Chickenpox', 'symptom_name': 'Fever', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Chickenpox', 'symptom_name': 'Fatigue', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Chickenpox', 'symptom_name': 'Loss of appetite', 'weight': 3, 'is_core': False, 'notes': ''},

    # --- Measles ---
    {'condition_name': 'Measles', 'symptom_name': 'Fever', 'weight': 8, 'is_core': True, 'notes': ''},
    {'condition_name': 'Measles', 'symptom_name': 'Skin rash', 'weight': 9, 'is_core': True, 'notes': 'Distinctive pattern'},
    {'condition_name': 'Measles', 'symptom_name': 'Cough', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Measles', 'symptom_name': 'Runny nose', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Measles', 'symptom_name': 'Runny or itchy eyes', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Measles', 'symptom_name': 'Sensitivity to light', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Chronic Kidney Disease ---
    {'condition_name': 'Chronic Kidney Disease', 'symptom_name': 'Fatigue', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Chronic Kidney Disease', 'symptom_name': 'Swollen legs', 'weight': 7, 'is_core': True, 'notes': ''},
    {'condition_name': 'Chronic Kidney Disease', 'symptom_name': 'Frequent urination', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Chronic Kidney Disease', 'symptom_name': 'Nausea', 'weight': 4, 'is_core': False, 'notes': ''},
    {'condition_name': 'Chronic Kidney Disease', 'symptom_name': 'Loss of appetite', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- Coronary Artery Disease ---
    {'condition_name': 'Coronary Artery Disease', 'symptom_name': 'Chest tightness', 'weight': 8, 'is_core': True, 'notes': 'Angina'},
    {'condition_name': 'Coronary Artery Disease', 'symptom_name': 'Shortness of breath', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Coronary Artery Disease', 'symptom_name': 'Fatigue', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Coronary Artery Disease', 'symptom_name': 'Palpitations', 'weight': 4, 'is_core': False, 'notes': ''},

    # --- COPD ---
    {'condition_name': 'Chronic Obstructive Pulmonary Disease', 'symptom_name': 'Shortness of breath', 'weight': 9, 'is_core': True, 'notes': ''},
    {'condition_name': 'Chronic Obstructive Pulmonary Disease', 'symptom_name': 'Cough', 'weight': 8, 'is_core': True, 'notes': 'Chronic'},
    {'condition_name': 'Chronic Obstructive Pulmonary Disease', 'symptom_name': 'Wheezing', 'weight': 6, 'is_core': False, 'notes': ''},
    {'condition_name': 'Chronic Obstructive Pulmonary Disease', 'symptom_name': 'Chest tightness', 'weight': 5, 'is_core': False, 'notes': ''},
    {'condition_name': 'Chronic Obstructive Pulmonary Disease', 'symptom_name': 'Fatigue', 'weight': 4, 'is_core': False, 'notes': ''},
]