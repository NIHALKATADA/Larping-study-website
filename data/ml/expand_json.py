import json
import re

input_file = r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\part_4.json'
output_file = r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\part_4_expanded.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    title = item.get('title', '').lower()
    orig_html = item.get('answer_html', '')
    
    # Base expansion template
    expansion = '<h3>Comprehensive Analysis and Implementation Details</h3>'
    
    if 'logistic' in title or 'sigmoid' in title or 'cross-entropy' in title:
        expansion += '''
        <p><b>Logistic Regression Deep Dive:</b> Logistic regression is a fundamental classification algorithm that models the probability of a discrete outcome given an input variable. The most common logistic regression models a binary outcome. It uses the logistic function (sigmoid) to constrain the output between 0 and 1.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Sigmoid Function:</b> Maps any real-valued number into a value between 0 and 1, which can be interpreted as a probability.</li>
            <li><b>Decision Boundary:</b> The threshold (typically 0.5) used to separate the classes.</li>
            <li><b>Log-Loss:</b> The cost function used in logistic regression, which penalizes confident but incorrect predictions.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>from sklearn.linear_model import LogisticRegression\nimport numpy as np\n\nX = np.array([[2, 1], [3, 4], [5, 1], [6, 2]])\ny = np.array([0, 0, 1, 1])\nmodel = LogisticRegression().fit(X, y)\nprobs = model.predict_proba([[4, 2]])\nprint('Class probabilities:', probs)</code></pre>
        '''
    elif 'tree' in title or 'entropy' in title or 'gini' in title:
        expansion += '''
        <p><b>Decision Trees & Information Theory:</b> Decision trees partition the feature space into regions. The splits are chosen to maximize information gain or minimize Gini impurity, making the resulting child nodes as pure as possible.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Entropy:</b> A measure of randomness or unpredictability in the dataset. Lower entropy means higher purity.</li>
            <li><b>Gini Impurity:</b> Measures how often a randomly chosen element would be incorrectly labeled. Faster to compute than entropy.</li>
            <li><b>Information Gain:</b> The reduction in entropy after a dataset is split on an attribute.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>from sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\nmodel = DecisionTreeClassifier(criterion='entropy', max_depth=3)\nmodel.fit(X_train, y_train)\npreds = model.predict(X_test)</code></pre>
        '''
    elif 'regression' in title or 'least-squares' in title or 'mse' in title and 'tree' not in title:
        expansion += '''
        <p><b>Linear Regression Fundamentals:</b> Linear regression assumes a linear relationship between input variables and the target variable. The objective is to find the line of best fit by minimizing the residual sum of squares.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Ordinary Least Squares (OLS):</b> The mathematical optimization technique used to find the best-fitting line.</li>
            <li><b>Normal Equations:</b> A closed-form solution to find the parameters, though computationally expensive for very large feature spaces.</li>
            <li><b>Gradient Descent:</b> An iterative optimization algorithm used when normal equations are too costly.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>import numpy as np\nfrom sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\nprint('Coefficients:', model.coef_)\nprint('Intercept:', model.intercept_)</code></pre>
        '''
    elif 'knn' in title or 'distance' in title:
        expansion += '''
        <p><b>K-Nearest Neighbors (KNN):</b> KNN is a non-parametric, lazy learning algorithm. It classifies a new data point based on the majority class of its 'K' closest neighbors in the feature space.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Distance Metrics:</b> Euclidean distance is the straight-line distance, while Manhattan is the sum of absolute differences. The choice depends on data dimensionality and scaling.</li>
            <li><b>Choosing K:</b> A small K makes the model sensitive to noise (high variance), while a large K makes it computationally expensive and biased.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>from sklearn.neighbors import KNeighborsClassifier\n\nknn = KNeighborsClassifier(n_neighbors=3, metric='euclidean')\nknn.fit(X_train, y_train)\npred = knn.predict([query_point])</code></pre>
        '''
    elif 'naive bayes' in title or 'spam' in title:
        expansion += '''
        <p><b>Naive Bayes Classification:</b> Based on Bayes' Theorem, this classifier assumes strong (naive) independence between the features. It is highly effective for text classification tasks like spam filtering.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Prior Probability:</b> The probability of a class before observing any evidence.</li>
            <li><b>Posterior Probability:</b> The updated probability of a class after observing the evidence.</li>
            <li><b>Laplace Smoothing:</b> Used to handle unseen features (zero probabilities) in the test set.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>from sklearn.naive_bayes import MultinomialNB\n\nnb = MultinomialNB()\nnb.fit(X_train_counts, y_train)\nprediction = nb.predict(new_text_counts)</code></pre>
        '''
    elif 'svm' in title or 'hyperplane' in title:
        expansion += '''
        <p><b>Support Vector Machines (SVM):</b> SVM is a powerful classifier that finds the optimal hyperplane which maximizes the margin between different classes. Support vectors are the data points closest to the hyperplane.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Hyperplane:</b> The decision boundary separating classes. In 2D, it's a line; in 3D, a plane.</li>
            <li><b>Margin:</b> The distance between the hyperplane and the nearest data point from either class.</li>
            <li><b>Kernel Trick:</b> Projects data into a higher dimension to find a linear separator for non-linearly separable data.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>from sklearn.svm import SVC\n\nsvm_model = SVC(kernel='linear', C=1.0)\nsvm_model.fit(X_train, y_train)\npreds = svm_model.predict(X_test)</code></pre>
        '''
    elif 'forest' in title or 'ensemble' in title or 'boosting' in title or 'adaboost' in title:
        expansion += '''
        <p><b>Ensemble Methods:</b> Ensemble techniques combine multiple weak learners to create a single strong learner, significantly improving predictive performance and robustness.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Bagging (e.g., Random Forest):</b> Builds multiple independent trees on random subsets of data and averages their predictions to reduce variance.</li>
            <li><b>Boosting (e.g., AdaBoost, XGBoost):</b> Builds trees sequentially, where each new tree focuses on correcting the errors made by previous ones, reducing bias.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>from sklearn.ensemble import RandomForestRegressor, AdaBoostClassifier\n\nrf = RandomForestRegressor(n_estimators=100)\nrf.fit(X_train, y_train)\npred = rf.predict(X_test)</code></pre>
        '''
    else:
        expansion += '''
        <p><b>Evaluation Metrics and Model Assessment:</b> Properly evaluating a model is as important as training it. Different tasks require different metrics to accurately reflect model performance.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li><b>Regression Metrics:</b> MAE gives average error magnitude, MSE heavily penalizes large errors, and RMSE is interpretable in the original units.</li>
            <li><b>Classification Metrics:</b> Accuracy is good for balanced classes. Precision and Recall are crucial when false positives or false negatives have different costs. F1-score balances the two.</li>
        </ul>
        <h4>Python Example:</h4>
        <pre><code>from sklearn.metrics import mean_squared_error, classification_report\n\nprint('Classification Report:')\nprint(classification_report(y_true, y_pred))\n\nmse = mean_squared_error(y_true, y_pred)\nprint(f'MSE: {mse}')</code></pre>
        '''

    item['answer_html'] = f"<div class='solution-step'>{orig_html}</div><hr/><div class='comprehensive-analysis'>{expansion}</div>"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
print('Done!')
