import json

data = json.load(open(r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_2.json", "r", encoding="utf-8"))

analogies = {
    "3m_q11": "Think of cooking a meal. If you start with fresh, pre-washed, and organized ingredients (good data fetching), cooking (model training) is fast and the dish (model) turns out great. If you have to dig for rotting vegetables (bad data), it ruins the whole meal.",
    "3m_q12": "Supervised is learning with a teacher giving answers. Unsupervised is organizing a messy room without instructions. Semi-supervised is having a teacher grade only a few assignments. Reinforcement is learning to ride a bike by falling (punishment) and balancing (reward).",
    "3m_q13": "It's like checking the nutrition label on a snack before buying it. You quickly glance at calories and sugar (mean, max) to get a general idea of what you are dealing with before eating it.",
    "3m_q14": "You wouldn't put crude, unrefined oil straight into a sports car's gas tank. The engine (algorithm) will choke. It needs to be processed into clean gasoline first.",
    "3m_q15": "Think of predicting a taxi fare. The intercept (beta 0) is the base starting fee you pay just for getting in, the slope (beta 1) is the rate per mile, and the error accounts for unexpected traffic delays.",
    "3m_q16": "Pricing a house based on multiple factors. Instead of just looking at square footage (one variable), you also factor in the number of bedrooms, age of the house, and location to get a much more accurate price.",
    "3m_q17": "Throwing a dart at a dartboard. The residual error is simply the distance between where your dart actually landed (actual value) and the bullseye you were aiming for (predicted value).",
    "3m_q18": "Imagine trying to lay a straight wooden board over a bumpy road. OLS shifts the board around until the total gaps between the board and the bumps are as small as possible.",
    "3m_q19": "Think of MSE as a strict coach grading your target practice. Missing by a little is fine, but missing by a lot gets you heavily penalized (squared) so you quickly learn to avoid huge mistakes.",
    "3m_q20": "Imagine being blindfolded on a foggy mountain and trying to get to the bottom. You feel the slope with your feet (calculate gradient) and take a step downwards, repeating until you hit the flat valley (minimum cost).",
    "3m_q21": "It's like adjusting the stride of your steps while walking down the mountain. Too large (high rate), you leap over the valley and get lost; too small (low rate), you take baby steps and take forever to reach the bottom.",
    "3m_q22": "Trying to fit a straight, rigid ruler onto a curved snake won't work well. Polynomial regression swaps the rigid ruler for a flexible tape measure that can bend and perfectly trace the snake's curves.",
    "3m_q23": "It's like baking a cake. You might transform the flour by sifting it (squaring the variable), but you still just add the ingredients together linearly. The mixing process (the model equation) is still simple addition.",
    "3m_q24": "Overfitting is like memorizing an exam's exact answer key instead of learning the actual subject. You will score 100% on that specific test, but fail completely if the teacher changes the questions slightly.",
    "3m_q25": "Underfitting is like studying for an advanced calculus exam by only reviewing basic addition. You haven't learned enough complexity to handle the subject, so you perform poorly on both practice tests and the real exam.",
    "3m_q26": "It's like adjusting your shower temperature. Bias is when the water is entirely too cold (too simple), and Variance is when it abruptly swings between freezing and scalding (too sensitive). You want the sweet spot right in the middle.",
    "3m_q27": "Think of it as a speed limit for your model. It prevents the model from racing out of control (over-complicating its weights) and forces it to drive smoothly and safely, making it more reliable overall.",
    "3m_q28": "Imagine packing a heavy suitcase. Ridge (L2) forces you to pack a little less of everything to save weight. Lasso (L1) forces you to completely throw away the least important items (zeroing out weights).",
    "3m_q29": "Lasso is like a strict budget manager. Instead of slightly reducing spending across all departments (like Ridge), it completely cuts off funding to the least useful departments, leaving only the essential ones running.",
    "3m_q30": "If you arrive late to work, MAE docks your pay steadily per minute. MSE is a strict boss who docks your pay exponentially more for every extra minute you are late, heavily penalizing huge delays.",
    "3m_q31": "If MSE tells you your error in confusing 'squared dollars', RMSE acts like a translator, square-rooting it back to regular 'dollars' so your boss can actually understand exactly how much money the prediction lost.",
    "3m_q32": "Regular R-squared is a team manager who praises you for adding more team members, even if they do nothing. Adjusted R-squared is the smart boss who only praises you if the new members actually increase the team's productivity.",
    "3m_q33": "It's like a magical funnel. You can dump any massive number (positive or negative) into the top, and it elegantly squishes it down so only a neat, manageable percentage between 0 and 1 comes out the bottom.",
    "3m_q34": "It's like a bouncer at a club using a height threshold. If you are 5'10\" or taller (probability >= 0.5), you go to the VIP room (class 1). If you are shorter, you stay in the main room (class 0).",
    "3m_q35": "Using MSE for classification is like trying to roll a bowling ball down a bumpy hill; it will get stuck in random ditches (local minima). Log-loss smooths the hill into a perfect bowl, ensuring the ball always reaches the bottom.",
    "3m_q36": "Imagine moving to a new city and asking the 5 closest neighbors if the area is safe. If 4 say 'yes' and 1 says 'no', you go with the majority vote and assume it is safe.",
    "3m_q37": "Euclidean distance is simply flying a drone in a perfectly straight line from your house to your neighbor's house. It measures the most direct, 'as the crow flies' path to find out who actually lives closest to you.",
    "3m_q38": "If you only ask 1 neighbor for advice (K=1), you might get a crazy person (overfitting). If you ask the entire state (large K), you lose local context (underfitting). You need to ask just the right neighborhood size.",
    "3m_q39": "Entropy is like measuring the messiness of a toy box. If the box only contains red legos, the messiness (entropy) is zero. If it contains a chaotic mix of cars, dolls, and blocks, the entropy is very high.",
    "3m_q40": "Information Gain is like asking the best possible 'Yes/No' question in a game of Guess Who. Asking 'Are they wearing glasses?' eliminates half the board, giving you maximum information gain and reducing uncertainty the fastest.",
    "3m_q41": "Both are used to measure the messiness of a room. Entropy is like using a complex mathematical formula to measure it perfectly, while Gini Impurity is a quick visual estimate that's almost as accurate but much faster to compute."
}

template = '<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip for Understanding:</strong> {analogy}</div>'

for item in data:
    q_id = item["id"]
    if q_id in analogies:
        item["answer_html"] = item["answer_html"] + template.format(analogy=analogies[q_id])

with open(r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_2_with_tips.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Done")
