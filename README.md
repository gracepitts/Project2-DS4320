# DS 4320 Project 2: Improving Clinical Trial Success Rates

**Executive Summary:** This repository contains a project focused on predicting clinical trial success using data from ClinicalTrials.gov. It includes a cleaned dataset, a full analysis pipeline built with Python and MongoDB, background readings, data documentation, and a press release summarizing the results. The project explores how factors like trial phase, organization type, and intervention type relate to whether a trial is successfully completed. 

**Name:** Grace Pitts

**NetID:** twg3sr

**Links**:

**DOI:**

[Press Release](press_release.md)

[Pipeline](pipeline)

This project is licensed under the MIT License. See the [License](LICENSE) file for details. 


## Problem Definition
**Initial Problem:** 

Clinical Drug Trials.

**Refined Problem Statement**: 

Predict whether a clinical trial will be completed or terminated based on trial characteristics.

**Refinement Rationale:** 

The general problem of clinical drug trials is too broad to study effectively in one project, so I refined the focus on predicting whether a trial is completed. This refinement works well because the dataset includes a clear status field, Overall Status, along with several useful explanatory variables such as Organization Class, Study Type, Phases, Conditions, Interventions, and Primary Purpose. Narrowing the project in this way makes the problem more specific, measurable, and appropriate for analysis and modeling. It will also allow me to perform a more meaningful and detailed analysis due to the more specific problem. It also is more applicable in the real world with this refinement because this can help to see which clinical trials are worth putting time and money into versus which clinical trials have little potential to be approved.

**Project Motivation**: 

Clinical trials are an important part of developing new treatments, but they can take a long time and require a large amount of planning and money. Not all trials reach completion, and differences in factors such as study type, phase, organization type, conditions being studied, interventions, and more may affect whether a trial moves forward successfully. Understanding these patterns can be useful for researchers, sponsors, and healthcare organizations because it may help them design stronger trials and better allocate resources. This project is motivated by the idea that analyzing clinical trial characteristics can reveal patterns that help explain trial outcomes, while also saving time and money on trials that are likely to fail.

**Press Release:** 

[Improving Clinical Trial Success Rates](press_release.md)



## Domain Exposition

**Terminology:**
| Term | Description |
|------|------------|
| Clinical Trial | A research study conducted to evaluate medical, surgical, or behavioral interventions in humans |
| Overall Status | The current state of a trial (e.g., Completed, Terminated, Withdrawn) |
| Phase | The stage of the clinical trial (Phase 1, Phase 2, Phase 3) indicating testing progression |
| Intervention | The treatment or procedure being studied (Drug, device, therapy) |
| Intervention Description | A detailed explanation of the intervention being used in the study |
| Condition | The disease or health issue being studied in the trial |
| Study Type | The type of study (Interventional or Observational) |
| Organization Class | The type of organization running the trial ( Industry, Academic) |
| Responsible Party | The individual or organization responsible for conducting and managing the clinical trial |
| Primary Purpose | The main goal of the trial (Treatment, Prevention) |
| Medical Subject Headings (MeSH) | Standardized terms used to categorize and index medical information |
| Success Rate | The proportion of trials that are completed versus those that are terminated or withdrawn |

**Project Domain:** 

This project is in the healthcare and clinical research domain, specifically focusing on clinical drug trials. Clinical trials are essential for testing the safety and effectiveness of new treatments before they are approved for public use. These studies involve multiple phases, different types of interventions, and are conducted by a variety of organizations, including pharmaceutical companies and academic institutions.

**Background Readings:**


