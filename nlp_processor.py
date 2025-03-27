import logging
import spacy
import re

logger = logging.getLogger(__name__)

# Load the spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logger.debug("Loaded spaCy model: en_core_web_sm")
except OSError:
    logger.warning("Default spaCy model not found, downloading...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    logger.debug("Downloaded and loaded spaCy model: en_core_web_sm")

# Medical terminology patterns
# Comprehensive list of medical terms for document processing
MEDICAL_TERMS_PATTERNS = [
    # Common chronic conditions
    r"(?i)diabet(?:es|ic)",
    r"(?i)hypertens(?:ion|ive)",
    r"(?i)chronic kidney disease",
    r"(?i)ckd(?: stage [1-5])?",
    r"(?i)heart failure",
    r"(?i)congestive heart failure",
    r"(?i)chf",
    r"(?i)asthma",
    r"(?i)copd",
    r"(?i)chronic obstructive pulmonary disease",
    r"(?i)cancer",
    r"(?i)carcinoma",
    r"(?i)malignant",
    r"(?i)neoplasm",
    r"(?i)tumor",
    r"(?i)metastatic",
    r"(?i)metastasis",
    r"(?i)stroke",
    r"(?i)cerebrovascular (?:accident|disease)",
    r"(?i)cva",
    r"(?i)tia",
    r"(?i)transient ischemic attack",
    r"(?i)alzheimer(?:'s disease)?",
    r"(?i)dementia",
    r"(?i)parkinson(?:'s disease)?",
    r"(?i)huntington(?:'s disease)?",
    r"(?i)multiple sclerosis",
    r"(?i)ms(?= |$|\.|,)",  # MS with word boundary to avoid false matches
    r"(?i)arthritis",
    r"(?i)rheumatoid arthritis",
    r"(?i)osteoarthritis",
    r"(?i)gout",
    r"(?i)depression",
    r"(?i)major depressive disorder",
    r"(?i)anxiety",
    r"(?i)generalized anxiety disorder",
    r"(?i)bipolar disorder",
    r"(?i)schizophrenia",
    r"(?i)post-traumatic stress disorder",
    r"(?i)ptsd",
    r"(?i)ocd",
    r"(?i)obsessive compulsive disorder",
    r"(?i)obesity",
    r"(?i)morbid obesity",
    r"(?i)bmi(?: [3-9][0-9])?",
    r"(?i)cirrhosis",
    r"(?i)hepatitis",
    r"(?i)fatty liver",
    r"(?i)nash",
    r"(?i)nonalcoholic steatohepatitis",
    r"(?i)emphysema",
    r"(?i)pulmonary fibrosis",
    r"(?i)coronary artery disease",
    r"(?i)cad",
    r"(?i)myocardial infarction",
    r"(?i)heart attack",
    r"(?i)angina",
    r"(?i)atrial fibrillation",
    r"(?i)afib",
    r"(?i)arrhythmia",
    r"(?i)hypothyroidism",
    r"(?i)hyperthyroidism",
    r"(?i)hyperlipidemia",
    r"(?i)dyslipidemia",
    r"(?i)osteoporosis",
    r"(?i)epilepsy",
    r"(?i)seizure disorder",
    r"(?i)neuropathy",
    r"(?i)peripheral neuropathy",
    r"(?i)retinopathy",
    r"(?i)nephropathy",
    
    # Blood Test Related Terms
    r"(?i)hemoglobin",
    r"(?i)hematocrit",
    r"(?i)rbc|red\s*blood\s*cells?",
    r"(?i)wbc|white\s*blood\s*cells?",
    r"(?i)platelets?",
    r"(?i)cholesterol",
    r"(?i)triglycerides?",
    r"(?i)hdl",
    r"(?i)ldl",
    r"(?i)a1c|hba1c",
    r"(?i)glycos(?:yl)?ated hemoglobin",
    r"(?i)glucose",
    r"(?i)fasting (?:blood )?glucose",
    r"(?i)creatinine",
    r"(?i)bun",
    r"(?i)blood urea nitrogen",
    r"(?i)egfr",
    r"(?i)estimated glomerular filtration rate",
    r"(?i)alt|alanine aminotransferase",
    r"(?i)ast|aspartate aminotransferase",
    r"(?i)ggt|gamma-glutamyl transferase",
    r"(?i)alkaline phosphatase",
    r"(?i)bilirubin",
    r"(?i)albumin",
    r"(?i)protein",
    r"(?i)tsh|thyroid stimulating hormone",
    r"(?i)t3|t4|thyroxine",
    r"(?i)sodium|potassium|chloride|bicarbonate",
    r"(?i)calcium|phosphorus|magnesium",
    r"(?i)ferritin|iron",
    r"(?i)transferrin",
    r"(?i)vitamin\s*d",
    r"(?i)vitamin\s*b12",
    r"(?i)folate|folic acid",
    r"(?i)hemoglobin a1c",
    r"(?i)inr|international normalized ratio",
    r"(?i)pt|prothrombin time",
    r"(?i)ptt|partial thromboplastin time",
    r"(?i)troponin",
    r"(?i)bnp|brain natriuretic peptide",
    r"(?i)nt-probnp",
    r"(?i)crp|c-reactive protein",
    r"(?i)esr|erythrocyte sedimentation rate",
    r"(?i)psa|prostate specific antigen",
    
    # Common diagnostic findings
    r"(?i)anemia",
    r"(?i)leukocytosis",
    r"(?i)leukopenia",
    r"(?i)thrombocytopenia",
    r"(?i)thrombocytosis",
    r"(?i)pancytopenia",
    r"(?i)neutropenia",
    r"(?i)neutrophilia",
    r"(?i)lymphocytosis",
    r"(?i)lymphopenia",
    r"(?i)eosinophilia",
    r"(?i)hypoglycemia",
    r"(?i)hyperglycemia",
    r"(?i)hyperlipidemia",
    r"(?i)hyponatremia",
    r"(?i)hypernatremia",
    r"(?i)hypokalemia",
    r"(?i)hyperkalemia",
    r"(?i)hypocalcemia",
    r"(?i)hypercalcemia",
    r"(?i)hypomagnesemia",
    r"(?i)hypermagnesemia",
    r"(?i)hypoalbuminemia",
    r"(?i)hyperbilirubinemia",
    r"(?i)hypoxemia",
    r"(?i)acidosis",
    r"(?i)alkalosis",
    r"(?i)proteinuria",
    r"(?i)hematuria",
    r"(?i)glycosuria",
    
    # Medical procedures and surgeries
    r"(?i)colonoscopy",
    r"(?i)endoscopy",
    r"(?i)mammogram",
    r"(?i)x-ray",
    r"(?i)mri",
    r"(?i)ct scan",
    r"(?i)ultrasound",
    r"(?i)echocardiogram",
    r"(?i)ekg|electrocardiogram",
    r"(?i)stress test",
    r"(?i)biopsy",
    r"(?i)surgery",
    r"(?i)cabg|coronary artery bypass graft",
    r"(?i)angioplasty",
    r"(?i)stent",
    r"(?i)pacemaker",
    r"(?i)defibrillator",
    r"(?i)joint replacement",
    r"(?i)appendectomy",
    r"(?i)cholecystectomy",
    r"(?i)hysterectomy",
    
    # Common medications by category/suffix
    r"(?i)\w+(?:mab|zumab|ximab|mumab)",  # Monoclonal antibodies
    r"(?i)\w+(?:olol)",  # Beta blockers
    r"(?i)\w+(?:sartan)",  # ARBs
    r"(?i)\w+(?:pril)",  # ACE inhibitors
    r"(?i)\w+(?:statin)",  # Statins
    r"(?i)\w+(?:dipine)",  # Calcium channel blockers
    r"(?i)\w+(?:methasone|sone|olone)",  # Corticosteroids
    r"(?i)\w+(?:cycline)",  # Tetracycline antibiotics
    r"(?i)\w+(?:mycin)",  # Macrolide antibiotics
    r"(?i)\w+(?:floxacin)",  # Quinolone antibiotics
    r"(?i)\w+(?:prazole)",  # Proton pump inhibitors
    r"(?i)warfarin|coumadin",
    r"(?i)heparin",
    r"(?i)aspirin",
    r"(?i)clopidogrel|plavix",
    r"(?i)metformin",
    r"(?i)insulin",
    r"(?i)levothyroxine|synthroid",
    r"(?i)prednisone",
    r"(?i)albuterol|ventolin",
    
    # Radiology and imaging findings
    r"(?i)fracture",
    r"(?i)osteopenia",
    r"(?i)osteoporosis",
    r"(?i)stenosis",
    r"(?i)cardiomegaly",
    r"(?i)effusion",
    r"(?i)mass",
    r"(?i)nodule",
    r"(?i)opacity",
    r"(?i)pneumonia",
    r"(?i)fibrosis",
    r"(?i)atrophy",
    r"(?i)atherosclerosis",
    r"(?i)edema",
    r"(?i)calcification",
    r"(?i)enlarged",
    r"(?i)abnormal",
    r"(?i)lesion",
    
    # Pathology findings
    r"(?i)hyperplasia",
    r"(?i)dysplasia",
    r"(?i)metaplasia",
    r"(?i)atypia",
    r"(?i)anaplasia",
    r"(?i)adenoma",
    r"(?i)granuloma",
    r"(?i)inflammation",
    r"(?i)infiltration",
    r"(?i)necrosis",
]

def extract_medical_terms(text):
    """
    Extract medical terminology from the extracted text
    
    Args:
        text: The text extracted from the document
    
    Returns:
        List of identified medical terms
    """
    try:
        logger.debug("Starting medical term extraction")
        
        # Process the text with spaCy
        doc = nlp(text)
        
        # Extract medical terms using pattern matching
        medical_terms = []
        
        # Use spaCy's entity recognition
        for ent in doc.ents:
            if ent.label_ in ["DISEASE", "CONDITION", "DIAGNOSIS"]:
                medical_terms.append({
                    "term": ent.text,
                    "category": ent.label_,
                    "source": "spaCy NER"
                })
        
        # Dictionaries to map pattern types to categories
        pattern_categories = {
            # Indices for relevant pattern ranges (mapping group of patterns to categories)
            (0, 92): "CHRONIC CONDITION",       # Chronic conditions (0-92)
            (93, 138): "LAB TEST",              # Lab test names (93-138)
            (139, 171): "DIAGNOSTIC FINDING",    # Diagnostic findings (139-171)
            (172, 193): "PROCEDURE",            # Procedures (172-193)
            (194, 215): "MEDICATION",           # Medications (194-215)
            (216, 235): "IMAGING FINDING",      # Imaging findings (216-235)
            (236, 247): "PATHOLOGY FINDING"     # Pathology findings (236-247)
        }
        
        # Use regex patterns for additional medical term extraction
        for pattern_idx, pattern in enumerate(MEDICAL_TERMS_PATTERNS):
            # Determine the category based on pattern index
            category = "CONDITION"  # Default category
            for (start, end), cat in pattern_categories.items():
                if start <= pattern_idx <= end:
                    category = cat
                    break
                    
            matches = re.finditer(pattern, text)
            for match in matches:
                term = match.group(0)
                if term not in [item["term"] for item in medical_terms]:
                    medical_terms.append({
                        "term": term,
                        "category": category,
                        "source": "pattern matching"
                    })
        
        # Enhanced medication extraction
        # Common medication names and classes that might not be caught by suffixes
        common_meds = [
            r"(?i)\bmetformin\b",
            r"(?i)\binsulin\b",
            r"(?i)\baspirin\b",
            r"(?i)\bwarfarin\b",
            r"(?i)\bclopidogrel\b",
            r"(?i)\blevothyroxine\b",
            r"(?i)\bsynthroid\b",
            r"(?i)\blisinopril\b",
            r"(?i)\batorvastatin\b",
            r"(?i)\biosartan\b",
            r"(?i)\bamlodipine\b",
            r"(?i)\bfurosemide\b",
            r"(?i)\blasix\b",
            r"(?i)\bomeprazole\b",
            r"(?i)\bprednisone\b",
            r"(?i)\balbuterol\b",
            r"(?i)\bgabapentin\b",
            r"(?i)\bhydrochlorothiazide\b",
            r"(?i)\bhctz\b",
            r"(?i)\bmetoprolol\b",
        ]
        
        for med in common_meds:
            for match in re.finditer(med, text):
                term = match.group(0)
                if term not in [item["term"] for item in medical_terms]:
                    medical_terms.append({
                        "term": term,
                        "category": "MEDICATION",
                        "source": "medication list"
                    })
        
        # Extract medication mentions by typical drug name suffixes
        medication_pattern = r"(?i)\b[A-Za-z]+(?:mab|zumab|ximab|mumab|olone|statin|sartan|pril|oxacin|cycline|prazole|dipine|kain|ide|barb|azole|micin|parib|tinib|afil|azine|asone|tadine|olam|pam)\b"
        for match in re.finditer(medication_pattern, text):
            term = match.group(0)
            if term not in [item["term"] for item in medical_terms]:
                medical_terms.append({
                    "term": term,
                    "category": "MEDICATION",
                    "source": "medication suffix"
                })
        
        # Extract lab values with abnormal markers or values - common in blood reports
        # Enhanced pattern to capture more lab test names and formats
        lab_value_pattern = r"(?i)(hemoglobin|hematocrit|hgb|hct|rbc|wbc|platelets?|plt|glucose|glu|cholesterol|triglycerides?|hdl|ldl|a1c|hba1c|creatinine|cre|bun|egfr|alt|ast|ggt|alp|bilirubin|bili|albumin|alb|protein|tsh|t[34]|sodium|na|potassium|k|chloride|cl|bicarbonate|co2|calcium|ca|phosphorus|phos|magnesium|mg|ferritin|iron|transferrin|vitamin\s*d|25-oh|vitamin\s*b12|folate|folic|inr|pt|ptt|troponin|trp|bnp|nt-probnp|crp|esr|psa|hcg|cbc|cmp)\s*:?\s*(?:<|>|≤|≥)?\s*(\d+\.?\d*)\s*([a-z%/\-]+)?\s*(?:\(?(high|low|h|l|abnormal|outside\s*reference|above\s*range|below\s*range|elevated|decreased|normal)\)?)??"
        
        # This will capture lab tests with values
        for match in re.finditer(lab_value_pattern, text):
            lab_name = match.group(1).strip()
            lab_value = match.group(2)
            unit = match.group(3) if match.group(3) else ""
            status = match.group(4) if match.group(4) else "measured"
            
            # Create a formatted string that includes the value
            term = f"{lab_name}: {lab_value} {unit}".strip()
            
            # Add a category based on the status if available
            status_lower = status.lower() if status else ""
            category = "ABNORMAL LAB" if status_lower in ['high', 'low', 'h', 'l', 'abnormal', 'outside reference', 'above range', 'below range', 'elevated', 'decreased'] else "LAB VALUE"
            
            medical_terms.append({
                "term": term,
                "category": category,
                "source": "lab value extraction"
            })
        
        # Look for ranges in the format "Reference Range: 4.0-10.0"
        range_pattern = r"(?i)(reference|normal)\s+range[:\s]+(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)"
        for match in re.finditer(range_pattern, text):
            medical_terms.append({
                "term": f"Reference Range: {match.group(2)}-{match.group(3)}",
                "category": "REFERENCE RANGE",
                "source": "reference range extraction"
            })
            
        # Extract ICD codes (often found in medical documents)
        icd_pattern = r"(?i)(?:ICD[-\s]?(?:9|10)[-\s]?(?:CM|PCS)?[-\s]?:?[-\s]?)?\b([A-Z]\d{1,2})\.?(\d{1,2})\b"
        for match in re.finditer(icd_pattern, text):
            code = f"{match.group(1)}.{match.group(2)}"
            medical_terms.append({
                "term": code,
                "category": "ICD CODE",
                "source": "ICD code extraction"
            })
            
        # Extract dates of service or examination dates
        date_patterns = [
            r"(?i)(?:date of (?:service|exam|examination|study|report|visit|admission|discharge))\s*:?\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})",
            r"(?i)(?:service|exam|examination|study|report|visit|admission|discharge) date\s*:?\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})",
            r"(?i)(?:performed|conducted|examined) on\s*:?\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})"
        ]
        
        for pattern in date_patterns:
            for match in re.finditer(pattern, text):
                medical_terms.append({
                    "term": f"Service Date: {match.group(1)}",
                    "category": "SERVICE DATE",
                    "source": "date extraction"
                })
            
        logger.debug(f"Extracted {len(medical_terms)} medical terms")
        return medical_terms
    
    except Exception as e:
        logger.error(f"Error during medical term extraction: {str(e)}")
        raise
