## Error Handling and Logging

This pipeline includes basic `try`/`except` error handling and logs important pipeline events to `pipeline.log`. This helps track whether the MongoDB connection, data query, model training, and evaluation steps run successfully.


```python
import logging

# Set up logging to a file so pipeline progress and errors are saved
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logging.info("Pipeline started")
print("Logging set up successfully.")
```

    Logging set up successfully.



```python
!pip -q install pymongo[srv]

import pandas as pd
from pymongo import MongoClient
```

    [33mWARNING: pymongo 4.17.0 does not provide the extra 'srv'[0m[33m
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m331.1/331.1 kB[0m [31m4.8 MB/s[0m eta [36m0:00:00[0m
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.8/1.8 MB[0m [31m21.1 MB/s[0m eta [36m0:00:00[0m
    [?25h


```python
from pymongo import MongoClient
from getpass import getpass

try:
    # Prompt user for credentials securely
    username = input("Enter your MongoDB username: ")
    password = getpass("Enter your MongoDB password: ")

    # Create MongoDB connection string
    uri = f"mongodb+srv://{username}:{password}@cluster1.ecpqpus.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

    # Initialize MongoDB client with timeout settings for stability
    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        retryWrites=True
    )

    # Test connection
    client.admin.command("ping")
    print("Connected successfully.")
    logging.info("Connected to MongoDB successfully")

except Exception as e:
    print("Error connecting to MongoDB:", e)
    logging.error(f"MongoDB connection failed: {e}")
    raise
```

    Enter your MongoDB username: gracepitts2004
    Enter your MongoDB password: ··········
    Connected successfully.



```python
try:
    # Select database and collection
    db = client["clinical_trials_project"]
    collection = db["clinical_trials"]

    # Print available collections and document count
    print("Collections:", db.list_collection_names())
    print("Document count:", collection.count_documents({}))

    # Display one sample document
    sample_doc = collection.find_one()
    logging.info("Database and collection selected successfully")
    sample_doc

except Exception as e:
    print("Error selecting database or collection:", e)
    logging.error(f"Database/collection selection failed: {e}")
    raise
```

    Collections: ['clinical_trials']
    Document count: 113032



```python
try:
    # Query selected fields from MongoDB for modeling
    docs = list(collection.find({}, {
        "_id": 0,
        "overall_status": 1,
        "phases": 1,
        "study_type": 1,
        "primary_purpose": 1,
        "organization.organization_class": 1,
        "interventions.names": 1,
        "conditions": 1
    }))

    # Convert MongoDB documents into a pandas DataFrame
    df = pd.DataFrame(docs)

    print(df.shape)
    logging.info(f"Loaded data from MongoDB with shape {df.shape}")
    display(df.head())

except Exception as e:
    print("Error loading data from MongoDB:", e)
    logging.error(f"Data loading failed: {e}")
    raise
```

    (113032, 7)




  <div id="df-e35b5a2e-ac03-4d69-9ccb-67f325e83ae0" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>overall_status</th>
      <th>study_type</th>
      <th>phases</th>
      <th>primary_purpose</th>
      <th>organization</th>
      <th>conditions</th>
      <th>interventions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>COMPLETED</td>
      <td>Interventional</td>
      <td>UNKNOWN</td>
      <td>Treatment</td>
      <td>{'organization_class': 'OTHER'}</td>
      <td>[Arthroplasty Complications, Arthroplasty, Rep...</td>
      <td>{'names': ['Kinesio(R)Tape for edema control']}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>COMPLETED</td>
      <td>Interventional</td>
      <td>PHASE2</td>
      <td>Treatment</td>
      <td>{'organization_class': 'OTHER'}</td>
      <td>[Migraine With Hypertension]</td>
      <td>{'names': ['Ramipril']}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>COMPLETED</td>
      <td>Observational</td>
      <td>UNKNOWN</td>
      <td>Unknown</td>
      <td>{'organization_class': 'OTHER'}</td>
      <td>[Diabetic Retinopathy]</td>
      <td>{'names': ['Dexamethasone intravitreal implant']}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>COMPLETED</td>
      <td>Interventional</td>
      <td>PHASE2</td>
      <td>Treatment</td>
      <td>{'organization_class': 'OTHER'}</td>
      <td>[Head and Neck Squamous Cell Carcinoma, Head a...</td>
      <td>{'names': ['Nivolumab 480mg and surgical resec...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>TERMINATED</td>
      <td>Interventional</td>
      <td>PHASE2</td>
      <td>Treatment</td>
      <td>{'organization_class': 'OTHER'}</td>
      <td>[Adenocarcinoma of the Prostate, Recurrent Pro...</td>
      <td>{'names': ['genistein', 'placebo', 'therapeuti...</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-e35b5a2e-ac03-4d69-9ccb-67f325e83ae0')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-e35b5a2e-ac03-4d69-9ccb-67f325e83ae0 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-e35b5a2e-ac03-4d69-9ccb-67f325e83ae0');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


    </div>
  </div>




```python
# Extract organization class from nested dictionary
df["organization_class"] = df["organization"].apply(
    lambda x: x.get("organization_class") if isinstance(x, dict) else None
)

# Simplify intervention information into broader categories
# Function to simplify detailed intervention names into broad categories for modeling
def simplify_intervention(x):
    if isinstance(x, dict):
        names = x.get("names", [])
        text = " ".join(names).lower()
        # Group interventions into general types
        if "drug" in text:
            return "Drug"
        elif "device" in text:
            return "Device"
        else:
            return "Other"
    return "Unknown"

# Apply the simplified intervention categories
df["intervention_type"] = df["interventions"].apply(simplify_intervention)

# Count how many conditions are listed for each trial
df["num_conditions"] = df["conditions"].apply(
    lambda x: len(x) if isinstance(x, list) else 0
)

# Create binary target variable (1 = success, 0 = not success)
df["success"] = df["overall_status"].apply(
    lambda x: 1 if str(x).strip().upper() == "COMPLETED" else 0
)

# Select only the columns needed for modeling
model_df = df[[
    "success",
    "phases",
    "organization_class",
    "intervention_type",
    "study_type",
    "primary_purpose",
    "num_conditions"
]].copy()

# Fill missing values and clean text formatting for categorical variables
for col in ["phases", "organization_class", "intervention_type", "study_type", "primary_purpose"]:
    model_df[col] = model_df[col].fillna("Unknown").astype(str).str.strip()

# Fill missing numeric values
model_df["num_conditions"] = model_df["num_conditions"].fillna(0)

# Check final dataset shape and preview data
print(model_df.shape)
model_df.head()
```

    (113032, 7)






  <div id="df-bdb5309b-f6bd-40e6-9af1-10692915b763" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>success</th>
      <th>phases</th>
      <th>organization_class</th>
      <th>intervention_type</th>
      <th>study_type</th>
      <th>primary_purpose</th>
      <th>num_conditions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>UNKNOWN</td>
      <td>OTHER</td>
      <td>Other</td>
      <td>Interventional</td>
      <td>Treatment</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>PHASE2</td>
      <td>OTHER</td>
      <td>Other</td>
      <td>Interventional</td>
      <td>Treatment</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>UNKNOWN</td>
      <td>OTHER</td>
      <td>Other</td>
      <td>Observational</td>
      <td>Unknown</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>PHASE2</td>
      <td>OTHER</td>
      <td>Other</td>
      <td>Interventional</td>
      <td>Treatment</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>PHASE2</td>
      <td>OTHER</td>
      <td>Other</td>
      <td>Interventional</td>
      <td>Treatment</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-bdb5309b-f6bd-40e6-9af1-10692915b763')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-bdb5309b-f6bd-40e6-9af1-10692915b763 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-bdb5309b-f6bd-40e6-9af1-10692915b763');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


    </div>
  </div>





```python
# Log successful completion of modeling dataset preparation
logging.info(f"Prepared modeling dataframe with shape {model_df.shape}")
```


```python
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Separate features (X) and target variable (y)
X = model_df.drop(columns="success")
y = model_df["success"]

# List of categorical features that need encoding
categorical_features = [
    "phases",
    "organization_class",
    "intervention_type",
    "study_type",
    "primary_purpose"
]

# List of numeric features
numeric_features = ["num_conditions"]

# Create a preprocessing pipeline:
# - One-hot encode categorical variables
# - Keep numeric variables as they are
# Create preprocessing steps for categorical and numeric variables
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

# Split data into training (80%) and testing (20%) sets
# stratify=y ensures the proportion of success/failure is similar in both sets
# Split the data into training and testing sets so the model is evaluated on unseen data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Print shapes to confirm split worked correctly
print("Training shape:", X_train.shape)
print("Test shape:", X_test.shape)
```

    Training shape: (90425, 6)
    Test shape: (22607, 6)



```python
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Create a pipeline that preprocesses the data and trains the model
# Create a machine learning pipeline that preprocesses data and trains a Random Forest model
rf_model = Pipeline(steps=[
    ("preprocessor", preprocessor),  # Apply encoding and transformations
    ("model", RandomForestClassifier(
        n_estimators=200,   # Number of trees in the forest
        max_depth=10,       # Limit tree depth to reduce overfitting
        random_state=42     # Ensure reproducible results
    ))
])

try:
    # Train the model using the training data
    rf_model.fit(X_train, y_train)
    print("Model trained.")
    logging.info("Model training successful")

except Exception as e:
    print("Error training model:", e)
    logging.error(f"Model training failed: {e}")
    raise
```

    Model trained.



```python
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

try:
    # Generate predictions for the test set
    y_pred = rf_model.predict(X_test)

    # Get predicted probabilities for the positive class
    y_prob = rf_model.predict_proba(X_test)[:, 1]

    # Calculate evaluation metrics
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    print("Accuracy:", round(acc, 3))
    print("ROC AUC:", round(auc, 3))

    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix:\n")
    print(confusion_matrix(y_test, y_pred))

    logging.info(f"Model evaluation successful - Accuracy: {acc:.3f}, ROC AUC: {auc:.3f}")

except Exception as e:
    print("Error during model evaluation:", e)
    logging.error(f"Model evaluation failed: {e}")
    raise
```

    Accuracy: 0.58
    ROC AUC: 0.618
    
    Classification Report:
    
                  precision    recall  f1-score   support
    
               0       0.57      0.31      0.40     10236
               1       0.59      0.80      0.68     12371
    
        accuracy                           0.58     22607
       macro avg       0.58      0.56      0.54     22607
    weighted avg       0.58      0.58      0.55     22607
    
    
    Confusion Matrix:
    
    [[3221 7015]
     [2472 9899]]



```python
import matplotlib.pyplot as plt
import pandas as pd

# Get feature names after preprocessing
ohe = rf_model.named_steps["preprocessor"].named_transformers_["cat"]
cat_names = ohe.get_feature_names_out(categorical_features)
feature_names = list(cat_names) + numeric_features

# Get feature importances from the trained random forest model
importances = rf_model.named_steps["model"].feature_importances_

# Create a dataframe of feature names and importance values
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})

# Keep only the top 10 most important features
importance_df = importance_df.sort_values("Importance", ascending=False).head(10).copy()

# Clean feature labels to be more professional and readable
importance_df["Feature"] = (
    importance_df["Feature"]
    .str.replace("organization_class_", "Organization: ", regex=False)
    .str.replace("phases_", "Phase: ", regex=False)
    .str.replace("study_type_", "Study Type: ", regex=False)
    .str.replace("primary_purpose_", "Purpose: ", regex=False)
    .str.replace("intervention_type_", "Intervention: ", regex=False)
    .str.replace("num_conditions", "Number of Conditions", regex=False)
)

# Improve readability by replacing underscores and applying title case
importance_df["Feature"] = (
    importance_df["Feature"]
    .str.replace("_", " ")
    .str.title()
)

# Manually fix labels that look awkward after title formatting
importance_df["Feature"] = importance_df["Feature"].replace({
    "Organization: Industry": "Organization: Industry",
    "Organization: Other": "Organization: Other",
    "Organization: Nih": "Organization: NIH",
    "Organization: Other Gov": "Organization: Government",
    "Study Type: Expanded Access": "Study Type: Expanded Access",
    "Phase: Phase1": "Phase: Phase I",
    "Phase: Phase2": "Phase: Phase II",
    "Phase: Phase3": "Phase: Phase III",
    "Phase: Phase4": "Phase: Phase IV",
    "Phase: Phase1, Phase2": "Phase: Phase I–II",
    "Phase: Unknown": "Phase: Unknown",
    "Purpose: Treatment": "Purpose: Treatment",
    "Number Of Conditions": "Number of Conditions"
})

# Reverse order so the most important feature appears at the top of the chart
importance_df = importance_df.iloc[::-1]

# Create the plot
plt.figure(figsize=(11, 6.5))
plt.barh(importance_df["Feature"], importance_df["Importance"])

# Add title and axis labels
plt.title("Key Factors Associated with Clinical Trial Success", fontsize=14, pad=12)
plt.xlabel("Feature Importance", fontsize=11)
plt.ylabel("")

# Remove unnecessary borders for a cleaner look
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Add a light x-axis grid to improve readability
plt.grid(axis="x", linestyle="--", alpha=0.4)

# Adjust font sizes
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Tight layout and save high-resolution version
plt.tight_layout()
plt.savefig("feature_importance_chart.png", dpi=300, bbox_inches="tight")
plt.show()
```


    
![png](pipeline_files/pipeline_11_0.png)
    



```python
logging.info("Pipeline completed successfully")
print("Pipeline complete. Log saved to pipeline.log")
```

    Pipeline complete. Log saved to pipeline.log


The goal of this analysis was to predict whether a clinical trial would succeed or fail, where success is defined as a trial with status COMPLETED. I selected features like trial phase, organization type, study type, intervention type, and number of conditions because they capture important aspects of trial design. The data was cleaned by handling missing values and simplifying categories, and then split into training and test sets to evaluate model performance. This analysis uses a Random Forest classifier, an ensemble machine learning method. A preprocessing pipeline was used to encode categorical variables and prepare the data. The model was trained on a training set and evaluated using accuracy and ROC AUC. The model achieved an accuracy of 0.58 and an ROC AUC of 0.618, indicating moderate predictive performance. This suggests the model performs better than random chance but that clinical trial outcomes are complex and not fully captured by the available data.

A feature importance chart was created to show which variables are most influential in predicting clinical trial success. The results highlight factors such as organization type, number of conditions, and trial phase.
A horizontal bar chart was used because it clearly compares feature importance and works well with longer labels. This visualization helps show how the model makes predictions in an interpretable way.