Background readings can be found here: [link](https://myuva-my.sharepoint.com/:f:/g/personal/twg3sr_virginia_edu/IgCMJ46DFPcvTaBdlSvUGWtCAd9E4P8SbWH7tnGzV_Rreyo?e=r9a5RU)

**Reading Descriptions:**
| Title | Brief Description | Link |
|------|------------------|----|
| Cost of Drug Development and Research and Development Intensity in the US, 2000–2018 | Examines the high costs of drug development and how failure rates impact pricing and innovation. | [View Article](https://myuva-my.sharepoint.com/:b:/g/personal/twg3sr_virginia_edu/IQCQJ5-HSoGFQKfbCPx9-yILAQyLuwwQBommnnPcznSCE58?e=yLQECz) |
| Factors Affecting Success of New Drug Clinical Trials | Identifies key factors like trial quality and efficiency that influence clinical trial success. | [View Article](https://myuva-my.sharepoint.com/:b:/g/personal/twg3sr_virginia_edu/IQCyc5HK97C8RaJdGoADMFQsAax0J2wPog_a3K4GNwbcPIs?e=RrrACm) |
| How We Define Success for a Clinical Trial | Explains how clinical trial success is measured using outcomes like effectiveness and safety. | [View Article](https://myuva-my.sharepoint.com/:b:/g/personal/twg3sr_virginia_edu/IQAmbUk-TLwoRqYKYVEDqsNAATzzDK4sgAFQL8XkFBdPazw?e=eldod8) |
| Learn About Studies | Provides an overview of clinical research and differences between study types. | [View Article](https://myuva-my.sharepoint.com/:b:/g/personal/twg3sr_virginia_edu/IQDFcpDMyw-rT4soF6MgraWGAWH2BeXaUgO4DB251w5Ij4E?e=Lc7gBn) |
| Why 90% of Clinical Drug Development Fails and How to Improve It | Explores why most trials fail and suggests ways to improve success rates. | [View Article](https://myuva-my.sharepoint.com/:b:/g/personal/twg3sr_virginia_edu/IQADEmUPrqsmQ5sOQzSacgpxATj-_Lfn3EzaHIXTdmj8Ldc?e=5DpTLc) |

## Data Creation

**Raw Data Accquisition:**


The dataset used in this project was downloaded from Kaggle, and is called "ClinicalTrials.gov Clinical Trials Dataset." This dataset was obtained from ClinicalTrials.gov, a publicly available database maintained by the U.S. National Library of Medicine. The U.S. National Library of Medicine provides information on clinical studies conducted around the world and includes data such as trial status, study type, phase, conditions, interventions, and organization characteristics. The dataset was downloaded as a compressed CSV file and extracted using Python in Google Colab. The data was then loaded into a pandas DataFrame for initial exploration and cleaning and will later be transformed into a document-based structure for use in MongoDB.

**Code Provenance Table:**
| File Name | Description | Link |
|----------|------------|------|
| load_and_clean_data.py | Loads the dataset from Kaggle and reads it into a pandas DataFrame. Cleans and preprocesses the data. |  [View Code](load_and_clean_data.py) 
| mongo_upload.py| Converts cleaned data into JSON format and uploads it to MongoDB Atlas | [View Code](mongo_upload.py) |


**Decision Rationale:** 

Several key decisions were made during data preparation and analysis. First, clinical trial success was defined as trials with an "Overall Status" of Completed, while all other statuses were considered non-successful. This simplifies the problem into a binary classification task but by doing so it may overlook nuances between different failure types. Next, only clearly defined phases (Phase 1 through Phase 4) were included in the final visualization to improve interpretability and avoid ambiguity from mixed or unknown phase labels. Additionally, text fields such as status and phase were standardized to ensure consistency during grouping and analysis. These decisions help improve clarity and usability of the dataset, but may introduce some loss of detail or simplification of real-world complexity.


**Bias Identification:**

Bias may be introduced in this dataset due to the way clinical trials are reported and recorded in ClinicalTrials.gov. Not all clinical trials are registered, and those that are may differ from those that are not, leading to selection bias. Also, the dataset could overrepresent trials from certain regions, organizations, or disease areas, especially those done by larger institutions with more resources. There could also be reporting bias since some trials may be terminated or have incomplete information, and the reasons for failure are not always fully captured in the dataset.

**Bias Mitigation:**

Biases in the dataset can be managed by recognizing their presence and accounting for them when interpreting results. For example, the analysis can focus on well-represented categories and use summary statistics to identify any imbalances in the data. Additionally, grouping similar categories and removing incomplete or inconsistent records can help improve overall data quality. Being transparent about these limitations ensures that results are interpreted appropriately rather than being misleading.

## Metadata

**Implicit Schema:**

The MongoDB collection follows a consistent document structure for each clinical trial. Each document represents a single trial and includes both top-level fields and nested fields.

Top-level fields include:
- trial_id
- brief_title
- full_title
- overall_status
- study_type
- phases
- primary_purpose
- start_date
- standard_age
- outcome_measure
- success

Nested fields are used to group related information:
- organization: contains organization_full_name, organization_class, and responsible_party
- conditions: stored as a list of condition names
- interventions: contains a list of intervention names and a description

This structure ensures consistency across documents while allowing flexibility for lists and nested data, which is a key advantage of the document model.

**Data Summary:**

| Component | Description |
|----------|------------|
| Collection Name | clinical_trials |
| Number of Documents | ~40,600 clinical trials |
| Data Source | ClinicalTrials.gov (Kaggle dataset) |
| Unit of Analysis | One document per clinical trial |
| Key Features | trial_id, overall_status, phases, study_type, primary_purpose |
| Nested Fields | organization, conditions, interventions |
| Target Variable | success (1 = completed, 0 = not completed) |

**Data Dictionary:**

| Feature Name | Data Type | Description | Example | % Missing | Mean | Median | Std Dev |
|-------------|----------|------------|---------|----------|------|--------|---------|
| Organization Full Name | String | Name of the organization conducting or sponsoring the trial | Montefiore Medical Center | — | — | — | — |
| Organization Class | String | Type of organization running the trial (e.g., Industry, Academic) | Industry | — | — | — | — |
| Responsible Party | String | Individual or organization responsible for the trial | Sponsor | — | — | — | — |
| Brief Title | String | Short title describing the clinical trial | Kinesiotape for Edema After Bilateral Total Knee Arthroplasty | — | — | — | — |
| Full Title | String | Full descriptive title of the clinical trial | Kinesiotape for Edema After Bilateral Total Knee Arthroplasty | — | — | — | — |
| Overall Status | String | Current status of the trial | COMPLETED | — | — | — | — |
| Start Date | Date | Date when the trial began | 2015-06-01 | — | — | — | — |
| Standard Age | String | Age group eligible for the trial | Adult | — | — | — | — |
| Conditions | String | Disease or condition being studied | Diabetes | — | — | — | — |
| Primary Purpose | String | Main goal of the trial (e.g., Treatment, Prevention) | Treatment | — | — | — | — |
| Interventions | String | Treatment or procedure being tested | Ramipril | — | — | — | — |
| Intervention Description | String | Detailed description of the intervention | ramipril 2.5mg twice a day | — | — | — | — |
| Study Type | String | Type of study conducted | Interventional | — | — | — | — |
| Phases | String | Phase of the clinical trial | PHASE3 | — | — | — | — |
| Outcome Measure | String | Outcome used to evaluate trial success | headache frequency | — | — | — | — |
| Medical Subject Headings | String | Standardized medical terms used to categorize the study | Hypospadias | — | — | — | — |
| num_conditions | Numeric | Number of conditions listed per trial | — | 0.00% | 1.86 | 1.0 | 2.30 |
| num_interventions | Numeric | Number of interventions per trial | — | 0.00% | 1.86 | 1.0 | 1.45 |
| title_length | Numeric | Length of trial title (characters) | — | 0.00% | 85.79 | 81.0 | 35.97 |
