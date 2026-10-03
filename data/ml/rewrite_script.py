import json
import os

input_file = r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\part_3.json'
output_file = r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\part_3_final.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Rewriting answer_html for each ID
rewrites = {
    'num_u3_q13': '''<div class='solution-step'>
    <h3>1. Problem Definition and Setup</h3>
    <ul>
        <li><b>Goal:</b> Calculate the final prediction from a weighted ensemble of three regression trees.</li>
        <li><b>Ensemble Learning:</b> A machine learning paradigm where multiple models (often called "weak learners") are trained to solve the same problem and combined to get better results.</li>
        <li><b>Given Data:</b>
            <ul>
                <li>Tree 1 (T1): Prediction = 100, Weight (W1) = 0.2</li>
                <li>Tree 2 (T2): Prediction = 120, Weight (W2) = 0.5</li>
                <li>Tree 3 (T3): Prediction = 110, Weight (W3) = 0.3</li>
            </ul>
        </li>
    </ul>

    <h3>2. Step-by-Step Calculation</h3>
    <ul>
        <li><b>Formula for Weighted Average:</b> The final prediction is the sum of the products of each individual prediction and its corresponding weight.</li>
        <li><b>Equation:</b> Weighted Prediction = (Pred1 &times; W1) + (Pred2 &times; W2) + (Pred3 &times; W3)</li>
        <li><b>Check Weights:</b> Ensure the weights sum to 1.0 (0.2 + 0.5 + 0.3 = 1.0). Since they do, no further normalization is required.</li>
        <li><b>Apply Values:</b>
            <ul>
                <li>Term 1: 100 &times; 0.2 = 20</li>
                <li>Term 2: 120 &times; 0.5 = 60</li>
                <li>Term 3: 110 &times; 0.3 = 33</li>
            </ul>
        </li>
        <li><b>Final Addition:</b> 20 + 60 + 33 = <b>113</b></li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <p><b>Decision Trees &amp; Information Theory:</b> Decision trees sequentially partition the feature space into distinct regions. The objective of these splits is to maximize information gain or minimize impurity metrics, thereby creating child nodes that are as homogeneous as possible regarding the target variable.</p>
    <h4>Key Concepts in Tree Construction:</h4>
    <ul>
        <li><b>Entropy:</b> A rigorous mathematical measure of the randomness, impurity, or unpredictability within a subset of data. Lower entropy indicates a higher degree of purity.</li>
        <li><b>Gini Impurity:</b> A metric quantifying the probability that a randomly chosen element from the set would be incorrectly labeled if it was randomly labeled according to the distribution of labels in the subset. It is computationally more efficient than entropy.</li>
        <li><b>Information Gain:</b> The calculated reduction in entropy that results from partitioning a dataset based on a specific attribute. The split with the highest information gain is selected.</li>
    </ul>
    <h4>Python Implementation Example:</h4>
    <pre><code>from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Initialize the model using entropy as the splitting criterion
model = DecisionTreeClassifier(criterion='entropy', max_depth=3)

# Train the model on the training data
model.fit(X_train, y_train)

# Generate predictions on the testing data
preds = model.predict(X_test)</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of the ensemble prediction like calculating your final grade in a course. Each tree is an assignment (like a quiz, midterm, or final exam), the prediction is your score on that assignment, and the weight is how much that assignment counts toward your final grade. Just multiply each score by its weight and add them up!</div>''',
    
    'num_u3_q14': '''<div class='solution-step'>
    <h3>1. Problem Definition and Setup</h3>
    <ul>
        <li><b>Goal:</b> Calculate the final prediction of a gradient boosting model after three successive rounds of corrections.</li>
        <li><b>Boosting Framework:</b> An additive model where weak learners are added sequentially. Each new model attempts to correct the residual errors made by the previous combined model.</li>
        <li><b>Given Data:</b>
            <ul>
                <li>Initial Prediction: F<sub>0</sub>(x) = 20</li>
                <li>Learner 1 Correction: h<sub>1</sub>(x) = 10</li>
                <li>Learner 2 Correction: h<sub>2</sub>(x) = 6</li>
                <li>Learner 3 Correction: h<sub>3</sub>(x) = 4</li>
                <li>Learning Rate (&alpha;): 0.2 (Scales the contribution of each weak learner to prevent overfitting)</li>
            </ul>
        </li>
    </ul>

    <h3>2. Step-by-Step Calculation</h3>
    <ul>
        <li><b>General Formula:</b> F<sub>m</sub>(x) = F<sub>m-1</sub>(x) + (&alpha; &times; h<sub>m</sub>(x))</li>
        <li><b>Round 1 (m = 1):</b>
            <ul>
                <li>F<sub>1</sub>(x) = F<sub>0</sub>(x) + (0.2 &times; h<sub>1</sub>(x))</li>
                <li>F<sub>1</sub>(x) = 20 + (0.2 &times; 10) = 20 + 2 = 22</li>
            </ul>
        </li>
        <li><b>Round 2 (m = 2):</b>
            <ul>
                <li>F<sub>2</sub>(x) = F<sub>1</sub>(x) + (0.2 &times; h<sub>2</sub>(x))</li>
                <li>F<sub>2</sub>(x) = 22 + (0.2 &times; 6) = 22 + 1.2 = 23.2</li>
            </ul>
        </li>
        <li><b>Round 3 (m = 3):</b>
            <ul>
                <li>F<sub>3</sub>(x) = F<sub>2</sub>(x) + (0.2 &times; h<sub>3</sub>(x))</li>
                <li>F<sub>3</sub>(x) = 23.2 + (0.2 &times; 4) = 23.2 + 0.8 = <b>24.0</b></li>
            </ul>
        </li>
    </ul>
    <p>The final predicted value after three boosting rounds is <b>24.0</b>.</p>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <p><b>Ensemble Methods (Bagging and Boosting):</b> Ensemble techniques integrate the outputs of multiple base models (weak learners) to formulate a single, highly accurate predictive model (strong learner). This process substantially enhances overall predictive performance, stability, and robustness against noisy data.</p>
    <h4>Key Methodologies:</h4>
    <ul>
        <li><b>Bagging (Bootstrap Aggregating):</b> Models (like Decision Trees in a Random Forest) are trained independently and in parallel on randomized subsets of the training data (created via sampling with replacement). Their predictions are averaged (regression) or majority-voted (classification) to primarily reduce model <b>variance</b> and prevent overfitting.</li>
        <li><b>Boosting:</b> Models (like those in AdaBoost or XGBoost) are built sequentially. Each subsequent model is specifically trained to minimize the loss or correct the errors of the preceding ensemble. This approach primarily reduces model <b>bias</b>.</li>
    </ul>
    <h4>Python Implementation Example:</h4>
    <pre><code>from sklearn.ensemble import RandomForestRegressor, AdaBoostClassifier

# Initialize a Bagging-based regressor
rf = RandomForestRegressor(n_estimators=100)

# Train the model
rf.fit(X_train, y_train)

# Generate predictions
pred = rf.predict(X_test)</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of boosting like steering a ship to a destination. The initial prediction is your starting point. Each "weak learner" is a minor course correction from the captain. The "learning rate" is how strongly you turn the wheel for each correction. You add up all these small adjustments step-by-step to arrive exactly at your target!</div>''',
    
    'num_u3_q15': '''<div class='solution-step'>
    <h3>1. Problem Definition and Setup</h3>
    <ul>
        <li><b>Goal:</b> Determine the error rate and the calculated classifier weight for a weak learner in the context of the AdaBoost algorithm.</li>
        <li><b>AdaBoost Mechanism:</b> In Adaptive Boosting, each weak classifier is assigned a weight based on its accuracy. More accurate classifiers have a higher "say" (weight) in the final voting process.</li>
        <li><b>Given Data:</b>
            <ul>
                <li>Total Training Samples (N): 100</li>
                <li>Correctly Classified Samples: 80</li>
                <li>Incorrectly Classified Samples: 20 (Derived as 100 - 80)</li>
            </ul>
        </li>
    </ul>

    <h3>2. Step-by-Step Calculation</h3>
    <ul>
        <li><b>Step 2a: Calculate the Error Rate (&epsilon;)</b>
            <ul>
                <li><b>Definition:</b> The proportion of samples that the classifier got wrong.</li>
                <li><b>Formula:</b> &epsilon; = (Number of Incorrect Predictions) / (Total Number of Samples)</li>
                <li><b>Calculation:</b> &epsilon; = 20 / 100 = <b>0.2</b></li>
            </ul>
        </li>
        <li><b>Step 2b: Calculate the Classifier Weight (&alpha;)</b>
            <ul>
                <li><b>Definition:</b> The influence this classifier will have in the final ensemble.</li>
                <li><b>Formula:</b> &alpha; = 0.5 &times; ln((1 - &epsilon;) / &epsilon;)</li>
                <li><b>Substitution:</b> &alpha; = 0.5 &times; ln((1 - 0.2) / 0.2)</li>
                <li><b>Simplification:</b> &alpha; = 0.5 &times; ln(0.8 / 0.2) = 0.5 &times; ln(4)</li>
                <li><b>Final Value:</b> Since ln(4) &approx; 1.386, &alpha; = 0.5 &times; 1.386 = <b>0.693</b></li>
            </ul>
        </li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <p><b>Evaluation Metrics and Model Assessment:</b> The rigorous evaluation of a machine learning model is as critical as the training phase itself. Selecting the appropriate metric depends fundamentally on the specific characteristics of the dataset (e.g., class imbalance) and the overarching business objective.</p>
    <h4>Key Metrics Categorization:</h4>
    <ul>
        <li><b>Regression Metrics:</b>
            <ul>
                <li><b>Mean Absolute Error (MAE):</b> Provides the average magnitude of errors without considering their direction.</li>
                <li><b>Mean Squared Error (MSE):</b> Squares the errors before averaging, thereby heavily penalizing larger errors.</li>
                <li><b>Root Mean Squared Error (RMSE):</b> The square root of MSE, bringing the metric back to the interpretable units of the original target variable.</li>
            </ul>
        </li>
        <li><b>Classification Metrics:</b>
            <ul>
                <li><b>Accuracy:</b> The ratio of correct predictions to total predictions. Most reliable when classes are perfectly balanced.</li>
                <li><b>Precision and Recall:</b> Vital metrics when the operational costs of False Positives and False Negatives differ significantly.</li>
                <li><b>F1-Score:</b> The harmonic mean of Precision and Recall, providing a single balanced metric.</li>
            </ul>
        </li>
    </ul>
    <h4>Python Implementation Example:</h4>
    <pre><code>from sklearn.metrics import mean_squared_error, classification_report

# Generate a comprehensive report for classification
print('Classification Report:')
print(classification_report(y_true, y_pred))

# Calculate error for regression
mse = mean_squared_error(y_true, y_pred)
print(f'Mean Squared Error: {mse}')</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> The formula for weight (alpha) uses the natural log (ln) of the ratio of "success rate" (1 - error) to "failure rate" (error). If the classifier is doing great (high success, low failure), this ratio is huge, and its voting weight goes up!</div>''',
    
    'num_u3_q16': '''<div class='solution-step'>
    <h3>1. Problem Definition and Setup</h3>
    <ul>
        <li><b>Goal:</b> Evaluate a binary classifier by calculating four standard performance metrics: Accuracy, Precision, Recall, and the F1-score.</li>
        <li><b>Confusion Matrix Components:</b>
            <ul>
                <li>True Positives (TP) = 80: Correctly predicted positive instances.</li>
                <li>True Negatives (TN) = 70: Correctly predicted negative instances.</li>
                <li>False Positives (FP) = 10: Incorrectly predicted positive instances (Type I Error).</li>
                <li>False Negatives (FN) = 20: Incorrectly predicted negative instances (Type II Error).</li>
            </ul>
        </li>
        <li><b>Total Samples (N):</b> TP + TN + FP + FN = 80 + 70 + 10 + 20 = 180</li>
    </ul>

    <h3>2. Step-by-Step Calculation of Metrics</h3>
    <ul>
        <li><b>Accuracy:</b> The overall proportion of correctly classified instances.
            <ul>
                <li><b>Formula:</b> (TP + TN) / Total</li>
                <li><b>Calculation:</b> (80 + 70) / 180 = 150 / 180 &approx; <b>0.833</b> (83.3%)</li>
            </ul>
        </li>
        <li><b>Precision:</b> The proportion of positive predictions that were actually correct. Focuses on minimizing False Positives.
            <ul>
                <li><b>Formula:</b> TP / (TP + FP)</li>
                <li><b>Calculation:</b> 80 / (80 + 10) = 80 / 90 &approx; <b>0.889</b> (88.9%)</li>
            </ul>
        </li>
        <li><b>Recall (Sensitivity or True Positive Rate):</b> The proportion of actual positives that were correctly identified. Focuses on minimizing False Negatives.
            <ul>
                <li><b>Formula:</b> TP / (TP + FN)</li>
                <li><b>Calculation:</b> 80 / (80 + 20) = 80 / 100 = <b>0.800</b> (80.0%)</li>
            </ul>
        </li>
        <li><b>F1-score:</b> The harmonic mean of Precision and Recall. It provides a balanced measure when there is a tradeoff between Precision and Recall.
            <ul>
                <li><b>Formula:</b> 2 &times; (Precision &times; Recall) / (Precision + Recall)</li>
                <li><b>Calculation:</b> 2 &times; (0.889 &times; 0.800) / (0.889 + 0.800)</li>
                <li><b>Simplification:</b> 2 &times; (0.7112) / (1.689) &approx; 1.4224 / 1.689 &approx; <b>0.842</b> (84.2%)</li>
            </ul>
        </li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <p><b>Evaluation Metrics and Model Assessment:</b> The rigorous evaluation of a machine learning model is as critical as the training phase itself. Selecting the appropriate metric depends fundamentally on the specific characteristics of the dataset (e.g., class imbalance) and the overarching business objective.</p>
    <h4>Key Metrics Categorization:</h4>
    <ul>
        <li><b>Regression Metrics:</b>
            <ul>
                <li><b>Mean Absolute Error (MAE):</b> Provides the average magnitude of errors without considering their direction.</li>
                <li><b>Mean Squared Error (MSE):</b> Squares the errors before averaging, thereby heavily penalizing larger errors.</li>
                <li><b>Root Mean Squared Error (RMSE):</b> The square root of MSE, bringing the metric back to the interpretable units of the original target variable.</li>
            </ul>
        </li>
        <li><b>Classification Metrics:</b>
            <ul>
                <li><b>Accuracy:</b> Good for balanced datasets, but misleading if classes are highly imbalanced.</li>
                <li><b>Precision and Recall:</b> Critical when the operational costs of false positives (e.g., spam filtering) or false negatives (e.g., medical diagnosis) differ significantly.</li>
                <li><b>F1-Score:</b> Useful when you need a single metric to compare models and you care equally about precision and recall.</li>
            </ul>
        </li>
    </ul>
    <h4>Python Implementation Example:</h4>
    <pre><code>from sklearn.metrics import mean_squared_error, classification_report

# Generate a comprehensive report for classification
print('Classification Report:')
print(classification_report(y_true, y_pred))

# Calculate error for regression
mse = mean_squared_error(y_true, y_pred)
print(f'Mean Squared Error: {mse}')</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> <ul><li><b>P</b>recision is about the <b>P</b>redictions: Out of all the times the model <i>claimed</i> "Positive," how many were real?</li><li><b>R</b>ecall is about <b>R</b>eality: Out of all the <i>real</i> Positives in the dataset, how many did the model find?</li></ul></div>''',
    
    'num_u3_q17': '''<div class='solution-step'>
    <h3>1. Problem Definition and Class Predictions</h3>
    <ul>
        <li><b>Goal:</b> Evaluate a model's predicted probabilities against actual labels to generate a confusion matrix, standard metrics, and log-loss.</li>
        <li><b>Threshold Rule:</b> If Probability (P) &ge; 0.5, Predicted Class = 1. If P &lt; 0.5, Predicted Class = 0.</li>
        <li><b>Applying the Threshold:</b>
            <ul>
                <li>S1: Actual=1, Prob=0.9 &rarr; Pred=1 (<b>True Positive, TP</b>)</li>
                <li>S2: Actual=0, Prob=0.2 &rarr; Pred=0 (<b>True Negative, TN</b>)</li>
                <li>S3: Actual=1, Prob=0.7 &rarr; Pred=1 (<b>True Positive, TP</b>)</li>
                <li>S4: Actual=0, Prob=0.6 &rarr; Pred=1 (<b>False Positive, FP</b>)</li>
                <li>S5: Actual=1, Prob=0.8 &rarr; Pred=1 (<b>True Positive, TP</b>)</li>
                <li>S6: Actual=0, Prob=0.1 &rarr; Pred=0 (<b>True Negative, TN</b>)</li>
                <li>S7: Actual=1, Prob=0.4 &rarr; Pred=0 (<b>False Negative, FN</b>)</li>
                <li>S8: Actual=0, Prob=0.3 &rarr; Pred=0 (<b>True Negative, TN</b>)</li>
            </ul>
        </li>
    </ul>

    <h3>2. Constructing the Confusion Matrix</h3>
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; margin-bottom: 15px;">
        <tr>
            <th></th>
            <th>Predicted 1 (Positive)</th>
            <th>Predicted 0 (Negative)</th>
        </tr>
        <tr>
            <th>Actual 1 (Positive)</th>
            <td>TP = 3</td>
            <td>FN = 1</td>
        </tr>
        <tr>
            <th>Actual 0 (Negative)</th>
            <td>FP = 1</td>
            <td>TN = 3</td>
        </tr>
    </table>

    <h3>3. Step-by-Step Calculation of Metrics</h3>
    <ul>
        <li><b>Total Samples (N):</b> 8</li>
        <li><b>Accuracy:</b> (TP + TN) / N = (3 + 3) / 8 = 6 / 8 = <b>0.75</b></li>
        <li><b>Precision:</b> TP / (TP + FP) = 3 / (3 + 1) = 3 / 4 = <b>0.75</b></li>
        <li><b>Recall:</b> TP / (TP + FN) = 3 / (3 + 1) = 3 / 4 = <b>0.75</b></li>
        <li><b>F1-score:</b> 2 &times; (Precision &times; Recall) / (Precision + Recall) = 2 &times; (0.75 &times; 0.75) / (0.75 + 0.75) = 2 &times; (0.5625) / 1.5 = <b>0.75</b></li>
    </ul>

    <h3>4. Calculating Log-Loss (Cross-Entropy Loss)</h3>
    <ul>
        <li><b>Log-Loss Formula:</b> -(1/N) &times; &Sigma; [y<sub>i</sub> &times; ln(p<sub>i</sub>) + (1 - y<sub>i</sub>) &times; ln(1 - p<sub>i</sub>)]</li>
        <li><b>Simplified Concept:</b> For Actual 1, we use ln(P). For Actual 0, we use ln(1 - P).</li>
        <li><b>Individual Sample Calculations:</b>
            <ul>
                <li>S1 (y=1): ln(0.9) &approx; -0.105</li>
                <li>S2 (y=0): ln(1 - 0.2) = ln(0.8) &approx; -0.223</li>
                <li>S3 (y=1): ln(0.7) &approx; -0.357</li>
                <li>S4 (y=0): ln(1 - 0.6) = ln(0.4) &approx; -0.916</li>
                <li>S5 (y=1): ln(0.8) &approx; -0.223</li>
                <li>S6 (y=0): ln(1 - 0.1) = ln(0.9) &approx; -0.105</li>
                <li>S7 (y=1): ln(0.4) &approx; -0.916</li>
                <li>S8 (y=0): ln(1 - 0.3) = ln(0.7) &approx; -0.357</li>
            </ul>
        </li>
        <li><b>Summing the Values:</b> -0.105 - 0.223 - 0.357 - 0.916 - 0.223 - 0.105 - 0.916 - 0.357 = -3.202</li>
        <li><b>Final Log-Loss:</b> -(1/8) &times; (-3.202) = <b>0.400</b></li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <p><b>Evaluation Metrics and Model Assessment:</b> The rigorous evaluation of a machine learning model is as critical as the training phase itself. Selecting the appropriate metric depends fundamentally on the specific characteristics of the dataset (e.g., class imbalance) and the overarching business objective.</p>
    <h4>Key Metrics Categorization:</h4>
    <ul>
        <li><b>Log-Loss (Cross-Entropy Loss):</b> Unlike accuracy, which only cares if the final prediction was right or wrong, log-loss evaluates the <i>confidence</i> of the probabilities. It heavily penalizes models that are highly confident but entirely incorrect.</li>
        <li><b>Classification Metrics:</b> Accuracy is good for balanced classes. Precision and Recall are crucial when false positives or false negatives have different costs. F1-score balances the two.</li>
    </ul>
    <h4>Python Implementation Example:</h4>
    <pre><code>from sklearn.metrics import log_loss, classification_report

# Ensure probabilities are used for log-loss, not hard predictions
loss = log_loss(y_true, y_pred_probabilities)
print(f'Log Loss: {loss}')

print('Classification Report:')
print(classification_report(y_true, y_pred_classes))</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> For Log-Loss, remember that it's a measure of "surprise" or "penalty". If a sample is actually a 1, and the model predicts 0.99, it is not surprised (tiny penalty). But if it's actually a 1, and the model confidently predicts 0.01, it is highly surprised, and the logarithmic penalty shoots through the roof!</div>''',
    
    'num_u3_q18': '''<div class='solution-step'>
    <h3>1. Problem Definition and Setup</h3>
    <ul>
        <li><b>Goal:</b> Compute information theory metrics (Entropy, Gini) and classification performance metrics based on a binary outcome.</li>
        <li><b>Given Matrix Data:</b>
            <ul>
                <li>Total Patients (N) = 100</li>
                <li>True Positives (TP) = 35</li>
                <li>True Negatives (TN) = 45</li>
                <li>False Positives (FP) = 10</li>
                <li>False Negatives (FN) = 10</li>
            </ul>
        </li>
        <li><b>Deriving Actual Class Distributions:</b>
            <ul>
                <li><b>Total Actual Positives:</b> TP + FN = 35 + 10 = 45</li>
                <li><b>Total Actual Negatives:</b> TN + FP = 45 + 10 = 55</li>
                <li><b>Probability of Positive Class p(+):</b> 45 / 100 = 0.45</li>
                <li><b>Probability of Negative Class p(-):</b> 55 / 100 = 0.55</li>
            </ul>
        </li>
    </ul>

    <h3>2. Step-by-Step Calculation of Impurity Metrics</h3>
    <ul>
        <li><b>Entropy (H):</b> Measures the unpredictability or impurity of the dataset.
            <ul>
                <li><b>Formula:</b> -[p(+) &times; log<sub>2</sub>(p(+)) + p(-) &times; log<sub>2</sub>(p(-))]</li>
                <li><b>Calculation:</b> -(0.45 &times; log<sub>2</sub>(0.45)) - (0.55 &times; log<sub>2</sub>(0.55))</li>
                <li><b>Simplification:</b> &approx; -(0.45 &times; -1.152) - (0.55 &times; -0.862) &approx; 0.518 + 0.474 = <b>0.992</b></li>
            </ul>
        </li>
        <li><b>Gini Impurity:</b> An alternative to entropy that measures the probability of misclassification.
            <ul>
                <li><b>Formula:</b> 1 - [(p(+))<sup>2</sup> + (p(-))<sup>2</sup>]</li>
                <li><b>Calculation:</b> 1 - [(0.45)<sup>2</sup> + (0.55)<sup>2</sup>]</li>
                <li><b>Simplification:</b> 1 - [0.2025 + 0.3025] = 1 - 0.505 = <b>0.495</b></li>
            </ul>
        </li>
    </ul>

    <h3>3. Step-by-Step Calculation of Classification Metrics</h3>
    <ul>
        <li><b>Accuracy:</b> (TP + TN) / Total = (35 + 45) / 100 = 80 / 100 = <b>0.80</b> (80%)</li>
        <li><b>Precision:</b> TP / (TP + FP) = 35 / (35 + 10) = 35 / 45 &approx; <b>0.778</b> (77.8%)</li>
        <li><b>Recall:</b> TP / (TP + FN) = 35 / (35 + 10) = 35 / 45 &approx; <b>0.778</b> (77.8%)</li>
        <li><b>F1-score:</b> 2 &times; (Precision &times; Recall) / (Precision + Recall) = 2 &times; (0.778 &times; 0.778) / (0.778 + 0.778) &approx; <b>0.778</b></li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <p><b>Decision Trees &amp; Information Theory:</b> Decision trees sequentially partition the feature space into distinct regions. The objective of these splits is to maximize information gain or minimize impurity metrics, thereby creating child nodes that are as homogeneous as possible regarding the target variable.</p>
    <h4>Key Concepts in Tree Construction:</h4>
    <ul>
        <li><b>Entropy:</b> A rigorous mathematical measure of the randomness, impurity, or unpredictability within a subset of data. Lower entropy indicates a higher degree of purity. A 50/50 split yields an entropy of 1.0 (maximum unpredictability).</li>
        <li><b>Gini Impurity:</b> A metric quantifying the probability that a randomly chosen element from the set would be incorrectly labeled. It scales between 0 (perfectly pure) and 0.5 (perfectly impure for binary tasks), making it computationally faster as it avoids logarithmic calculations.</li>
        <li><b>Information Gain:</b> The calculated reduction in entropy that results from partitioning a dataset based on a specific attribute.</li>
    </ul>
    <h4>Python Implementation Example:</h4>
    <pre><code>from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Initialize the model using entropy as the splitting criterion
model = DecisionTreeClassifier(criterion='entropy', max_depth=3)

# Train the model on the training data
model.fit(X_train, y_train)

# Generate predictions on the testing data
preds = model.predict(X_test)</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Gini and Entropy both measure how "mixed up" a dataset is. If a node is 100% one class, both metrics are 0 (perfectly pure). To remember the difference in limits: Gini peaks at 0.5, while Entropy peaks at 1.0!</div>''',
    
    'num_u3_q19': '''<div class='solution-step'>
    <h3>1. Problem Definition and Setup</h3>
    <ul>
        <li><b>Goal:</b> Evaluate three regression models by calculating Mean Absolute Error (MAE) and Mean Squared Error (MSE), and identify the most performant model.</li>
        <li><b>Given Actual Targets:</b> [100, 200, 150, 300]</li>
        <li><b>Given Model Predictions:</b>
            <ul>
                <li>Random Forest (RF): [95, 210, 145, 290]</li>
                <li>Gradient Boosting (GB): [98, 205, 148, 295]</li>
                <li>XGBoost (XGB): [99, 202, 152, 298]</li>
            </ul>
        </li>
    </ul>

    <h3>2. Step-by-Step Calculation for Random Forest (RF)</h3>
    <ul>
        <li><b>Raw Errors (Actual - Prediction):</b> (100 - 95 = 5), (200 - 210 = -10), (150 - 145 = 5), (300 - 290 = 10)</li>
        <li><b>Absolute Errors (For MAE):</b> [5, 10, 5, 10]
            <ul>
                <li><b>MAE:</b> Sum of Absolute Errors / N = (5 + 10 + 5 + 10) / 4 = 30 / 4 = <b>7.5</b></li>
            </ul>
        </li>
        <li><b>Squared Errors (For MSE):</b> [5<sup>2</sup>, (-10)<sup>2</sup>, 5<sup>2</sup>, 10<sup>2</sup>] = [25, 100, 25, 100]
            <ul>
                <li><b>MSE:</b> Sum of Squared Errors / N = (25 + 100 + 25 + 100) / 4 = 250 / 4 = <b>62.5</b></li>
            </ul>
        </li>
    </ul>

    <h3>3. Step-by-Step Calculation for Gradient Boosting (GB)</h3>
    <ul>
        <li><b>Raw Errors:</b> (100 - 98 = 2), (200 - 205 = -5), (150 - 148 = 2), (300 - 295 = 5)</li>
        <li><b>Absolute Errors:</b> [2, 5, 2, 5]
            <ul>
                <li><b>MAE:</b> (2 + 5 + 2 + 5) / 4 = 14 / 4 = <b>3.5</b></li>
            </ul>
        </li>
        <li><b>Squared Errors:</b> [4, 25, 4, 25]
            <ul>
                <li><b>MSE:</b> (4 + 25 + 4 + 25) / 4 = 58 / 4 = <b>14.5</b></li>
            </ul>
        </li>
    </ul>

    <h3>4. Step-by-Step Calculation for XGBoost (XGB)</h3>
    <ul>
        <li><b>Raw Errors:</b> (100 - 99 = 1), (200 - 202 = -2), (150 - 152 = -2), (300 - 298 = 2)</li>
        <li><b>Absolute Errors:</b> [1, 2, 2, 2]
            <ul>
                <li><b>MAE:</b> (1 + 2 + 2 + 2) / 4 = 7 / 4 = <b>1.75</b></li>
            </ul>
        </li>
        <li><b>Squared Errors:</b> [1, 4, 4, 4]
            <ul>
                <li><b>MSE:</b> (1 + 4 + 4 + 4) / 4 = 13 / 4 = <b>3.25</b></li>
            </ul>
        </li>
    </ul>

    <h3>5. Conclusion</h3>
    <p><b>XGBoost</b> demonstrates the most superior predictive performance because it yields the lowest values for both MAE (1.75) and MSE (3.25), indicating its predictions are consistently closer to the true values.</p>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <p><b>Regression Fundamentals &amp; Evaluation:</b> Regression algorithms attempt to model the relationship between input variables and a continuous target variable. Evaluating these models requires metrics that quantify the distance between predicted and actual values.</p>
    <h4>Key Metric Distinctions:</h4>
    <ul>
        <li><b>Mean Absolute Error (MAE):</b> Treats all errors linearly. An error of 10 is penalized exactly twice as much as an error of 5. It is robust to outliers.</li>
        <li><b>Mean Squared Error (MSE):</b> Squares the errors, meaning larger errors are punished exponentially more than smaller ones. An error of 10 is penalized four times as much as an error of 5 (100 vs 25). This is preferred when large errors are particularly undesirable.</li>
    </ul>
    <h4>Python Implementation Example:</h4>
    <pre><code>import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Given y_true and y_pred lists/arrays
mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)

print(f'MAE: {mae}')
print(f'MSE: {mse}')</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> <b>MAE</b> is like standard grading: every mistake costs you a fixed amount of points. <b>MSE</b> is like strict penalty grading: small mistakes cost a little, but huge mistakes are squared, severely penalizing wild guesses!</div>'''
}

for item in data:
    if item['id'] in rewrites:
        item['answer_html'] = rewrites[item['id']]

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print('Success!')
