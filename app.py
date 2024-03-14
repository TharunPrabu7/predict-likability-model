from flask import Flask, request, render_template
import json

# Create flask app
app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("index.html")

with open('likability_score.json', 'r') as f:
    scores = f.read()

likability_scores = json.loads(scores)

with open('coefficients.json', "r") as f:
    coefficients = json.load(f)

def load_intercept():
    with open('intercept_value.txt', 'r') as file:
        return float(file.read())
    
intercept = load_intercept()

def calculate_match_score(coefficients, age, finance, communication, emoint, listeningSkills, looks,
                          fashionSense, fitness, confidence, senseOfHumor, kindness, openMindedness, loyalty,
                          generosity, selflessness, honesty, gender, sexuality, lang):
    
    form_responses = {
        'What is your age?': int(age),
        'Financial status of your partner': int(finance),
        'Communication': int(communication),
        'Emotional Intelligence': int(emoint),
        'Listening Skills': int(listeningSkills),
        'Looks': int(looks),
        'Fashion sense': int(fashionSense),
        'Fitness': int(fitness),
        'Confidence': int(confidence),
        'Sense of Humor': int(senseOfHumor),
        'Kindness': int(kindness),
        'Open-mindedness': int(openMindedness),
        'Loyalty': int(loyalty),
        'Generosity': int(generosity),
        'Selfless': int(selflessness),
        'Honesty': int(honesty),
        'What is your gender?_Male': 1 if gender.lower() == 'male' else 0,
        'What is your gender?_Female': 1 if gender.lower() == 'female' else 0, 
        'What is your sexuality?_Others': 1 if sexuality.lower() == 'others' else 0,
        'What is your sexuality?_Straight as an arrow': 1 if sexuality.lower() == 'straight as an arrow' else 0,
        'language_Hindi': 1 if lang.lower() == 'hindi' else 0,
        'language_Kannada': 1 if lang.lower() == 'kannada' else 0,
        'language_Malayalam': 1 if lang.lower() == 'malayalam' else 0,
        'language_Tamil': 1 if lang.lower() == 'tamil' else 0,
        'language_Telugu': 1 if lang.lower() == 'telugu' else 0,
    }


    # Calculate the match score
    match_score = sum(coefficients[feature] * form_responses[feature] for feature in coefficients) + intercept
    return match_score

def classifier(score):
    if score < 30:
        return 'bad'
    elif score >=30 and score <=50:
        return 'alright'
    elif score > 50 and score <= 70:
        return 'good'
    elif score > 70 and score < 90:
        return 'better'
    else:
        return 'best'
    
def how_much_people_like_you(score):
    count=0
    for i, value in enumerate(likability_scores):
        if score >= value:
            count += 1

    percent = round((count/len(likability_scores)*100),2)          
    return percent


@app.route("/predict", methods=["POST", "GET"])
def predict():
    # Use request.form.to_dict() to convert MultiDict to a regular dictionary
    input_features = request.form.to_dict()

    # Use the form data to calculate the match score
    match_score = int(round(calculate_match_score(coefficients, **input_features),0))

    result = classifier(match_score)

    people_likey = how_much_people_like_you(match_score)

    return render_template("result.html", data=result, 
                           people_percent=f"Out of the people who took the survey you are liked by {people_likey}% of the people.",
                           score="You ability to be liked by other people is {}".format(match_score))


if __name__ == "__main__":
    app.run(debug=True)