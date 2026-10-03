import json

file_path = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_3_part2.json"

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_answers = {
    "5m_q8": """<div>
  <div class="concept-heading">Polynomial Regression</div>
  <p>Polynomial Regression is a form of regression analysis where the relationship between the independent variable $x$ and the dependent variable $y$ is modeled as an $n$-th degree polynomial.</p>
  <p><b>1. Capturing Non-Linear Patterns:</b></p>
  <ul>
    <li>Standard linear regression assumes a straight-line relationship: $y = \\theta_0 + \\theta_1x$.</li>
    <li>Polynomial regression adds higher-degree terms (like $x^2, x^3$): $y = \\theta_0 + \\theta_1x + \\theta_2x^2 + \\dots + \\theta_nx^n$.</li>
    <li>These additional terms allow the model's regression line to curve.</li>
    <li>This curvature enables the model to accurately fit complex, non-linear trajectories in the data that a straight line would miss.</li>
  </ul>
  <p><b>2. Maintaining a Linear Cost Function:</b></p>
  <ul>
    <li>Despite the curved decision boundary, the model is still classified mathematically as a <i>Linear Model</i>.</li>
    <li>This is because the model remains linear concerning its parameters (the weights $\\theta_i$).</li>
    <li>By defining new features (e.g., $x_1 = x, x_2 = x^2, x_3 = x^3$), the equation translates into a standard multiple linear regression format: $y = \\theta_0 + \\theta_1x_1 + \\theta_2x_2 + \\dots + \\theta_nx_n$.</li>
    <li>Consequently, the cost function (Mean Squared Error) remains a convex bowl shape.</li>
    <li>This guarantees that optimization algorithms, like Gradient Descent or Ordinary Least Squares (OLS), can find the global minimum without structural changes.</li>
  </ul>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of the $x, x^2, x^3$ terms as completely different variables ($x_1, x_2, x_3$) acting in a straight-line equation. The curve happens on the graph, but the math under the hood is still just adding up separate variables multiplied by weights!</div>""",
    "5m_q9": """<div>
  <div class="concept-heading">Overfitting, Underfitting, and Bias-Variance Tradeoff</div>
  <p>In Machine Learning, a model must generalize well to unseen data. When a model fails to generalize, it typically suffers from either Underfitting or Overfitting.</p>
  <p><b>1. Underfitting (High Bias):</b></p>
  <ul>
    <li>Occurs when the model is too simplistic to learn the underlying patterns in the training data.</li>
    <li>Results in poor predictive performance on both the training dataset and the testing dataset.</li>
    <li>Represents <b>High Bias</b>, as the model makes strong, incorrect assumptions about the data structure.</li>
  </ul>
  <p><b>2. Overfitting (High Variance):</b></p>
  <ul>
    <li>Occurs when the model is excessively complex, memorizing random noise and fluctuations rather than the true signal.</li>
    <li>Results in exceptionally high accuracy on the training dataset but poor performance on the unseen testing dataset.</li>
    <li>Represents <b>High Variance</b>, as the model's predictions fluctuate wildly depending on the specific training data it saw.</li>
  </ul>
  <p><b>3. Relationship with Model Complexity and Error Rates:</b></p>
  <ul>
    <li><b>Training Error:</b> As model complexity increases, training error steadily decreases because the model fits the training points more tightly.</li>
    <li><b>Testing Error:</b> Initially decreases as the model learns useful patterns, but eventually begins to increase sharply once the model becomes too complex and starts to overfit.</li>
    <li><b>Bias-Variance Tradeoff:</b> The ultimate goal of model training is to find the optimal complexity—the "sweet spot"—that minimizes total testing error by perfectly balancing bias and variance.</li>
  </ul>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Underfitting is like a student who didn't study and fails the exam (bad on train, bad on test). Overfitting is like a student who memorized the exact practice questions but can't solve new ones (perfect on train, bad on test). The Tradeoff is studying the underlying concepts to pass any exam!</div>""",
    "5m_q10": """<div>
  <div class="concept-heading">Ridge (L2) vs Lasso (L1) Regularization</div>
  <p>Regularization is a technique used to prevent overfitting by adding a penalty term to the cost function. This penalty discourages the model from assigning excessively large values to its weights (coefficients).</p>
  <p><b>1. Ridge Regularization (L2):</b></p>
  <ul>
    <li><b>Cost Function Penalty:</b> Adds the <i>squared magnitude</i> of the coefficients to the Mean Squared Error (MSE): $J(\\theta) = MSE + \\lambda \\sum_{i=1}^{n} \\theta_i^2$.</li>
    <li><b>Coefficient Shrinkage:</b> It shrinks all feature coefficients closer to zero but rarely forces them to be exactly zero.</li>
    <li><b>Use Case:</b> Excellent for handling multicollinearity (highly correlated features) by evenly distributing the weights among them.</li>
  </ul>
  <p><b>2. Lasso Regularization (L1):</b></p>
  <ul>
    <li><b>Cost Function Penalty:</b> Adds the <i>absolute value</i> of the coefficients to the MSE: $J(\\theta) = MSE + \\lambda \\sum_{i=1}^{n} |\\theta_i|$.</li>
    <li><b>Sparse Solutions (Feature Selection):</b> The absolute value penalty creates a diamond-shaped geometric constraint region.</li>
    <li>Because of this sharp geometry, the optimization process often forces the coefficients of less important features to become <b>exactly zero</b>.</li>
    <li><b>Use Case:</b> Highly useful for automatic feature selection, resulting in sparse, simpler, and more interpretable models.</li>
  </ul>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> L<b>a</b>sso = L<b>1</b> = <b>A</b>bsolute value = forces weights to Zero (Feature Selection). R<b>i</b>dge = L<b>2</b> = Squared (L-tw<b>o</b>) = shrinks weights but keeps them all.</div>""",
    "5m_q11": """<div>
  <div class="concept-heading">Regression Evaluation Metrics</div>
  <p>Evaluating regression models requires quantifying the difference between the actual target values ($y$) and the predicted values ($\\hat{y}$).</p>
  <p><b>1. Common Error Metrics:</b></p>
  <ul>
    <li><b>Mean Absolute Error (MAE):</b> Calculates the average of the absolute differences: $\\frac{1}{n} \\sum |y_i - \\hat{y}_i|$. It is robust to outliers, but its derivative is undefined at exactly zero.</li>
    <li><b>Mean Squared Error (MSE):</b> Calculates the average of the squared differences: $\\frac{1}{n} \\sum (y_i - \\hat{y}_i)^2$. Squaring the errors heavily penalizes large outliers and creates a smooth, differentiable curve ideal for gradient descent.</li>
    <li><b>Root Mean Squared Error (RMSE):</b> The square root of MSE: $\\sqrt{MSE}$.</li>
  </ul>
  <p><b>2. Explained Variance Metrics:</b></p>
  <ul>
    <li><b>R-Squared ($R^2$):</b> Measures the proportion of variance in the dependent variable that the model successfully explains. It ranges from 0 to 1, where higher is better.</li>
    <li><b>Adjusted $R^2$:</b> A modified version of $R^2$ that includes a penalty for adding irrelevant predictive features.</li>
  </ul>
  <p><b>3. Why RMSE and Adjusted $R^2$ are Preferred:</b></p>
  <ul>
    <li><b>RMSE:</b> By taking the square root of the MSE, the resulting metric is expressed in the exact same units as the original target variable. This makes it highly intuitive for stakeholders to interpret the average error magnitude.</li>
    <li><b>Adjusted $R^2$:</b> Standard $R^2$ mathematically increases every time a new feature is added, even if the feature is completely random garbage. Adjusted $R^2$ fixes this by penalizing unnecessary complexity, providing a much more honest evaluation of the model's real predictive power.</li>
  </ul>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> RMSE puts the error back into "normal human units" (like dollars instead of squared-dollars). Adjusted $R^2$ acts like a strict grader who deducts points if you add useless fluff to your essay just to make it longer!</div>""",
    "5m_q12": """<div>
  <div class="concept-heading">Logistic Regression and Sigmoid Function</div>
  <p>Logistic Regression is a fundamental supervised learning algorithm utilized primarily for binary classification tasks (predicting one of two classes).</p>
  <p><b>1. Transition from Linear to Logistic:</b></p>
  <ul>
    <li>Standard linear regression outputs a continuous unbounded number ($z = W^TX + b$).</li>
    <li>Logistic regression takes this continuous linear output and mathematically "squashes" it into a valid probability score between 0 and 1.</li>
    <li>This squashing is achieved using the <b>Sigmoid Activation Function</b>.</li>
  </ul>
  <p><b>2. The Sigmoid Function ($\\sigma$):</b></p>
  <ul>
    <li><b>Formula:</b> $\\sigma(z) = \\frac{1}{1 + e^{-z}}$</li>
  </ul>
  <p><b>3. Mathematical Properties of Sigmoid:</b></p>
  <ul>
    <li><b>Probability Range:</b> The output is strictly bounded: $0 \\le \\sigma(z) \\le 1$, making it perfectly suited for representing probabilities.</li>
    <li><b>S-shaped Curve:</b> Large positive inputs asymptotically approach 1, while large negative inputs asymptotically approach 0. An input of exactly 0 yields 0.5.</li>
    <li><b>Efficient Derivative:</b> The derivative can be calculated using the function's own output: $\\sigma'(z) = \\sigma(z)(1 - \\sigma(z))$. This makes backpropagation and gradient descent computationally efficient.</li>
    <li><b>Decision Boundary Threshold:</b> In practice, a threshold (usually 0.5) is applied. If the output probability is $\\ge 0.5$, the model predicts Class 1; otherwise, it predicts Class 0.</li>
  </ul>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of the Sigmoid function as a strict bouncer at a club. No matter how large the number trying to get in (positive or negative infinity), the bouncer forces them to stand nicely in line between 0 and 1!</div>""",
    "5m_q13": """<div>
  <div class="concept-heading">Log-Loss (Binary Cross-Entropy)</div>
  <p>In Logistic Regression, the model must be trained using a specific cost function called Log-Loss (or Binary Cross-Entropy), which measures how far the predicted probabilities deviate from the actual binary labels.</p>
  <p><b>1. The Log-Loss Formula:</b></p>
  <p>$J(\\theta) = -\\frac{1}{m} \\sum_{i=1}^{m} \\left[ y^{(i)} \\log(h_\\theta(x^{(i)})) + (1 - y^{(i)}) \\log(1 - h_\\theta(x^{(i)})) \\right]$</p>
  <ul>
    <li>$h_\\theta(x)$ represents the model's predicted probability (between 0 and 1).</li>
    <li>$y$ represents the true actual label (either strictly 0 or strictly 1).</li>
  </ul>
  <p><b>2. Why Standard MSE Fails for Classification:</b></p>
  <ul>
    <li>If we attempt to use the standard Mean Squared Error equation: $J(\\theta) = \\frac{1}{2m} \\sum (\\sigma(W^TX) - y)^2$, problems arise.</li>
    <li>The inclusion of the non-linear sigmoid function ($\\sigma$) inside the squared term warps the mathematical landscape of the cost function.</li>
    <li>This results in a <b>non-convex</b> shape, characterized by multiple "valleys" or local minima.</li>
    <li>During optimization, Gradient Descent can easily become trapped in these local minima, completely missing the best possible global solution.</li>
  </ul>
  <p><b>3. The Solution Provided by Log-Loss:</b></p>
  <ul>
    <li>By using logarithms, Log-Loss cancels out the problematic non-linearity of the sigmoid function.</li>
    <li>This mathematically guarantees a smooth, <b>convex</b> (single bowl-shaped) cost function landscape with only one global minimum.</li>
    <li>Additionally, the logarithm heavily and exponentially penalizes the model when it is highly confident but completely wrong.</li>
  </ul>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> MSE on a Sigmoid is like a bumpy mountain range (non-convex)—you might get stuck in a high valley. Log-Loss smooths the whole mountain into a single perfect bowl (convex), so a rolling ball (Gradient Descent) will always reach the true bottom!</div>""",
    "5m_q14": """<div>
  <div class="concept-heading">K-Nearest Neighbors (KNN) Algorithm</div>
  <p>K-Nearest Neighbors (KNN) is an intuitive, instance-based, non-parametric learning algorithm that can be utilized for both classification and regression tasks.</p>
  <p><b>1. Step-by-Step Prediction Mechanics:</b></p>
  <ul>
    <li><b>Step 1:</b> When given a new, unseen data point, calculate the geometric distance between this new point and every single point in the existing training dataset.</li>
    <li><b>Step 2:</b> Sort these distances in ascending order to identify the $K$ closest training data points (the "nearest neighbors").</li>
    <li><b>Step 3 (Classification):</b> Apply a majority vote. The new point is assigned the class that is most common among its $K$ neighbors.</li>
    <li><b>Step 4 (Regression):</b> Calculate the mathematical average of the target values of the $K$ neighbors to predict the continuous value.</li>
  </ul>
  <p><b>2. Distance Metric Selection:</b></p>
  <ul>
    <li><b>Euclidean Distance:</b> The standard straight-line distance, best for continuous, real-valued data.</li>
    <li><b>Manhattan Distance:</b> Calculates distance along grid lines (like city blocks). Superior for high-dimensional datasets.</li>
  </ul>
  <p><b>3. Impact of the 'K' Value:</b></p>
  <ul>
    <li><b>Small K (e.g., K=1):</b> The algorithm rigidly follows the closest single point. This creates jagged, irregular decision boundaries that capture local noise. It results in low bias but <b>high variance (overfitting)</b>.</li>
    <li><b>Large K:</b> The algorithm averages over many points. This creates smooth, generalized decision boundaries. However, if K is excessively large, it ignores local patterns completely, resulting in high bias and <b>underfitting</b>.</li>
  </ul>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> A small K (like K=1) is like asking your single closest friend for advice—their personal bias heavily influences you (Overfitting). A large K is like asking the whole city—you get a very general average, but lose the nuance (Underfitting).</div>""",
    "5m_q15": """<div>
  <div class="concept-heading">Decision Tree Splitting Metrics</div>
  <p>Decision Trees build predictive models by recursively partitioning the training dataset. At each step, the algorithm must choose a feature threshold that maximizes the purity (homogeneity) of the resulting child nodes.</p>
  <p><b>1. Entropy:</b></p>
  <ul>
    <li>A mathematical measure of the impurity, disorder, or uncertainty within a specific node.</li>
    <li>A perfectly pure node (all samples belong to one class) has an Entropy of 0. A perfectly mixed binary node (50/50 split) has a maximum Entropy of 1.0.</li>
    <li><b>Formula:</b> $E = -\\sum_{i=1}^{c} p_i \\log_2(p_i)$ (where $p_i$ is the probability/proportion of class $i$).</li>
  </ul>
  <p><b>2. Information Gain:</b></p>
  <ul>
    <li>Measures the total reduction in Entropy achieved by splitting a dataset using a specific attribute.</li>
    <li>The algorithm calculates Information Gain for every possible feature split and selects the one that provides the highest gain (i.e., reduces disorder the most).</li>
    <li><b>Formula:</b> $IG(S, A) = Entropy(S) - \\sum \\left( \\frac{|S_v|}{|S|} \\right) Entropy(S_v)$</li>
  </ul>
  <p><b>3. Gini Impurity:</b></p>
  <ul>
    <li>An alternative metric to Entropy, predominantly used by the CART decision tree algorithm.</li>
    <li>It measures the probability that a randomly chosen element from the node would be misclassified if it were randomly labeled according to the node's class distribution.</li>
    <li>It is computationally faster to calculate than Entropy because it avoids complex logarithmic functions.</li>
    <li><b>Formula:</b> $Gini = 1 - \\sum_{i=1}^{c} p_i^2$</li>
  </ul>
</div>
<div class="diagram-container" style="margin-top: 1.5rem;">
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="20" width="100" height="40" rx="4" fill="var(--card-bg)" stroke="currentColor" stroke-width="2"/>
  <text x="200" y="45" text-anchor="middle" fill="currentColor" font-size="12">Root Node</text>
  <line x1="200" y1="60" x2="100" y2="100" stroke="currentColor" stroke-width="2"/>
  <text x="130" y="80" fill="currentColor" font-size="10">Feature X &gt; 0.5</text>
  <line x1="200" y1="60" x2="300" y2="100" stroke="currentColor" stroke-width="2"/>
  <text x="280" y="80" fill="currentColor" font-size="10">Feature X &lt;= 0.5</text>
  <rect x="50" y="100" width="100" height="40" rx="4" fill="var(--card-bg)" stroke="currentColor" stroke-width="2"/>
  <text x="100" y="125" text-anchor="middle" fill="currentColor" font-size="12">Internal Node</text>
  <rect x="250" y="100" width="100" height="40" rx="4" fill="var(--primary-teal)" stroke="currentColor" stroke-width="2"/>
  <text x="300" y="125" text-anchor="middle" fill="#000" font-weight="bold" font-size="12">Leaf A</text>
  <line x1="100" y1="140" x2="50" y2="180" stroke="currentColor" stroke-width="2"/>
  <line x1="100" y1="140" x2="150" y2="180" stroke="currentColor" stroke-width="2"/>
  <rect x="0" y="180" width="100" height="40" rx="4" fill="var(--primary-teal)" stroke="currentColor" stroke-width="2"/>
  <text x="50" y="205" text-anchor="middle" fill="#000" font-weight="bold" font-size="12">Leaf B</text>
  <rect x="110" y="180" width="100" height="40" rx="4" fill="var(--primary-teal)" stroke="currentColor" stroke-width="2"/>
  <text x="160" y="205" text-anchor="middle" fill="#000" font-weight="bold" font-size="12">Leaf C</text>
  <text x="300" y="180" fill="currentColor" font-size="12" font-weight="bold">Information Gain</text>
  <text x="300" y="195" fill="currentColor" font-size="12">reduces Entropy</text>
  <text x="300" y="210" fill="currentColor" font-size="12">at each split.</text>
</svg>
</div>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Entropy is the "messiness" of a room. Information Gain is measuring exactly how much cleaner the room got after you organized (split) it. Gini is just a faster mathematical broom to calculate the mess!</div>"""
}

for item in data:
    if item['id'] in new_answers:
        item['answer_html'] = new_answers[item['id']]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Updates applied successfully.")
