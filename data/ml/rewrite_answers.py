import json
import os

input_file = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\part_1.json"
output_file = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\part_1_final.json"

updates = {
    "num_q16": """<div class='solution-step'>
    <h3>Step 1: Understand the Goal</h3>
    <ul>
        <li>We need to fit a <strong>Quadratic Model</strong>: <code>y = b0 + b1x + b2x²</code>.</li>
        <li>We use the <strong>Least-Squares Method</strong> to find the coefficients (b0, b1, b2) that minimize the error between predicted and actual Y values.</li>
    </ul>
    <h3>Step 2: Construct the Data Table</h3>
    <ul>
        <li>We must calculate the necessary sums (Σ) for our normal equations by computing x², x³, x⁴, xy, and x²y for each data point.</li>
    </ul>
    <table>
        <tr><th>X</th><th>Y</th><th>X²</th><th>X³</th><th>X⁴</th><th>XY</th><th>X²Y</th></tr>
        <tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
        <tr><td>1</td><td>3</td><td>1</td><td>1</td><td>1</td><td>3</td><td>3</td></tr>
        <tr><td>2</td><td>9</td><td>4</td><td>8</td><td>16</td><td>18</td><td>36</td></tr>
        <tr><td>3</td><td>19</td><td>9</td><td>27</td><td>81</td><td>57</td><td>171</td></tr>
        <tr><td><b>Σ=6</b></td><td><b>Σ=32</b></td><td><b>Σ=14</b></td><td><b>Σ=36</b></td><td><b>Σ=98</b></td><td><b>Σ=78</b></td><td><b>Σ=210</b></td></tr>
    </table>
    <h3>Step 3: Set Up the Normal Equations</h3>
    <ul>
        <li>For a quadratic curve, the normal equations are derived by taking partial derivatives of the squared error with respect to each coefficient and setting them to zero. This gives us three simultaneous equations:</li>
    </ul>
    <pre>
1. n*b0 + Σx*b1 + Σx²*b2 = Σy
2. Σx*b0 + Σx²*b1 + Σx³*b2 = Σxy
3. Σx²*b0 + Σx³*b1 + Σx⁴*b2 = Σx²y
    </pre>
    <ul>
        <li>Substituting our calculated sums (with n=4 data points):</li>
    </ul>
    <pre>
(1)  4b0 +  6b1 + 14b2 = 32
(2)  6b0 + 14b1 + 36b2 = 78
(3) 14b0 + 36b1 + 98b2 = 210
    </pre>
    <h3>Step 4: Solve the System of Equations</h3>
    <ul>
        <li><strong>Simplify Equation (1):</strong> Divide by 2 to get <code>2b0 + 3b1 + 7b2 = 16</code>, which means <code>2b0 = 16 - 3b1 - 7b2</code>.</li>
        <li><strong>Eliminate b0 from Equation (2):</strong> Multiply Equation (1) by 3 (gives 6b0), substitute, and simplify to get <code>b1 = 6 - 3b2</code>.</li>
        <li><strong>Eliminate b0 from Equation (3):</strong> Use similar substitution to get <code>15b1 + 49b2 = 98</code>.</li>
        <li><strong>Find b2:</strong> Substitute <code>b1 = 6 - 3b2</code> into the previous result: <code>15(6 - 3b2) + 49b2 = 98</code>. This simplifies to <code>4b2 = 8</code>, so <b>b2 = 2</b>.</li>
        <li><strong>Find b1:</strong> <code>b1 = 6 - 3(2) = 0</code>, so <b>b1 = 0</b>.</li>
        <li><strong>Find b0:</strong> <code>2b0 = 16 - 3(0) - 7(2) = 2</code>, so <b>b0 = 1</b>.</li>
    </ul>
    <h3>Step 5: Final Model</h3>
    <ul>
        <li>Substitute the coefficients back into the equation: <b>y = 1 + 2x²</b>.</li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <ul>
        <li><b>Linear and Polynomial Regression Fundamentals:</b> Regression aims to model the relationship between variables. By adding polynomial terms (like x²), a linear model can fit non-linear curves while remaining "linear" in its parameters.</li>
        <li><b>Ordinary Least Squares (OLS):</b> The mathematical optimization technique used here to minimize the residual sum of squares (the difference between predicted and actual values).</li>
        <li><b>Normal Equations vs. Gradient Descent:</b> The method used above is the closed-form normal equation method, which provides an exact solution but can be computationally expensive for very large datasets, where iterative methods like Gradient Descent are preferred.</li>
    </ul>
    <h4>Python Example:</h4>
    <pre><code>import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Transform features to include x^2
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_train)

model = LinearRegression()
model.fit(X_poly, y_train)
print('Coefficients:', model.coef_)
print('Intercept:', model.intercept_)</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of the normal equations like building a pyramid. The first equation is the base (sums of basic terms). As you go down to the second and third equations, you multiply everything by another 'x', increasing the power of every term by one level!</div>""",
    "num_q28": """<div class='solution-step'>
    <h3>Step 1: Understand Error Metrics</h3>
    <ul>
        <li><strong>Error (e):</strong> The difference between the Actual value (Y) and the Predicted value (Y_hat). Formula: <code>e = Y - Y_hat</code>.</li>
        <li>We need to calculate three fundamental regression metrics: MAE, MSE, and RMSE.</li>
    </ul>
    <h3>Step 2: Construct the Error Table</h3>
    <ul>
        <li>Calculate the raw error, the absolute error <code>|e|</code>, and the squared error <code>e²</code> for each data point.</li>
    </ul>
    <table>
        <tr><th>Y (Actual)</th><th>Y_hat (Predicted)</th><th>Error (e = Y - Y_hat)</th><th>Absolute Error |e|</th><th>Squared Error e²</th></tr>
        <tr><td>10</td><td>12</td><td>-2</td><td>2</td><td>4</td></tr>
        <tr><td>15</td><td>13</td><td>2</td><td>2</td><td>4</td></tr>
        <tr><td>20</td><td>18</td><td>2</td><td>2</td><td>4</td></tr>
        <tr><td>25</td><td>28</td><td>-3</td><td>3</td><td>9</td></tr>
        <tr><td>30</td><td>27</td><td>3</td><td>3</td><td>9</td></tr>
        <tr><td><b>Sum (Σ)</b></td><td></td><td></td><td><b>12</b></td><td><b>30</b></td></tr>
    </table>
    <h3>Step 3: Calculate the Metrics</h3>
    <ul>
        <li>Total number of observations (<b>n</b>) = 5.</li>
        <li><b>Mean Absolute Error (MAE):</b> The average of the absolute errors. It measures the average magnitude of errors regardless of their direction.
            <br><i>Calculation:</i> Σ|e| / n = 12 / 5 = <b>2.4</b>
        </li>
        <li><b>Mean Squared Error (MSE):</b> The average of the squared errors. It penalizes larger errors more heavily because of the squaring.
            <br><i>Calculation:</i> Σe² / n = 30 / 5 = <b>6.0</b>
        </li>
        <li><b>Root Mean Squared Error (RMSE):</b> The square root of the MSE. It brings the error metric back to the original units of the target variable, making it easier to interpret.
            <br><i>Calculation:</i> √MSE = √6.0 ≈ <b>2.449</b>
        </li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <ul>
        <li><b>Evaluating Regression Models:</b> MAE, MSE, and RMSE are standard metrics used to quantify how well a regression model's predictions align with real-world data.</li>
        <li><b>Choosing the Right Metric:</b> 
            <ul>
                <li>Use <b>MAE</b> when you want a straightforward average error and your dataset contains outliers you don't want to heavily penalize.</li>
                <li>Use <b>MSE</b> or <b>RMSE</b> when large prediction errors are particularly undesirable, as squaring the errors drastically increases the penalty for outliers.</li>
            </ul>
        </li>
    </ul>
    <h4>Python Example:</h4>
    <pre><code>from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
print(f'MAE: {mae}, MSE: {mse}, RMSE: {rmse}')</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> MAE is the "polite" critic that treats all mistakes equally. MSE is the "harsh" critic that heavily punishes you for huge mistakes (by squaring them). RMSE is just the harsh critic forced to speak in terms you can understand (original units).</div>""",
    "num_u3_q1": """<div class='solution-step'>
    <h3>Step 1: Understand the Sigmoid Function</h3>
    <ul>
        <li><strong>Logistic Regression</strong> outputs a linear score (z). To convert this score into a valid probability (between 0 and 1), we pass it through the <strong>Sigmoid Function</strong>.</li>
        <li>Formula: <code>P = 1 / (1 + e^(-z))</code>, where <i>e</i> is Euler's number (approximately 2.718).</li>
    </ul>
    <h3>Step 2: Calculate the Probability</h3>
    <ul>
        <li>Given linear score: <b>z = 2.5</b></li>
        <li>Substitute z into the sigmoid function: 
            <br><code>P = 1 / (1 + e^(-2.5))</code>
        </li>
        <li>Calculate the exponential term: <code>e^(-2.5) ≈ 0.082</code></li>
        <li>Complete the calculation: 
            <br><code>P = 1 / (1 + 0.082)</code>
            <br><code>P = 1 / 1.082 ≈ <b>0.924</b></code>
        </li>
    </ul>
    <h3>Step 3: Classify Using the Threshold</h3>
    <ul>
        <li>A <strong>Decision Boundary (Threshold)</strong> is used to map the probability to a discrete class (0 or 1).</li>
        <li>Given Threshold = 0.5.</li>
        <li>Since our calculated probability <b>0.924 > 0.5</b>, the model is highly confident.</li>
        <li>Therefore, the predicted class is <b>1</b>.</li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <ul>
        <li><b>Logistic Regression Deep Dive:</b> A fundamental classification algorithm that models the probability of a discrete outcome given an input variable. Despite its name, it is used for classification, not continuous regression.</li>
        <li><b>The Role of Sigmoid:</b> The sigmoid function mathematically guarantees that the output will always smoothly asymptote between 0 and 1, making it perfectly suited for modeling probabilities.</li>
        <li><b>Log-Loss (Binary Cross-Entropy):</b> The cost function used to optimize logistic regression. It penalizes predictions that are confident but wrong.</li>
    </ul>
    <h4>Python Example:</h4>
    <pre><code>from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.array([[2, 1], [3, 4], [5, 1], [6, 2]])
y = np.array([0, 0, 1, 1])
model = LogisticRegression().fit(X, y)
probs = model.predict_proba([[4, 2]])
print('Class probabilities:', probs)</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> The Sigmoid function is like a harsh bouncer at a club. It takes any number from negative infinity to positive infinity and physically forces them to fit into a tiny room between exactly 0 and 1! Positive numbers get pushed toward 1, negative numbers toward 0.</div>""",
    "num_u3_q2": """<div class='solution-step'>
    <h3>Step 1: Apply the Sigmoid Function</h3>
    <ul>
        <li>We are given a negative linear score: <b>z = -1.8</b>.</li>
        <li>We must convert this raw score into a probability using the <strong>Sigmoid Function</strong>.</li>
        <li>Formula: <code>P = 1 / (1 + e^(-z))</code></li>
    </ul>
    <h3>Step 2: Perform the Calculation</h3>
    <ul>
        <li>Substitute z = -1.8 into the formula:
            <br><code>P = 1 / (1 + e^(-(-1.8)))</code>
            <br><code>P = 1 / (1 + e^(1.8))</code>
        </li>
        <li>Calculate the exponential term: <code>e^(1.8) ≈ 6.0496</code></li>
        <li>Complete the division:
            <br><code>P = 1 / (1 + 6.0496)</code>
            <br><code>P = 1 / 7.0496 ≈ <b>0.1418</b></code>
        </li>
    </ul>
    <h3>Step 3: Determine the Class</h3>
    <ul>
        <li>Compare the calculated probability against the specified classification <strong>threshold</strong> of 0.5.</li>
        <li>Since <b>0.1418 < 0.5</b>, the model predicts that the event is unlikely to happen.</li>
        <li>Therefore, the sample belongs to <b>Class 0</b>.</li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <ul>
        <li><b>Handling Negative Z-Scores:</b> In logistic regression, a negative z-score mathematically translates to a probability of less than 0.5. The more negative the score, the closer the probability approaches exactly 0.</li>
        <li><b>Decision Boundary:</b> The standard threshold is 0.5, but in practical applications (like medical diagnosis or fraud detection), this threshold can be adjusted to minimize false positives or false negatives depending on business requirements.</li>
    </ul>
    <h4>Python Example:</h4>
    <pre><code>import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

z_score = -1.8
prob = sigmoid(z_score)
predicted_class = 1 if prob >= 0.5 else 0

print(f'Probability: {prob:.4f}, Class: {predicted_class}')</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> A negative z-score ALWAYS guarantees a probability below 50%. A positive z-score ALWAYS guarantees a probability above 50%. If z=0 exactly, it's a perfect 50/50 coin toss!</div>""",
    "num_u3_q3": """<div class='solution-step'>
    <h3>Step 1: Calculate the Linear Combination (z)</h3>
    <ul>
        <li>The logistic regression equation combines input features with learned weights to produce a linear score.</li>
        <li><strong>Model Equation:</strong> <code>z = -3 + 0.8*x1 + 1.2*x2</code></li>
        <li>Substitute the given data point values (<b>x1 = 2</b>, <b>x2 = 1</b>):
            <br><code>z = -3 + 0.8(2) + 1.2(1)</code>
            <br><code>z = -3 + 1.6 + 1.2</code>
            <br><code>z = <b>-0.2</b></code>
        </li>
    </ul>
    <h3>Step 2: Convert to Probability (Sigmoid Function)</h3>
    <ul>
        <li>Now, transform the linear score (z) into a probability (P) between 0 and 1.</li>
        <li><strong>Formula:</strong> <code>P = 1 / (1 + e^(-z))</code></li>
        <li>Substitute z = -0.2:
            <br><code>P = 1 / (1 + e^(-(-0.2)))</code>
            <br><code>P = 1 / (1 + e^(0.2))</code>
        </li>
        <li>Calculate components: <code>e^(0.2) ≈ 1.2214</code></li>
        <li>Result: <code>P = 1 / (1 + 1.2214) = 1 / 2.2214 ≈ <b>0.450</b></code></li>
    </ul>
    <h3>Step 3: Make the Prediction</h3>
    <ul>
        <li>Compare the final probability to the <strong>decision boundary</strong> (threshold = 0.5).</li>
        <li>Since <b>0.450 < 0.5</b>, the model leans slightly towards the negative class.</li>
        <li>The predicted class is <b>0</b>.</li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <ul>
        <li><b>Feature Weights and Bias:</b> In the equation <code>z = b0 + b1x1 + b2x2</code>, the constant term (-3) is the bias (or intercept), which shifts the decision boundary. The coefficients (0.8 and 1.2) represent the weight or importance of each feature in determining the outcome.</li>
        <li><b>Interpreting the Output:</b> Because the probability (0.450) is very close to 0.5, this implies the data point is physically located very close to the decision boundary in the feature space. The model is somewhat uncertain, but forced to make a binary decision.</li>
    </ul>
    <h4>Python Example:</h4>
    <pre><code>import math

x1, x2 = 2, 1
z = -3 + 0.8*x1 + 1.2*x2
probability = 1 / (1 + math.exp(-z))
prediction = 1 if probability >= 0.5 else 0

print(f'Z: {z}, Prob: {probability:.3f}, Class: {prediction}')</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of the linear equation (z) as a scale. The bias (-3) puts a heavy weight on the "Class 0" side. The features (x1, x2) add weights to the "Class 1" side. In this case, the features added 2.8, which wasn't quite enough to overcome the -3 bias, keeping the result slightly on the Class 0 side!</div>""",
    "num_u3_q4": """<div class='solution-step'>
    <h3>Step 1: Understand Binary Cross-Entropy (Log-Loss)</h3>
    <ul>
        <li><strong>Log-Loss</strong> measures the performance of a classification model where the prediction input is a probability value between 0 and 1. It heavily penalizes confident but incorrect predictions.</li>
        <li><strong>Formula:</strong> <code>Log-Loss = -1/n * Σ [y*ln(p) + (1-y)*ln(1-p)]</code>
            <ul>
                <li><code>n</code> = number of observations</li>
                <li><code>y</code> = actual label (0 or 1)</li>
                <li><code>p</code> = predicted probability</li>
                <li><code>ln</code> = natural logarithm</li>
            </ul>
        </li>
    </ul>
    <h3>Step 2: Calculate the Loss for Each Observation</h3>
    <ul>
        <li>Note: If y=1, the second half of the formula <code>(1-y)*ln(1-p)</code> becomes zero. If y=0, the first half <code>y*ln(p)</code> becomes zero.</li>
        <li><strong>Observation 1:</strong> y=1, p=0.9
            <br>Loss contribution = <code>1 * ln(0.9) ≈ -0.1054</code>
        </li>
        <li><strong>Observation 2:</strong> y=1, p=0.7
            <br>Loss contribution = <code>1 * ln(0.7) ≈ -0.3567</code>
        </li>
        <li><strong>Observation 3:</strong> y=0, p=0.2
            <br>Loss contribution = <code>(1-0) * ln(1 - 0.2) = ln(0.8) ≈ -0.2231</code>
        </li>
        <li><strong>Observation 4:</strong> y=0, p=0.4
            <br>Loss contribution = <code>(1-0) * ln(1 - 0.4) = ln(0.6) ≈ -0.5108</code>
        </li>
    </ul>
    <h3>Step 3: Aggregate and Compute Final Loss</h3>
    <ul>
        <li><strong>Sum the individual contributions:</strong>
            <br><code>Σ = (-0.1054) + (-0.3567) + (-0.2231) + (-0.5108) = -1.196</code>
        </li>
        <li><strong>Multiply by -1/n (where n = 4):</strong>
            <br><code>Log-Loss = -1/4 * (-1.196) = <b>0.299</b></code>
        </li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <ul>
        <li><b>Why Logarithms?</b> The natural logarithm strongly penalizes predictions that are far from the true label. If a model predicts a probability of 0.99 for an event that does not happen (y=0), the log-loss penalty approaches infinity.</li>
        <li><b>Optimization Objective:</b> During the training of a logistic regression or neural network model, the algorithm's primary goal is to find the weights that minimize this exact Log-Loss value across the entire dataset.</li>
    </ul>
    <h4>Python Example:</h4>
    <pre><code>from sklearn.metrics import log_loss
import numpy as np

y_true = np.array([1, 1, 0, 0])
y_pred_probs = np.array([0.9, 0.7, 0.2, 0.4])

loss = log_loss(y_true, y_pred_probs)
print(f'Log-Loss: {loss:.3f}')</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> The Log-Loss formula looks scary, but it acts like a simple two-way switch. If the actual answer is 1, the formula deletes the right half and only looks at `ln(p)`. If the actual answer is 0, it deletes the left half and only looks at `ln(1-p)`!</div>""",
    "num_u3_q5": """<div class='solution-step'>
    <h3>Step 1: Understand the Goal of K-Nearest Neighbors (KNN)</h3>
    <ul>
        <li>We need to classify an unknown Query Point <b>Q (4,3)</b> using a training dataset.</li>
        <li>Using <b>K=3</b>, we will find the 3 closest data points to Q and take a majority vote to determine its class.</li>
    </ul>
    <h3>Step 2: Calculate Euclidean Distances</h3>
    <ul>
        <li><strong>Formula:</strong> <code>d = √((x2 - x1)² + (y2 - y1)²)</code></li>
        <li>We must calculate the distance from Query Q (4,3) to every training point:</li>
        <li><strong>Point A (1,1, C=0):</strong>
            <br><code>d(A, Q) = √((4-1)² + (3-1)²) = √(3² + 2²) = √(9 + 4) = √13 ≈ 3.605</code>
        </li>
        <li><strong>Point B (2,2, C=0):</strong>
            <br><code>d(B, Q) = √((4-2)² + (3-2)²) = √(2² + 1²) = √(4 + 1) = √5 ≈ 2.236</code>
        </li>
        <li><strong>Point C (3,2, C=1):</strong>
            <br><code>d(C, Q) = √((4-3)² + (3-2)²) = √(1² + 1²) = √(1 + 1) = √2 ≈ 1.414</code>
        </li>
        <li><strong>Point D (5,4, C=1):</strong>
            <br><code>d(D, Q) = √((4-5)² + (3-4)²) = √((-1)² + (-1)²) = √(1 + 1) = √2 ≈ 1.414</code>
        </li>
        <li><strong>Point E (6,5, C=1):</strong>
            <br><code>d(E, Q) = √((4-6)² + (3-5)²) = √((-2)² + (-2)²) = √(4 + 4) = √8 ≈ 2.828</code>
        </li>
    </ul>
    <h3>Step 3: Select the K Nearest Neighbors</h3>
    <ul>
        <li>Rank the distances from smallest to largest. We only need the top K=3 closest points.</li>
        <li><strong>1st Closest:</strong> Point C (d ≈ 1.414), Class = 1</li>
        <li><strong>2nd Closest:</strong> Point D (d ≈ 1.414), Class = 1</li>
        <li><strong>3rd Closest:</strong> Point B (d ≈ 2.236), Class = 0</li>
    </ul>
    <h3>Step 4: Determine the Final Class via Majority Vote</h3>
    <ul>
        <li>The classes of our 3 nearest neighbors are: <b>{1, 1, 0}</b>.</li>
        <li>Class 1 appears twice, while Class 0 appears once.</li>
        <li>By majority vote, the predicted class for Query Q is <b>Class 1</b>.</li>
    </ul>
</div>
<hr/>
<div class='comprehensive-analysis'>
    <h3>Comprehensive Analysis and Implementation Details</h3>
    <ul>
        <li><b>Non-Parametric and Lazy Learning:</b> KNN is a "lazy" algorithm because it does not explicitly build a mathematical model during a training phase. Instead, it memorizes the dataset and performs all computations at prediction time.</li>
        <li><b>Choosing K:</b> K should generally be an odd number (like 3, 5, or 7) in binary classification to avoid tie votes. A very small K (e.g., K=1) makes the prediction highly sensitive to noise and outliers, while a very large K dilutes the local context and might just predict the majority class of the whole dataset.</li>
    </ul>
    <h4>Python Example:</h4>
    <pre><code>from sklearn.neighbors import KNeighborsClassifier
import numpy as np

X_train = np.array([[1,1], [2,2], [3,2], [5,4], [6,5]])
y_train = np.array([0, 0, 1, 1, 1])

knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
knn.fit(X_train, y_train)

query_point = np.array([[4, 3]])
prediction = knn.predict(query_point)
print('Predicted class:', prediction[0])</code></pre>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of KNN like asking your closest neighbors for advice. If you need a recommendation (a classification), you don't ask the whole city. You ask your 3 closest friends. Whatever the majority of them recommend, you follow!</div>"""
}

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item['id'] in updates:
        item['answer_html'] = updates[item['id']]

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Updated successfully")
