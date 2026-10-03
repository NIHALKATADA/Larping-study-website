import json

file_path = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_4.json"
output_path = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_4_with_tips.json"

analogies = {
    "num_q3": "Think of a taxi fare: the intercept is the base fare you pay just to get in, and the slope is the charge per mile. Here, the base sales are the 12,000 units, and each thousand rupees in advertising is like traveling an extra mile.",
    "num_q4": "Imagine you are drawing a straight line through a scatter of stars to show their general path. The slope is how steep the path goes up, and the intercept is where it started.",
    "num_q5": "Think of making a recipe that requires multiple ingredients. The design matrix is like a list of how much of each ingredient goes into different batches, and normal equations help find the perfect balance of each ingredient to get the exact taste you want.",
    "num_q6": "Imagine pricing a custom pizza. There is a base price, plus a cost for every topping (rooms) and crust style (parking spaces). You just multiply the amounts and add them up.",
    "num_q7": "Imagine trying to find the weights of two different types of fruits on a scale using multiple mixed measurements. Solving the equations tells you the exact weight of each fruit type.",
    "num_q13": "Imagine carefully hiking down a foggy mountain. You take small steps (learning rate) in the steepest direction downward (gradient) to reach the valley (minimum error).",
    "num_q14": "Think of adjusting the volume on your radio to match a song playing outside. Each iteration is a small twist of the knob, bringing you closer to the perfect volume (minimum loss).",
    "num_q16": "Think of throwing a ball in the air. Instead of a straight line, its path is a curve. A quadratic model is just finding the perfect curved track that matches the ball's path.",
    "num_q28": "Think of throwing darts at a dartboard. MAE is the average distance from the bullseye. MSE squares the distances, penalizing you much more for darts that are completely off the board. RMSE puts that penalty back into normal distance units.",
    "num_u3_q1": "The sigmoid function is like a judge reviewing evidence. The linear score is the raw evidence. If the evidence pushes the probability above 50% (the threshold), the judge rules 'guilty' (class 1).",
    "num_u3_q2": "Think of a weather forecast. If the raw data gives less than a 50% chance of rain, you leave your umbrella at home (Class 0).",
    "num_u3_q3": "Imagine predicting if a student will pass based on study hours and sleep. The model combines these into a single score, converts it to a percentage, and if it's less than 50%, predicts a fail.",
    "num_u3_q4": "Log-loss is like a teacher grading your test not just on whether you got the answer right, but how confident you were. Being highly confident but wrong gives you a massive penalty!",
    "num_u3_q5": "Imagine moving to a new neighborhood and deciding who to vote for based on your 3 closest neighbors. If 2 out of 3 vote a certain way, you vote that way too!",
    "num_u3_q6": "Imagine navigating a city. Euclidean distance is like a bird flying in a straight line between buildings. Manhattan distance is driving a taxi, forced to follow the grid of city streets.",
    "num_u3_q7": "Entropy is like a bag of mixed candies. If the bag has only red candies, there's no surprise (zero entropy). If it's a mix of red and blue, pulling a random candy is a surprise (high entropy).",
    "num_u3_q8": "Information gain is like asking a good '21 Questions' question. A good question splits a confusing group of items into much more predictable, uniform groups, reducing the overall confusion.",
    "num_u3_q9": "Think of Gini impurity like a measure of messiness in two rooms. If you split a messy group into two rooms, the weighted Gini tells you the average messiness of the house, weighted by how big each room is.",
    "num_u3_q10": "Imagine a detective looking for clues. 'Buy now' might point to spam, while 'meeting' points to not spam. Naive Bayes simply multiplies the individual clue probabilities together to make a final decision, ignoring if the clues are related.",
    "num_u3_q11": "An SVM hyperplane is like a fence exactly in the middle of two properties. If you stand on one side (positive score), you're in one yard; if on the other side (negative score), you're in the neighbor's yard.",
    "num_u3_q12": "Think of guessing the weight of a cow at a fair. Instead of asking one expert, you ask three different people and take the average of their guesses for a more reliable answer.",
    "num_u3_q13": "Imagine asking for advice from three friends, but you trust one friend's judgment more than the others. You give their advice more 'weight' when deciding what to do.",
    "num_u3_q14": "Imagine a golf player taking a first big swing towards the hole (initial prediction), and then taking successive, smaller, careful putts (corrections) to finally sink the ball.",
    "num_u3_q15": "A weak classifier is like a student who gets 80% on a test. Their error rate is the 20% they got wrong. Because they did well, they get a strong 'vote' in the final group decision.",
    "num_u3_q16": "Think of a security alarm. Accuracy is how often it's right. Precision is: when it rings, is it actually a burglar? Recall is: when a burglar comes, did it ring?",
    "num_u3_q17": "Imagine testing a medical screening tool. You need to know not just how often it's right overall, but also how many sick people it missed (Recall) and how many healthy people it falsely scared (Precision).",
    "num_u3_q18": "Think of a doctor diagnosing an illness with a flowchart of questions. The evaluation metrics tell you how often the flowchart leads to the correct treatment versus a false alarm or a missed diagnosis.",
    "num_u3_q19": "Comparing models is like interviewing different contractors for a job. You look at their past mistakes (MAE and MSE) and hire the one with the smallest errors."
}

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    qid = item.get("id")
    tip = analogies.get(qid, "This concept represents a fundamental building block in machine learning, helping us bridge theoretical math with real-world predictions.")
    
    html_block = f'\n<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip for Understanding:</strong> {tip}</div>'
    
    item["answer_html"] = item["answer_html"] + html_block

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Done writing to", output_path)
