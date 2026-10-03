import json
import os

input_file = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_1.json"
output_file = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_1_final.json"

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

rewrites = {
    "2m_q32": """<p><b>Formula:</b> <code>RMSE = &radic;((1/n) &Sigma; (yi - &ycirc;i)&sup2;)</code></p>
<p><b>Definition:</b> RMSE calculates the average magnitude of the errors in a set of predictions, without considering their direction.</p>
<p><b>Advantages over Mean Squared Error (MSE):</b></p>
<ul>
    <li><b>Same Units:</b> By taking the square root, RMSE converts the error metric back into the original units of the target variable. This makes the error much easier to interpret directly.</li>
    <li><b>Penalizes Large Errors:</b> Similar to MSE, RMSE squares the errors before averaging them. This means it places a heavy penalty on large errors, which is useful when large deviations are particularly undesirable in a model.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> "Root" brings it back to the "Root" units (original units). The "Square" ensures large errors stand out!</div>""",
    
    "2m_q33": """<p><b>Definition:</b> The R-squared (R&sup2;) coefficient, also known as the coefficient of determination, measures the proportion of variance in the dependent variable that is predictably explained by the independent variables in a regression model.</p>
<p><b>Standard Range:</b></p>
<ul>
    <li>Its standard range is strictly between <b>0 and 1</b>.</li>
    <li><b>0:</b> Indicates that the model explains none of the variability in the data around its mean.</li>
    <li><b>1:</b> Indicates that the model explains all of the variability in the data.</li>
</ul>
<p><b>Interpretation:</b> A higher R-squared value generally indicates a better fit for the model. However, a high R&sup2; does not always mean the model is practically good; it must be evaluated alongside other statistical metrics and context.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of R&sup2; as a percentage score (from 0% to 100%) grading how well the model's inputs explain its output.</div>""",

    "2m_q34": """<p><b>Limitation of Standard R-squared:</b></p>
<ul>
    <li>Standard R&sup2; has a mathematical flaw: it will always increase or remain the same whenever a new independent variable is added to a model.</li>
    <li>It does this even if the new variable provides absolutely no meaningful improvement to the predictions, leading to an artificially inflated score.</li>
</ul>
<p><b>Advantages of Adjusted R-squared:</b></p>
<ul>
    <li><b>Penalizes Useless Variables:</b> Adjusted R&sup2; incorporates a mathematical penalty for adding non-significant predictors.</li>
    <li><b>Adjusts for Model Complexity:</b> It adjusts the score based on the number of terms (variables) in the model relative to the number of data points.</li>
    <li><b>Prevents Overfitting:</b> By ensuring that only genuinely useful variables increase the score, it provides a much more accurate and reliable measure of goodness-of-fit for multiple linear regression models.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Standard R&sup2; is a flatterer that always goes up. Adjusted R&sup2; is a strict professor who deducts marks if you add useless fluff to your answer.</div>""",

    "2m_q35": """<p><b>Formula:</b> <code>&sigma;(z) = 1 / (1 + e^(-z))</code></p>
<p><b>Output Range:</b></p>
<ul>
    <li>The function maps any real-valued number into a continuously bounded output range strictly between <b>0 and 1</b>.</li>
    <li>The resulting graph forms a characteristic "S-shaped" curve.</li>
</ul>
<p><b>Primary Applications:</b></p>
<ul>
    <li><b>Binary Classification:</b> It is highly ideal for tasks with two possible outcomes.</li>
    <li><b>Probability Estimation:</b> Because the output is constrained between 0 and 1, the result can be mathematically interpreted directly as a probability (e.g., the probability that a data point belongs to the positive class).</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> "S"igmoid creates an "S" shape. It squishes any big or small number into a neat probability percentage between 0 and 1.</div>""",

    "2m_q36": """<p><b>Standard Threshold:</b></p>
<ul>
    <li>In Logistic Regression for binary classification, the standard decision threshold value is typically set to <b>0.5</b>.</li>
</ul>
<p><b>Classification Rules:</b></p>
<ul>
    <li><b>Positive Class (Class 1):</b> If the model's predicted probability for an instance is greater than or equal to 0.5 (<code>p &ge; 0.5</code>).</li>
    <li><b>Negative Class (Class 0):</b> If the predicted probability is strictly less than 0.5 (<code>p &lt; 0.5</code>).</li>
</ul>
<p><b>Adjustability:</b> This threshold is not fixed mathematically; it can be manually adjusted depending on the specific problem requirements. For instance, shifting the threshold can balance precision versus recall.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> 0.5 is the exact halfway point. If it's 50% or more likely, it's a "yes" (1). If it's less than 50% likely, it's a "no" (0).</div>""",

    "2m_q37": """<p><b>Formula:</b> <code>Cost = - [y * log(&ycirc;) + (1 - y) * log(1 - &ycirc;)]</code></p>
<p><b>Term Definitions:</b></p>
<ul>
    <li><code>y</code>: Represents the true binary label of the sample (must be exactly 0 or 1).</li>
    <li><code>&ycirc;</code>: Represents the model's predicted probability that the sample belongs to class 1 (a value between 0 and 1).</li>
</ul>
<p><b>Function Behavior:</b></p>
<ul>
    <li>If the true label is 1 (y=1), the second half of the equation cancels out, and the cost is based purely on <code>-log(&ycirc;)</code>.</li>
    <li>If the true label is 0 (y=0), the first half cancels out, and the cost is based on <code>-log(1 - &ycirc;)</code>.</li>
    <li>This cost function heavily penalizes highly confident but incorrect predictions, structurally guiding the model toward more accurate probability estimates.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> It's a "two-part switch." If true is 1, the left part turns on. If true is 0, the right part turns on. It brutally punishes the model if it is 100% sure about the wrong answer!</div>""",

    "2m_q38": """<p><b>Definition:</b> A decision boundary in a binary classification problem is a geometric hypersurface that separates the underlying feature space into two distinct regions, one corresponding to each class.</p>
<p><b>Types of Boundaries:</b></p>
<ul>
    <li><b>Linear Boundary:</b> A straight line or flat plane (e.g., a hyperplane in Support Vector Machines or Logistic Regression).</li>
    <li><b>Non-Linear Boundary:</b> A complex, curved shape (e.g., created by Decision Trees or RBF-kernel SVMs).</li>
</ul>
<p><b>Function:</b> Any new, unclassified data point falling on one side of this geometric boundary is computationally assigned to the first class, while points falling on the opposite side are assigned to the second class.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of it as a strict border wall on a map. If you land North of the wall, you belong to Country A; if South, you belong to Country B.</div>""",

    "2m_q39": """<p><b>Core Concept:</b> K-Nearest Neighbors (KNN) is a non-parametric, instance-based learning method. This means it doesn't build a complex internal model but rather memorizes the training data directly.</p>
<p><b>Working Mechanism (Step-by-Step):</b></p>
<ul>
    <li><b>Calculate Distance:</b> When classifying a new, unseen data point, the algorithm computes the mathematical distance between this new point and all existing points in the training dataset (commonly using Euclidean distance).</li>
    <li><b>Identify Neighbors:</b> It then ranks the distances and identifies the 'K' closest data points in the feature space. These are the "nearest neighbors".</li>
    <li><b>Determine Class:</b> Finally, it assigns the new point to the class that represents the statistical mode (the majority vote) among those specific K neighbors.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> "Tell me who your neighbors are, and I'll tell you who you are." The algorithm asks the K closest points for a vote on what the new point should be.</div>""",

    "2m_q40": """<p><b>Formula:</b> <code>d(p, q) = &radic;(&Sigma; (q_i - p_i)&sup2;)</code> for <code>i=1</code> to <code>n</code>.</p>
<p><b>Definition:</b> This metric mathematically calculates the length of the shortest, straight-line path connecting two distinct points (p and q) in an n-dimensional feature space.</p>
<p><b>Applications in Machine Learning:</b></p>
<ul>
    <li>It is the most widely used default distance metric in various algorithms to quantify similarity or dissimilarity.</li>
    <li>Crucial for algorithms like <b>K-Nearest Neighbors (KNN)</b> to find closest points.</li>
    <li>Crucial for <b>K-Means clustering</b> to calculate the distance between data points and cluster centroids.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> It is just the Pythagorean theorem (a&sup2; + b&sup2; = c&sup2;) stretched out into as many dimensions as you have features!</div>""",

    "2m_q41": """<p><b>When K is too small (e.g., K=1):</b></p>
<ul>
    <li><b>Overfitting:</b> The model becomes overly sensitive to local noise and statistical outliers in the training data.</li>
    <li><b>Complex Boundaries:</b> The decision boundaries become highly jagged and overly complex, severely harming the model's ability to generalize to new data.</li>
</ul>
<p><b>When K is too large (e.g., K = N):</b></p>
<ul>
    <li><b>Underfitting:</b> The decision boundary becomes overly smooth and generalized.</li>
    <li><b>Loss of Detail:</b> The model fails to capture intricate, local patterns in the data. In extreme cases, it will simply predict the majority class of the entire dataset for every input.</li>
</ul>
<p><b>Conclusion:</b> A balanced, optimal K value must be selected, typically through an iterative process like cross-validation.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Small K is like asking just your one eccentric neighbor for advice (too noisy). Large K is like asking the entire city for advice (too generic). You want a balanced committee.</div>""",

    "2m_q42": """<p><b>Definition:</b> In Information Theory, Entropy is a fundamental metric used to mathematically quantify the level of uncertainty, impurity, or randomness within a given dataset or system.</p>
<p><b>Formula:</b> <code>H(S) = - &Sigma; (p_i * log2(p_i))</code></p>
<p><b>Variables:</b></p>
<ul>
    <li><code>S</code>: The specific set of data being evaluated.</li>
    <li><code>p_i</code>: The proportion (or relative frequency) of elements belonging to a specific class <code>i</code> within the set.</li>
</ul>
<p><b>Interpretation:</b></p>
<ul>
    <li><b>Entropy = 0:</b> The dataset is completely pure (all elements belong to one single class). There is zero uncertainty.</li>
    <li><b>Maximum Entropy:</b> The dataset has an equally distributed mix of all classes, representing maximum uncertainty and randomness.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> High entropy means high chaos (a messy room). Low entropy means high order (a perfectly organized drawer).</div>""",

    "2m_q43": """<p><b>Definition:</b> Information Gain measures the mathematically expected reduction in Entropy (or impurity) that is achieved by splitting a dataset according to a specific feature or attribute.</p>
<p><b>Role in Decision Trees:</b></p>
<ul>
    <li><b>Primary Criterion:</b> It acts as the primary evaluation criterion for selecting the best possible feature to split on at each internal node of the tree.</li>
    <li><b>Selection Process:</b> The algorithm iteratively evaluates all available features and calculates the Information Gain for each.</li>
    <li><b>Maximizing Purity:</b> It always selects the feature that yields the highest Information Gain, guaranteeing that the resulting child nodes are as homogeneous (pure) as possible.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Information Gain asks: "Which question can I ask right now that will clear up the most confusion?"</div>""",

    "2m_q44": """<p><b>Formula:</b> <code>Gini = 1 - &Sigma; (p_i)&sup2;</code></p>
<p><b>Definition:</b> This metric quantifies the statistical probability of a randomly chosen element from the set being incorrectly labeled, assuming it was randomly labeled according to the underlying distribution of labels in that subset.</p>
<p><b>Interpretation of Values:</b></p>
<ul>
    <li><b>Gini = 0:</b> Indicates perfect purity. Every item in the subset belongs to exactly one class.</li>
    <li><b>Higher Gini Values:</b> Indicate a highly diverse mix of classes within the node (high impurity).</li>
</ul>
<p><b>Usage:</b> It is the default impurity metric commonly used in CART (Classification and Regression Trees) algorithms due to its computational efficiency compared to Entropy.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Like Entropy, Gini measures a "messiness score." A Gini of 0 means the folder contains only one type of document—perfectly sorted.</div>""",

    "2m_q45": """<p><b>Formula:</b> <code>P(A|B) = [P(B|A) * P(A)] / P(B)</code></p>
<p><b>Term Definitions:</b></p>
<ul>
    <li><b>P(A|B) - Posterior Probability:</b> The calculated probability of class A occurring given that predictor B has been observed. This is what the model is trying to solve.</li>
    <li><b>P(B|A) - Likelihood:</b> The probability of observing predictor B given that class A is already true.</li>
    <li><b>P(A) - Prior Probability:</b> The initial, independent probability of class A occurring in the general population, before looking at any new evidence.</li>
    <li><b>P(B) - Marginal Probability (Evidence):</b> The overall independent probability of predictor B occurring across all classes.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> It updates your old beliefs (Prior) using new evidence (Likelihood) to give you a smart new conclusion (Posterior).</div>""",

    "2m_q46": """<p><b>The Core Assumption:</b></p>
<ul>
    <li>The classifier is termed "naive" because it makes a very strong, sweeping assumption of <b>conditional independence</b> among all features.</li>
</ul>
<p><b>What this means:</b></p>
<ul>
    <li>It fundamentally assumes that the presence, absence, or value of one particular feature is entirely unrelated to the presence or value of any other feature, given the class label.</li>
    <li>In mathematical terms, it treats all features as if they do not interact with each other.</li>
</ul>
<p><b>Reality vs. Practice:</b></p>
<ul>
    <li>This assumption is mathematically unrealistic in almost all real-world scenarios (e.g., in text, the word "machine" often interacts with the word "learning").</li>
    <li>Despite being "naive," the algorithm frequently delivers highly robust and competitive performance in complex applications like text classification and spam filtering.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> It's "naive" because it stubbornly believes every feature is a lone wolf that never communicates or interacts with the other features.</div>""",

    "2m_q47": """<p><b>Hyperplane:</b></p>
<ul>
    <li>A Hyperplane is the central geometric, linear decision boundary that mathematically separates the n-dimensional feature space into distinct regions corresponding to different classes.</li>
    <li>In 2D space, it is a line; in 3D, it is a flat plane.</li>
</ul>
<p><b>Support Vectors:</b></p>
<ul>
    <li>Support Vectors are the specific, critical data points from the training set that lie strictly closest to the hyperplane.</li>
    <li>They act as structural pillars: they directly dictate the exact position and orientation of the hyperplane.</li>
    <li>If these specific vectors were removed or slightly altered, the boundary's position would shift significantly. Changes to non-support vectors do not affect the hyperplane.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> The Hyperplane is the fence. The Support Vectors are the specific fence-posts holding it up. Only the posts matter for where the fence is placed!</div>""",

    "2m_q48": """<p><b>Hard Margin SVM:</b></p>
<ul>
    <li><b>Strict Enforcement:</b> It mathematically demands that the hyperplane must perfectly separate classes without allowing a single misclassification.</li>
    <li><b>Weakness:</b> It is highly susceptible to severe overfitting. Furthermore, it completely fails to converge if the training data is not perfectly linearly separable.</li>
</ul>
<p><b>Soft Margin SVM:</b></p>
<ul>
    <li><b>Flexibility:</b> It introduces a hyperparameter (denoted as C) and mathematical slack variables to intentionally permit a controlled degree of misclassification or margin violations.</li>
    <li><b>Strength:</b> By allowing a few errors during training, this approach drastically improves the model's robustness and generalization capabilities when dealing with noisy, overlapping real-world datasets.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Hard Margin is a strict zero-tolerance policy (breaks easily). Soft Margin is realistic and forgives a few mistakes to find a much better overall rule.</div>""",

    "2m_q49": """<p><b>The Problem:</b> Linear SVMs cannot draw boundaries for data that is intertwined or non-linearly separable in its original dimension.</p>
<p><b>The Purpose of Kernel Functions:</b></p>
<ul>
    <li>Kernel functions (like Radial Basis Function or Polynomial) mathematically compute the relationship (dot product) between data points as if they were projected into a transformed, much higher-dimensional feature space.</li>
    <li>In this higher dimension, previously intertwined data becomes linearly separable by a flat hyperplane.</li>
</ul>
<p><b>The "Kernel Trick":</b></p>
<ul>
    <li>The brilliant advantage is that Kernels allow the algorithm to perform this calculation computationally <i>without</i> ever explicitly transforming the data or storing the coordinates of that higher dimension.</li>
    <li>This enables SVMs to efficiently discover highly complex, non-linear decision boundaries.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Imagine throwing flat, mixed-up dots into the air (a higher dimension). While they are in the air, you slip a flat sheet of paper between them. The Kernel trick does this mathematically!</div>""",

    "2m_q50": """<p><b>Ensemble Approach:</b></p>
<ul>
    <li>Random Forests do not rely on a single model. They construct a multitude of individual decision trees during the training phase.</li>
    <li><b>Randomness injected:</b> Each individual tree is built independently using a bootstrapped (randomly sampled with replacement) subset of the training data. Furthermore, only a random subset of features is considered at each split.</li>
</ul>
<p><b>Voting Structure:</b></p>
<ul>
    <li>During the prediction phase for classification, every individual tree independently processes the input and outputs a predicted class label.</li>
    <li><b>Aggregation:</b> The final classification output of the entire Random Forest is determined by taking a democratic majority vote among all the trees. The class with the most votes wins.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> It's a "wisdom of the crowd" approach. One tree might be wrong, but thousands of slightly different trees voting together will usually find the right answer.</div>""",

    "2m_q51": """<p><b>Three Popular Boosting Algorithms:</b></p>
<ol>
    <li><b>AdaBoost (Adaptive Boosting):</b> The foundational algorithm. It builds models sequentially, where each new model aggressively adjusts the weights of misclassified instances from the previous model to focus on the hardest cases.</li>
    <li><b>Gradient Boosting Machine (GBM):</b> A robust approach that builds trees sequentially by minimizing a specific, differentiable loss function utilizing the mathematical principles of gradient descent.</li>
    <li><b>XGBoost (Extreme Gradient Boosting):</b> A highly optimized, modern, scalable, and heavily regularized software implementation of gradient boosting. It executes much faster and frequently yields state-of-the-art performance in competitions.</li>
</ol>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Boosting is like a relay race where each runner tries to fix the specific mistakes made by the runner who handed them the baton.</div>""",

    "2m_q52": """<p><b>Formulas and Definitions:</b></p>
<ul>
    <li><b>Precision:</b> <code>TP / (TP + FP)</code>
        <br><i>Definition:</i> Measures accuracy of positive predictions. (Out of all the instances the model <i>claimed</i> were positive, how many were actually positive?)</li>
    <li><b>Recall:</b> <code>TP / (TP + FN)</code>
        <br><i>Definition:</i> Measures the ability to find positive instances. (Out of all the <i>actual</i> positive instances, how many did the model successfully find?)</li>
    <li><b>F1-Score:</b> <code>2 * (Precision * Recall) / (Precision + Recall)</code>
        <br><i>Definition:</i> The harmonic mean of Precision and Recall. It provides a single, balanced metric of performance, which is especially crucial when working with highly imbalanced datasets where accuracy is misleading.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Precision is "quality control" (no false alarms). Recall is a "dragnet search" (don't miss anything). F1 is the compromise between them.</div>""",

    "3m_q1": """<p><b>1. Supervised Learning:</b></p>
<ul>
    <li><b>Data Requirement:</b> Strictly relies on fully labeled training datasets (every input instance must be paired with its desired output/target variable).</li>
    <li><b>Characteristic:</b> The objective is to train a model to mathematically map inputs to correct outputs, enabling it to generalize and make predictions on unseen data (e.g., Classification, Regression).</li>
</ul>
<p><b>2. Unsupervised Learning:</b></p>
<ul>
    <li><b>Data Requirement:</b> Utilizes completely unlabeled datasets. The system is given no predefined "correct" answers or target variables.</li>
    <li><b>Characteristic:</b> The model's primary goal is autonomous discovery. It explores the data to find hidden structures, inherent patterns, or natural groupings (e.g., Clustering, Dimensionality Reduction).</li>
</ul>
<p><b>3. Reinforcement Learning:</b></p>
<ul>
    <li><b>Data Requirement:</b> Does not use static datasets. It requires a dynamic environment where an agent can perform state-based actions.</li>
    <li><b>Characteristic:</b> An autonomous agent learns to make a sequence of decisions by interacting with the environment. It receives direct feedback via numerical rewards or penalties, adjusting its policy over time to maximize long-term cumulative reward.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Supervised is learning with a teacher (labeled). Unsupervised is independent self-discovery (unlabeled). Reinforcement is learning via trial-and-error with treats and punishments (rewards/penalties).</div>""",

    "3m_q2": """<p><b>Stage 1: Data Collection</b></p>
<ul>
    <li><b>Focus:</b> The foundational stage of building a comprehensive dataset.</li>
    <li><b>Actions:</b> It involves strategically sourcing, aggregating, and extracting raw data from diverse external sources (e.g., SQL databases, REST APIs, web scraping, or IoT sensor logs).</li>
</ul>
<p><b>Stage 2: Data Preparation and Cleaning</b></p>
<ul>
    <li><b>Focus:</b> Enhancing structural data quality before modeling.</li>
    <li><b>Actions:</b> Practitioners meticulously handle missing values (via imputation or deletion), identify and remove duplicate records, correct structural formatting inconsistencies, and systematically address statistical outliers.</li>
</ul>
<p><b>Stage 3: Exploratory Data Analysis (EDA)</b></p>
<ul>
    <li><b>Focus:</b> Deep investigation and pattern discovery.</li>
    <li><b>Actions:</b> Data scientists leverage statistical summaries and visual tools (like scatter plots, histograms, and correlation matrices) to investigate data distributions, uncover underlying patterns, and identify mathematical relationships between variables prior to formal model selection.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Get the data (Collect), wash the data (Clean), look closely at the data (Explore).</div>""",

    "3m_q3": """<p><b>Importance of Data Cleaning:</b></p>
<ul>
    <li>High-quality data is the fundamental bedrock of robust machine learning.</li>
    <li>The strict principle of "garbage in, garbage out" dictates that feeding noisy, corrupted, or inconsistent data into an algorithm will inevitably result in poor model accuracy and unreliable predictions. Cleaning ensures overall pipeline integrity.</li>
</ul>
<p><b>Strategies for Handling Missing Values:</b></p>
<ul>
    <li><b>Strategy 1: Statistical Imputation</b>
        <br>Systematically replacing missing values with calculated estimates (e.g., the mean, median, or mode of that specific column). This is highly effective because it preserves dataset size while maintaining the general statistical distribution.</li>
    <li><b>Strategy 2: Deletion (Listwise/Pairwise)</b>
        <br>Entirely removing a row or column if it contains an overwhelmingly high percentage of missing data. While this prevents artificial bias created by fake estimates, it must be used cautiously to avoid severe loss of valuable information.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> If a puzzle piece is missing, you can either paint a cardboard replacement that roughly fits (Imputation) or just throw that part of the puzzle away entirely (Deletion).</div>""",

    "3m_q4": """<p><b>Definition of EDA:</b></p>
<ul>
    <li>Exploratory Data Analysis (EDA) is an iterative phase where analysts use descriptive statistics and visual techniques to systematically summarize the fundamental characteristics of a dataset.</li>
    <li>The goal is to intuitively understand the data's structure, uncover underlying patterns, and formulate hypotheses before applying predictive models.</li>
</ul>
<p><b>Role of Data Visualization in EDA:</b></p>
<ul>
    <li><b>Histograms:</b> Effectively illustrate the frequency distribution, spread, and statistical skewness of continuous variables.</li>
    <li><b>Box Plots:</b> Provide a clear, condensed visual summary of a variable's central tendency (median), spread (interquartile range), and clearly flag mathematical outliers.</li>
    <li><b>Scatter Plots:</b> Are highly instrumental in plotting pairs of continuous features to identify linear or non-linear correlations.</li>
</ul>
<p><b>Outcome:</b> By translating raw numbers into visual formats, EDA enables practitioners to instantly detect anomalies, verify structural assumptions, and inform downstream feature engineering.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> EDA is like scanning the blueprint before building the house. Visualizations are the x-ray glasses that reveal the hidden skeleton of your raw data matrix.</div>""",

    "3m_q5": """<p><b>Feature Engineering:</b></p>
<ul>
    <li><b>Role:</b> The creative process of mathematically transforming existing features or constructing entirely new ones to better expose underlying patterns to the learning algorithm.</li>
    <li><b>Examples:</b> Creating polynomial combinations, extracting the "day of the week" from a raw date stamp, or applying logarithmic transformations to fix skewed data.</li>
    <li><b>Goal:</b> To drastically enhance the model's predictive power by providing richer, more informative inputs.</li>
</ul>
<p><b>Feature Selection:</b></p>
<ul>
    <li><b>Role:</b> The systematic reduction process aimed at identifying and retaining <i>only</i> the most relevant, original features while discarding redundant, noisy, or irrelevant ones.</li>
    <li><b>Examples:</b> Dropping features with low correlation to the target, or using recursive feature elimination.</li>
    <li><b>Goal:</b> To simplify the model architecture, reduce training time, combat the curse of dimensionality, and mitigate overfitting.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Feature Engineering is <i>creating</i> new tools from raw materials. Feature Selection is <i>decluttering</i> the toolbox to only keep what you actually need.</div>""",

    "3m_q6": """<p><b>The Mathematical Limitation:</b></p>
<ul>
    <li>The vast majority of machine learning optimization techniques (like gradient descent) and distance metrics strictly require continuous numerical input matrices to perform their calculations.</li>
    <li>Raw categorical data consists of text strings or discrete labels (e.g., "Red", "Green", "Blue"). Mathematical equations cannot process text strings directly.</li>
</ul>
<p><b>The Solution (Encoding):</b></p>
<ul>
    <li><b>Label Encoding:</b> Assigns a unique integer to each category. This is useful for ordinal data where an inherent ranking exists (e.g., Low=1, Medium=2, High=3).</li>
    <li><b>One-Hot Encoding:</b> Creates separate binary dummy variables (0 or 1) for each category. This prevents the model from mathematically assuming false ordinality in nominal data.</li>
</ul>
<p><b>Conclusion:</b> Failing to mathematically translate qualitative text into quantitative numbers will result in immediate execution errors or severe misinterpretations by the algorithm.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Algorithms only speak the language of numbers. Encoding is simply hiring a translator to convert text labels into numerical values so the math can work.</div>""",

    "3m_q7": """<p><b>Feature Scaling (Min-Max Scaling):</b></p>
<ul>
    <li><b>Method:</b> Linearly transforms numeric features so they fall within a specific, strictly bounded standard range (most commonly between 0 and 1).</li>
    <li><b>Best for:</b> Algorithms that do not make structural assumptions about the statistical distribution of the data (e.g., Neural Networks, K-Nearest Neighbors).</li>
</ul>
<p><b>Feature Normalization (Standardization/Z-score):</b></p>
<ul>
    <li><b>Method:</b> Transforms the data distribution to geometrically center around a mean of zero, with a standard deviation of exactly one.</li>
    <li><b>Best for:</b> Optimization algorithms like Gradient Descent (used in SVMs and Logistic Regression). It handles statistical outliers far better than basic scaling.</li>
</ul>
<p><b>Why they are applied:</b></p>
<ul>
    <li>If unscaled, features with naturally massive magnitudes (e.g., house prices in millions) will disproportionately dominate the model's error function or distance calculations.</li>
    <li>Scaling ensures fair, balanced learning across all variables, regardless of their original native units.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> If age is 25 and salary is 80,000, the math thinks salary is infinitely more important. Scaling forces both metrics onto a level playing field so the model listens to both equally.</div>""",

    "3m_q8": """<p><b>Concept of Model Training:</b></p>
<ul>
    <li>Model training represents the central, computationally intensive phase where a chosen theoretical algorithm is actively exposed to the prepared training dataset.</li>
    <li>During this phase, the algorithm iteratively adjusts its internal mathematical parameters (such as weights and biases in a neural network, or coefficients in regression).</li>
    <li>The mechanism relies on continuously comparing its current predictions against the actual ground-truth labels and minimizing a predefined error/loss function.</li>
</ul>
<p><b>Significance in the Lifecycle:</b></p>
<ul>
    <li>This is the specific phase where the model essentially "learns" the complex mathematical mapping between independent input features and the dependent target variable.</li>
    <li>The rigor and success of this phase directly dictate the model's ultimate capacity to generalize its learned rules to accurately predict outcomes on completely new, unseen data.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Model training is the "study session." The model reviews flashcards (data), makes a guess, checks the answer key, and updates its brain to get closer to the right answer next time.</div>""",

    "3m_q9": """<p><b>Strategy 1: Train-Test Split</b></p>
<ul>
    <li><b>Process:</b> The complete dataset is randomly partitioned into two mutually exclusive subsets: a training set (typically 70-80%) and a distinct testing set (20-30%).</li>
    <li><b>Purpose:</b> The testing set is held out to simulate real-world, unseen data. Evaluating the model on this subset provides a baseline estimate of generalization error and exposes obvious overfitting.</li>
</ul>
<p><b>Strategy 2: K-Fold Cross-Validation</b></p>
<ul>
    <li><b>Process:</b> The dataset is divided into 'K' equally sized, mutually exclusive folds. The model is trained and evaluated K separate times. In each iteration, it trains on K-1 folds and validates on the single remaining fold.</li>
    <li><b>Purpose:</b> The final metric is the mathematical average across all K iterations. This provides a significantly more robust, unbiased, and reliable estimate of performance, particularly crucial when working with smaller datasets.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Train-Test Split is taking one big final exam. K-Fold is taking 5 different quizzes throughout the semester to ensure you actually understand the material, not just got lucky once.</div>""",

    "3m_q10": """<p><b>Independent Predictor Variables (Features / X):</b></p>
<ul>
    <li>These are the measurable attributes, characteristics, or inputs of the dataset that the model utilizes to perform its calculation.</li>
    <li>These are the known variables that you can observe prior to making a prediction.</li>
</ul>
<p><b>Dependent Target Variable (Label / Output / y):</b></p>
<ul>
    <li>This is the specific outcome or objective value that the model is actively attempting to forecast, classify, or predict based on the independent variables.</li>
</ul>
<p><b>Concrete Example: Medical Diagnosis</b></p>
<ul>
    <li><b>Independent Variables:</b> Patient metrics such as age, resting blood pressure, cholesterol levels, and family history.</li>
    <li><b>Dependent Variable:</b> The final diagnosis (e.g., a binary classification of whether the patient actually has heart disease: Yes or No). The algorithm maps how the patient metrics mathematically influence this final diagnosis.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Independent variables are the "Clues". The dependent variable is the "Mystery solved".</div>"""
}

for item in data:
    q_id = item["id"]
    if q_id in rewrites:
        item["answer_html"] = rewrites[q_id]

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
print("Processing complete")
