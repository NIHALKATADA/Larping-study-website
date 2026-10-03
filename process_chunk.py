import json

new_html_map = {
    "3m_q11": """<p>Efficient data collection serves as the foundation of any machine learning pipeline. It directly impacts downstream efficiency in the following ways:</p>
<ul>
  <li><b>Data Quality and Quantity:</b> High-quality, representative data reduces the significant overhead usually required for data cleaning and preprocessing.</li>
  <li><b>Optimized Fetching Strategies:</b> Techniques like incremental loading or real-time streaming prevent downstream components from becoming bottlenecked.</li>
  <li><b>Final Model Performance:</b> Seamless data flow ultimately leads to improved predictive accuracy, better model generalization, and enhanced reliability in deployment.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> High-quality data IN = Less cleaning time + Faster processing + Better predictions OUT (Garbage In, Garbage Out).</div>""",

    "3m_q12": """<p>Machine learning has evolved significantly and is structured into distinct paradigms:</p>
<ul>
  <li><b>Historical Evolution:</b> Began with early logical rules and symbolic AI, progressed through statistical learning methods, and culminated in advanced deep neural networks for complex pattern recognition.</li>
  <li><b>Structural Taxonomy:</b> Primarily divided into four categories based on labeled feedback:
    <ul>
      <li><b>Supervised Learning:</b> Learning from labeled data to predict outcomes.</li>
      <li><b>Unsupervised Learning:</b> Finding hidden patterns and structures in completely unlabeled data.</li>
      <li><b>Semi-supervised Learning:</b> Utilizing a small amount of labeled data combined with a large amount of unlabeled data.</li>
      <li><b>Reinforcement Learning:</b> Learning optimal actions and policies through trial and error based on rewards and penalties.</li>
    </ul>
  </li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of the taxonomy as teaching styles: Supervised (teacher with answers), Unsupervised (student explores alone), Semi-supervised (teacher gives a few hints), and Reinforcement (learning to ride a bike by falling and succeeding).</div>""",

    "3m_q13": """<p>Computing statistical summaries is a critical first step in Exploratory Data Analysis (EDA) because it provides a rapid numerical overview of the dataset:</p>
<ul>
  <li><b>Central Tendency and Dispersion:</b> Metrics like mean, median, standard deviation, and quartiles describe how data is centered and spread out.</li>
  <li><b>Anomaly Detection:</b> Helps quickly highlight potential anomalies and identify extreme outliers that could skew models.</li>
  <li><b>Scale Understanding:</b> Reveals the scale and range of different features, which is essential for determining next steps.</li>
  <li><b>Preprocessing Decisions:</b> Allows data scientists to make informed choices on necessary preprocessing steps, such as normalization, standardization, or missing value imputation, prior to deeper analysis.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Statistical summaries are like the "vital signs" of a dataset—checking the pulse (mean/median) and temperature (variance) before starting surgery (modeling).</div>""",

    "3m_q14": """<p>Raw, unstructured, or uncleaned datasets cannot be directly utilized by standard machine learning algorithms for several critical reasons:</p>
<ul>
  <li><b>Mathematical Requirement:</b> Algorithms fundamentally rely on well-structured, numerical tabular data to perform mathematical calculations.</li>
  <li><b>Incompatible Elements:</b> Raw data frequently contains text, noise, inconsistencies, infinite entries, or missing fields which algorithms cannot mathematically process.</li>
  <li><b>Consequences of Skipping Cleaning:</b> If used without cleaning, the algorithms will either crash completely or produce highly inaccurate, "garbage" outputs.</li>
</ul>
<p>Therefore, rigorous preprocessing and data wrangling are mandatory prerequisites for reliable modeling.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Algorithms only speak "Math." Feeding them uncleaned raw data is like trying to feed a diesel engine raw crude oil—it will break down.</div>""",

    "3m_q15": """<p>The mathematical formulation for a Simple Linear Regression model is <code>y = &beta;0 + &beta;1x + &epsilon;</code>. The terms represent the following:</p>
<ul>
  <li><b>y (Dependent Variable):</b> The target variable being predicted.</li>
  <li><b>x (Independent Variable):</b> The predictor feature used to make the estimate.</li>
  <li><b>&beta;0 (Y-intercept):</b> The expected value of y when x is exactly zero.</li>
  <li><b>&beta;1 (Slope Coefficient):</b> Indicates the expected change in y for a 1-unit change in x.</li>
  <li><b>&epsilon; (Error Term):</b> Accounts for the variance in y that cannot be explained by the linear relationship with x.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> It's the classic line equation (y = mx + c) adapted for statistics, where &beta;1 is the slope (m), &beta;0 is the intercept (c), and &epsilon; is the unavoidable real-world error.</div>""",

    "3m_q16": """<p>Multiple Linear Regression is an extension of simple linear regression designed to model the relationship between one continuous dependent variable and two or more independent variables. This allows for a more realistic representation of complex real-world phenomena.</p>
<p>The algebraic equation for a model with <i>n</i> independent variables is:</p>
<code>y = &beta;0 + &beta;1x1 + &beta;2x2 + ... + &beta;nxn + &epsilon;</code>
<ul>
  <li><b>&beta; coefficients:</b> Each &beta; represents the independent effect of its corresponding feature on the target variable, assuming all other features are held constant.</li>
  <li><b>&epsilon; (Error Term):</b> Accounts for the random, unexplained error in the prediction.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Multiple regression is just simple regression scaled up. Instead of one slope for one feature, every feature gets its own dedicated slope (&beta;).</div>""",

    "3m_q17": """<p>In linear regression, analyzing the residual error is crucial for evaluating model performance:</p>
<ul>
  <li><b>Mathematical Definition:</b> The difference between the actual observed value and the value predicted by the model (formula: <code>e = y - &#375;</code>).</li>
  <li><b>Geometric Interpretation:</b> Represents the vertical distance from a specific data point on a scatter plot to the fitted regression line.</li>
  <li><b>Ideal Behavior:</b> Residuals should be randomly scattered around zero. This random distribution indicates that the model's linear assumptions hold true and the underlying trend is adequately captured.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Residuals are the "leftovers." Geometrically, they are the vertical drop from the actual dot down to the prediction line.</div>""",

    "3m_q18": """<p>Ordinary Least Squares (OLS) is a widely used estimation method in linear regression designed to find the optimal line of best fit:</p>
<ul>
  <li><b>Objective Function:</b> OLS determines optimal regression coefficients by minimizing the sum of the squared residuals. Mathematically, it minimizes: <code>&Sigma;(yi - &#375;i)&sup2;</code>.</li>
  <li><b>Why Square the Errors?</b> Squaring the residuals ensures that positive and negative errors do not cancel each other out.</li>
  <li><b>Penalty on Outliers:</b> The squaring process places a significantly heavier mathematical penalty on larger errors, forcing the line to fit as closely as possible to all data points.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> OLS is like stretching rubber bands from every point to a stick (the line). Squaring the errors pulls the stick harder towards points that are further away.</div>""",

    "3m_q19": """<p>The Mean Squared Error (MSE) computes the average of the squared mathematical differences between predicted values and actual observed values. Its role in optimization includes:</p>
<ul>
  <li><b>Primary Cost Function:</b> It serves as the primary cost function, denoted as J(&theta;), when optimizing regression models.</li>
  <li><b>Guiding Optimization:</b> Algorithms like Gradient Descent use this function to iteratively adjust the model's weights and biases to find the lowest possible J(&theta;).</li>
  <li><b>Indicator of Fit:</b> A lower MSE indicates a better-fitting model, demonstrating that the algorithm successfully found optimal parameters.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> MSE is the "scoreboard" for the model. The goal of the algorithm is to get the lowest score possible by adjusting its weights.</div>""",

    "3m_q20": """<p>Gradient Descent is an iterative optimization algorithm used to find the optimal slope and intercept by minimizing the model's cost function:</p>
<ul>
  <li><b>Calculating the Gradient:</b> It calculates the partial derivatives (the gradient) of the cost function with respect to each parameter, which indicates the direction of steepest ascent.</li>
  <li><b>Parameter Updates:</b> To minimize the cost, it takes small steps in the exact opposite direction of the gradient.</li>
  <li><b>Learning Rate:</b> The size of these update steps is controlled by a parameter called the learning rate.</li>
  <li><b>Convergence:</b> This iterative process repeats until the parameters reach the global minimum cost, representing the optimal fit.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Imagine being blindfolded on a hill. You feel the slope with your feet (gradient) and take a step downhill (opposite direction) until you reach the flat valley (minimum).</div>""",

    "3m_q21": """<p>The learning rate (&alpha;) in Gradient Descent is a hyperparameter that determines the step size taken at each iteration toward the cost function's minimum:</p>
<ul>
  <li><b>Too High:</b> The algorithm takes steps that are too large, potentially overshooting the minimum entirely. This can cause the optimization to diverge or oscillate wildly without settling.</li>
  <li><b>Too Low:</b> The step sizes become minuscule. This leads to exceedingly slow convergence times, high computational cost, and raises the risk of getting stuck in suboptimal local minima.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Goldilocks rule: Too high, you jump over the valley. Too low, it takes a lifetime to walk down. It must be "just right."</div>""",

    "3m_q22": """<p>Polynomial Regression models the relationship between the independent variable x and the dependent variable y as an nth degree polynomial (e.g., <code>y = &beta;0 + &beta;1x + &beta;2x&sup2;</code>):</p>
<ul>
  <li><b>Introducing Curves:</b> By adding higher-degree terms like squares (x&sup2;) and cubes (x&sup3;), the model introduces curves into the fitted line or decision boundary.</li>
  <li><b>Capturing Non-linearity:</b> This flexibility allows the model to accurately capture and fit non-linear, complex data trends.</li>
  <li><b>Reducing Underfitting:</b> It prevents the severe underfitting that occurs when attempting to apply a simple straight line to inherently curved data.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> When the data looks like a U-shape, a straight ruler won't work. Polynomial features let you bend the ruler to fit the curve.</div>""",

    "3m_q23": """<p>Despite its ability to fit complex, non-linear curves to data, Polynomial Regression is mathematically classified as a linear model due to the following reason:</p>
<ul>
  <li><b>Linearity in Parameters:</b> The regression equation remains completely linear with respect to its learnable parameters (the &beta; coefficients). The relationship between these parameters and the output y is strictly additive and linear.</li>
  <li><b>Feature Engineering:</b> While the input features themselves are transformed non-linearly (e.g., squaring x to create a new feature x&sup2;), the model simply treats these transformed terms as new independent variables.</li>
  <li><b>Conclusion:</b> Under the hood, the model is merely performing standard multiple linear regression on engineered polynomial features.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> It is called a "linear" model because the weights (&beta;) are linearly added together, even if the inputs (x) are squared or cubed.</div>""",

    "3m_q24": """<p>Overfitting occurs when a regression model becomes overly complex, memorizing not only the underlying data patterns but also the random noise. This results in excellent training performance but poor generalization to unseen data. It is typically detected by a large gap between high training accuracy and low validation accuracy.</p>
<p>Two highly practical techniques to prevent it are:</p>
<ul>
  <li><b>Cross-validation:</b> Using techniques like K-Fold to rigorously evaluate the model on different subsets of data, ensuring robust performance evaluation.</li>
  <li><b>Regularization:</b> Applying L1 (Lasso) or L2 (Ridge) penalties to the loss function, which constrains the model's weights and penalizes excessive complexity.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Overfitting is like memorizing the answers to a practice test but failing the final exam because you didn't learn the actual concepts.</div>""",

    "3m_q25": """<p>Underfitting occurs when a machine learning model is far too simplistic to capture the underlying structures and trends in the dataset, leading to high bias. Its primary characteristics are:</p>
<ul>
  <li><b>Root Causes:</b> Using a model with insufficient complexity (e.g., a straight line for curved data), providing inadequate or poorly engineered features, or applying excessive regularization penalties.</li>
  <li><b>Error Profile:</b> Unlike overfitting (which has low training error but high validation error), underfitting is distinctly characterized by <b>high training error AND high validation error</b>. This indicates the model failed to learn the data entirely.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Underfitting is like studying only the table of contents for an exam—you perform poorly on both the practice tests (training) and the final exam (validation).</div>""",

    "3m_q26": """<p>The Bias-Variance tradeoff describes the fundamental conflict between two primary sources of error in predictive models:</p>
<ul>
  <li><b>Bias:</b> The error introduced by making overly simplistic assumptions about the data. High bias leads to underfitting.</li>
  <li><b>Variance:</b> The error introduced by the model's excessive sensitivity to small fluctuations and noise in the training data. High variance leads to overfitting.</li>
  <li><b>Influence of Complexity:</b> As model complexity increases, bias typically decreases (it fits the data better), but variance increases (it starts memorizing noise).</li>
</ul>
<p>The goal of the tradeoff is to find the optimal "sweet spot" of complexity that minimizes total overall error on unseen data.</p>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> High Bias = Too rigid (won't bend to learn). High Variance = Too flexible (bends too much to fit noise). You want a model with just the right flexibility.</div>""",

    "3m_q27": """<p>Regularization is a powerful technique designed to prevent overfitting by intentionally penalizing model complexity:</p>
<ul>
  <li><b>Penalty Introduction:</b> It introduces a specific penalty term into the model's loss function based on the magnitude of the model's coefficients (weights).</li>
  <li><b>Balancing Act:</b> Without regularization, models assign excessively large weights to perfectly fit training noise. The penalty forces the optimization algorithm to balance minimizing traditional error against keeping the weights small.</li>
  <li><b>Result:</b> This discourages overly complex models, yielding a simpler, smoother model that generalizes far better to unseen data.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Regularization acts like a strict budget for model weights—it charges a "tax" for making weights too large, forcing the model to stay simple.</div>""",

    "3m_q28": """<p>Ridge (L2) and Lasso (L1) regression combat overfitting by applying different mathematical penalties to the weights:</p>
<ul>
  <li><b>Ridge (L2):</b> Adds a penalty strictly proportional to the sum of the <b>squared weights</b> (<code>&lambda;&Sigma;w&sup2;</code>). This uniformly shrinks coefficients towards zero, making them small, but rarely forces them to exactly zero.</li>
  <li><b>Lasso (L1):</b> Adds a penalty proportional to the sum of the <b>absolute values</b> of the weights (<code>&lambda;&Sigma;|w|</code>). This constraint can actively force the weights of less important features to exactly zero.</li>
  <li><b>Impact on Weights:</b> Ridge retains all features with diminished impact, while Lasso aggressively creates sparse models by entirely eliminating features.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Ridge (L2) <b>shrinks</b> all weights evenly. Lasso (L1) <b>snips</b> away useless weights by forcing them to absolute zero.</div>""",

    "3m_q29": """<p>Lasso (L1) performs automatic feature selection due to the geometric shape of its constraint region, unlike Ridge (L2):</p>
<ul>
  <li><b>Lasso (L1) Geometry:</b> Its penalty term creates a constraint region shaped like a diamond with sharp corners located directly on the axes. When the loss function contours expand, they frequently intersect this diamond exactly at a corner, forcing that specific coefficient to exactly zero (eliminating the feature).</li>
  <li><b>Ridge (L2) Geometry:</b> Its penalty creates a circular constraint region without sharp corners. Intersections typically occur off the axes, shrinking the coefficients continuously without ever forcing them perfectly to zero.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Think of Lasso as a diamond with pointy corners on the graph axes. Hitting a corner means a coordinate is zero (feature deleted). Ridge is a circle, with no corners to hit.</div>""",

    "3m_q30": """<p>Mean Absolute Error (MAE) and Mean Squared Error (MSE) measure prediction errors differently based on their mathematical formulations:</p>
<ul>
  <li><b>MAE Formula:</b> <code>(1/n) &Sigma;|yi - &#375;i|</code>. It calculates the average absolute distance between predictions and actuals.</li>
  <li><b>MSE Formula:</b> <code>(1/n) &Sigma;(yi - &#375;i)&sup2;</code>. It calculates the average of the squared distances.</li>
  <li><b>Handling Outliers:</b> Because MSE squares the errors, it disproportionately penalizes large errors (outliers), pulling the model aggressively to correct them. MAE treats all errors linearly, making it far more robust and stable when a dataset contains extreme outliers.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> MSE acts like a magnifying glass for big errors (an error of 10 becomes 100). MAE treats an error of 10 exactly as 10.</div>""",

    "3m_q31": """<p><b>Root Mean Squared Error (RMSE)</b> is mathematically defined as the square root of the Mean Squared Error (MSE): <code>&radic;((1/n) &Sigma;(yi - &#375;i)&sup2;)</code>.</p>
<p>Its primary interpretive advantage lies in dimensionality:</p>
<ul>
  <li>The square root operation transforms the error metric back into the exact same units as the original dependent target variable.</li>
  <li>For instance, if predicting house prices, MSE outputs "squared dollars" (which is difficult to interpret). RMSE outputs straightforward "dollars," making it intuitive and accessible for stakeholders assessing average error magnitude.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> RMSE brings the error back to reality. It unpacks the square made by MSE so you can talk in real-world units (like dollars or meters) again.</div>""",

    "3m_q32": """<p>The R&sup2; (R-squared) goodness-of-fit metric is used to evaluate regression models, but standard R&sup2; has limitations in multiple regression contexts:</p>
<ul>
  <li><b>Standard R&sup2;:</b> Measures the proportion of total variance in the dependent variable explained by the model (ranging from 0 to 1). However, it mechanically increases or stays the same when any new feature is added, even if that feature is entirely irrelevant.</li>
  <li><b>Adjusted R&sup2;:</b> Resolves this flaw by incorporating a mathematical penalty for adding unnecessary independent variables. It only increases if the new variable improves the model more than would be expected by chance, providing a realistic evaluation of complex models.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Standard R&sup2; is like a hoarder—it values everything you throw at it. Adjusted R&sup2; acts like a minimalist—it penalizes you for keeping useless clutter.</div>""",

    "3m_q33": """<p>The Sigmoid activation function plays a foundational role in binary classification by converting outputs into valid probabilities:</p>
<ul>
  <li><b>Mathematical Formula:</b> <code>&sigma;(z) = 1 / (1 + e^(-z))</code></li>
  <li><b>Purpose:</b> It takes any real-valued continuous number (z) from negative infinity to positive infinity and maps it smoothly onto an S-curve bounded strictly between 0 and 1.</li>
  <li><b>Probability Interpretation:</b> Because the output is constrained between 0 and 1, it directly represents a valid statistical probability. This makes it essential for algorithms like Logistic Regression.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> The Sigmoid function is a "probability squasher." It takes any wild number (like -400 or +1000) and safely squashes it into a neat percentage between 0% and 100%.</div>""",

    "3m_q34": """<p>In Logistic Regression, binary decision boundaries translate continuous probabilities into strict categorical predictions:</p>
<ul>
  <li><b>Probability Output:</b> The model first outputs a continuous probability score strictly between 0 and 1, indicating the likelihood of an instance belonging to the positive class.</li>
  <li><b>Applying a Threshold:</b> A specific threshold (commonly set at 0.5) is applied. If the probability <code>p &ge; 0.5</code>, the instance is classified as class 1; if <code>p &lt; 0.5</code>, it is classified as class 0.</li>
  <li><b>Decision Boundary:</b> This threshold logically establishes a distinct linear hyperplane in the feature space that perfectly separates the two predicted classes.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> The threshold acts as a bouncer at a club. If your probability score is 0.5 or higher, you enter the "Class 1" room. Lower, you go to "Class 0."</div>""",

    "3m_q35": """<p>The single-sample log-loss (binary cross-entropy) formula is essential for optimizing classification models, as MSE is fundamentally flawed for this task:</p>
<ul>
  <li><b>Log-Loss Formula:</b> <code>Loss = -[y*log(p) + (1-y)*log(1-p)]</code>, where y is the true label and p is the predicted probability.</li>
  <li><b>Why MSE Fails:</b> Using Mean Squared Error (MSE) with a sigmoid activation function produces a non-convex loss surface.</li>
  <li><b>The Local Minima Problem:</b> A non-convex surface features undulating terrain with multiple local minima. Gradient Descent frequently gets trapped in these local minima, completely failing to locate the true global minimum and rendering the model useless.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Using MSE for classification is like dropping a ball in a bumpy egg carton—it gets stuck in random dips (local minima). Log-loss is like a smooth bowl, ensuring the ball always rolls to the true bottom.</div>""",

    "3m_q36": """<p>The K-Nearest Neighbors (KNN) classification algorithm operates through four straightforward, step-by-step mechanics:</p>
<ul>
  <li><b>Step 1 (Select K):</b> Define the hyperparameter 'K', which dictates the exact number of neighboring data points to consider.</li>
  <li><b>Step 2 (Calculate Distances):</b> For any new unseen test instance, calculate the geometric spatial distance (e.g., Euclidean) between it and all points in the training dataset.</li>
  <li><b>Step 3 (Find Neighbors):</b> Sort all calculated distances in ascending order to isolate the 'K' closest training points.</li>
  <li><b>Step 4 (Majority Vote):</b> Assign the new test instance to the statistical majority class among those K nearest neighbors.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> KNN is just "guilt by association." If you move into a neighborhood where 4 out of 5 closest neighbors own a dog, the algorithm predicts you own a dog too.</div>""",

    "3m_q37": """<p>The Euclidean distance formula quantifies the geometric similarity between points in n-dimensional space, which is critical for KNN predictions:</p>
<ul>
  <li><b>Formula:</b> <code>d = &radic;(&Sigma;(xi - yi)&sup2;)</code> from i=1 to n.</li>
  <li><b>Purpose in KNN:</b> It precisely measures the spatial "closeness" between a new test instance and all existing historical training instances.</li>
  <li><b>Foundation of Prediction:</b> By calculating these straight-line distances, the algorithm objectively determines which data points are most similar, forming the entirely distance-based foundation for its final classification.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Euclidean distance is simply the Pythagorean theorem (a&sup2; + b&sup2; = c&sup2;) scaled up for multiple dimensions to find the shortest straight-line distance between two dots.</div>""",

    "3m_q38": """<p>Selecting the optimal value for the hyperparameter 'K' in K-Nearest Neighbors drastically dictates model generalization and performance:</p>
<ul>
  <li><b>Too Small (e.g., K=1):</b> The model becomes highly sensitive to individual noisy data points. This creates fragmented, highly irregular decision boundaries, leading to high variance and severe overfitting.</li>
  <li><b>Too Large:</b> Decision boundaries become overly smoothed and heavily biased toward the dataset's overall majority class. This ignores localized patterns, leading to high bias and underfitting.</li>
  <li><b>Finding Balance:</b> The optimal K (usually found via cross-validation) strikes a careful balance, ensuring robustness against noise while preserving true local structural patterns.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Small K = Listening only to your weird next-door neighbor (overfitting). Huge K = Asking the entire city for advice and losing local context (underfitting).</div>""",

    "3m_q39": """<p>In Information Theory, Entropy is a fundamental metric used to measure the level of impurity, chaos, or uncertainty within a specific dataset:</p>
<ul>
  <li><b>Mathematical Expression:</b> <code>H(S) = -&Sigma;(p_i * log2(p_i))</code>, where p_i represents the proportion of examples belonging to class i.</li>
  <li><b>Meaning of Zero Entropy:</b> An entropy value of exactly zero signifies a state of perfect purity and zero uncertainty. </li>
  <li><b>Implication for Trees:</b> A zero entropy node means that every single example in that specific subset identically belongs to exactly one single class, making any further mathematical splits entirely unnecessary.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Entropy measures the "messiness" of a room. If a box contains only red balls, it's perfectly organized (Zero Entropy). If it has 5 colors mixed up, it has High Entropy.</div>""",

    "3m_q40": """<p>Information Gain represents the expected reduction in a dataset's overall entropy (impurity) after partitioning it based on a specific attribute. Decision Trees utilize it to construct optimal architectures:</p>
<ul>
  <li><b>Evaluating Features:</b> At every given node, the algorithm calculates the potential Information Gain for splitting the data using each available feature.</li>
  <li><b>Selecting the Split:</b> It actively selects the single feature that yields the absolute highest Information Gain.</li>
  <li><b>Result:</b> This selection process aggressively maximizes the class purity of the resulting child nodes, rapidly reducing model uncertainty as the tree grows.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Information Gain asks, "Which question brings me the most clarity right now?" The tree always asks the most clarifying question first.</div>""",

    "3m_q41": """<p>Gini Impurity is a standard metric used by decision trees to measure the probability of incorrectly classifying a randomly chosen element from a dataset. It is widely preferred for specific structural advantages:</p>
<ul>
  <li><b>Mathematical Formula:</b> <code>Gini = 1 - &Sigma;(p_i)&sup2;</code>.</li>
  <li><b>Computational Efficiency:</b> Compared to Entropy, Gini Impurity is computationally much more efficient and faster to calculate.</li>
  <li><b>Why it is faster:</b> Gini only requires basic squaring operations of probabilities. Entropy, however, requires computing computationally expensive logarithmic functions (log base 2), making Gini superior for rapidly building large decision tree ensembles.</li>
</ul>
<div style="margin-top: 15px; padding: 15px; background: rgba(0, 200, 150, 0.1); border-left: 4px solid var(--primary-teal); border-radius: 8px;"><strong>💡 Tip to remember:</strong> Entropy does complex math (logarithms) to measure messiness. Gini uses simple math (squares) to measure the same thing, making it the faster, preferred shortcut for algorithms.</div>"""
}

def main():
    input_file = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_2.json"
    output_file = r"c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\chunk_2_final.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        q_id = item.get("id")
        if q_id in new_html_map:
            item["answer_html"] = new_html_map[q_id]
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
if __name__ == "__main__":
    main()
