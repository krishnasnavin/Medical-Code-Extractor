import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Path to the HCC codes mapping file
HCC_CODES_FILE = Path(__file__).parent / "static" / "data" / "hcc_codes.json"

def load_hcc_codes():
    """
    Load HCC codes from the JSON file
    
    Returns:
        Dictionary of HCC codes mappings
    """
    try:
        if os.path.exists(HCC_CODES_FILE):
            with open(HCC_CODES_FILE, 'r') as f:
                hcc_codes = json.load(f)
                logger.debug(f"Loaded {len(hcc_codes)} HCC code mappings")
                return hcc_codes
        else:
            logger.warning(f"HCC codes file not found at {HCC_CODES_FILE}")
            # Return a fallback minimal set of codes
            return {
                "diabetes": {"code": "HCC 19", "description": "Diabetes without Complication"},
                "diabetes type 2": {"code": "HCC 19", "description": "Diabetes without Complication"},
                "diabetes type 1": {"code": "HCC 17", "description": "Diabetes with Acute Complications"},
                "diabetic": {"code": "HCC 19", "description": "Diabetes without Complication"},
                "hypertension": {"code": "HCC 85", "description": "Congestive Heart Failure"},
                "heart failure": {"code": "HCC 85", "description": "Congestive Heart Failure"},
                "chronic kidney disease": {"code": "HCC 136", "description": "Chronic Kidney Disease, Stage 5"},
                "ckd": {"code": "HCC 136", "description": "Chronic Kidney Disease, Stage 5"},
                "copd": {"code": "HCC 111", "description": "Chronic Obstructive Pulmonary Disease"},
                "asthma": {"code": "HCC 110", "description": "Asthma"},
                "cancer": {"code": "HCC 12", "description": "Breast, Prostate, Colorectal and Other Cancers and Tumors"},
                "stroke": {"code": "HCC 100", "description": "Cerebrovascular Disease, Except Hemorrhage or Aneurysm"},
                "alzheimer": {"code": "HCC 51", "description": "Dementia With Complications"},
                "dementia": {"code": "HCC 52", "description": "Dementia Without Complication"},
                "depression": {"code": "HCC 58", "description": "Major Depressive, Bipolar, and Paranoid Disorders"},
                "anxiety": {"code": "HCC 59", "description": "Reactive and Unspecified Psychosis, Delusional Disorders"},
                "cirrhosis": {"code": "HCC 27", "description": "End-Stage Liver Disease"},
                "hepatitis": {"code": "HCC 29", "description": "Chronic Hepatitis"},
                "emphysema": {"code": "HCC 111", "description": "Chronic Obstructive Pulmonary Disease"},
                "obesity": {"code": "HCC 22", "description": "Morbid Obesity"}
            }
    except Exception as e:
        logger.error(f"Error loading HCC codes: {str(e)}")
        return {}

def map_to_hcc_codes(medical_terms):
    """
    Map the extracted medical terms to HCC codes
    
    Args:
        medical_terms: List of extracted medical terms
    
    Returns:
        List of mapped HCC codes with details
    """
    try:
        logger.debug("Starting HCC code mapping")
        
        # Load HCC codes
        hcc_mapping = load_hcc_codes()
        
        # Expanded lab test mappings for more comprehensive coverage
        lab_test_mappings = {
            # Blood glucose abnormalities
            "glucose": {"high": {"code": "HCC 19", "description": "Diabetes without Complication"}},
            "glu": {"high": {"code": "HCC 19", "description": "Diabetes without Complication"}},
            "a1c": {"high": {"code": "HCC 17", "description": "Diabetes with Acute Complications"}},
            "hba1c": {"high": {"code": "HCC 17", "description": "Diabetes with Acute Complications"}},
            "glycosylated hemoglobin": {"high": {"code": "HCC 17", "description": "Diabetes with Acute Complications"}},
            "fasting glucose": {"high": {"code": "HCC 19", "description": "Diabetes without Complication"}},
            
            # Blood cell abnormalities
            "hemoglobin": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "hgb": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "hematocrit": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "hct": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "rbc": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "red blood cell": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "wbc": {
                "high": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"},
                "low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}
            },
            "white blood cell": {
                "high": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"},
                "low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}
            },
            "platelets": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "plt": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            
            # Cholesterol and lipids
            "cholesterol": {"high": {"code": "HCC 88", "description": "Unstable Angina and Other Acute Ischemic Heart Disease"}},
            "triglycerides": {"high": {"code": "HCC 88", "description": "Unstable Angina and Other Acute Ischemic Heart Disease"}},
            "ldl": {"high": {"code": "HCC 88", "description": "Unstable Angina and Other Acute Ischemic Heart Disease"}},
            "hdl": {"low": {"code": "HCC 88", "description": "Unstable Angina and Other Acute Ischemic Heart Disease"}},
            
            # Kidney function
            "creatinine": {"high": {"code": "HCC 138", "description": "Chronic Kidney Disease, Moderate (Stage 3)"}},
            "cre": {"high": {"code": "HCC 138", "description": "Chronic Kidney Disease, Moderate (Stage 3)"}},
            "bun": {"high": {"code": "HCC 138", "description": "Chronic Kidney Disease, Moderate (Stage 3)"}},
            "blood urea nitrogen": {"high": {"code": "HCC 138", "description": "Chronic Kidney Disease, Moderate (Stage 3)"}},
            "egfr": {"low": {"code": "HCC 138", "description": "Chronic Kidney Disease, Moderate (Stage 3)"}},
            "estimated glomerular filtration rate": {"low": {"code": "HCC 138", "description": "Chronic Kidney Disease, Moderate (Stage 3)"}},
            
            # Liver function
            "alt": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "alanine aminotransferase": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "ast": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "aspartate aminotransferase": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "ggt": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "gamma-glutamyl transferase": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "alkaline phosphatase": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "alp": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "bilirubin": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            "bili": {"high": {"code": "HCC 29", "description": "Chronic Hepatitis"}},
            
            # Thyroid
            "tsh": {
                "high": {"code": "HCC 21", "description": "Hypothyroidism"},
                "low": {"code": "HCC 21", "description": "Hyperthyroidism"}
            },
            "thyroid stimulating hormone": {
                "high": {"code": "HCC 21", "description": "Hypothyroidism"},
                "low": {"code": "HCC 21", "description": "Hyperthyroidism"}
            },
            "t3": {"high": {"code": "HCC 21", "description": "Hyperthyroidism"}},
            "t4": {"high": {"code": "HCC 21", "description": "Hyperthyroidism"}},
            "thyroxine": {"high": {"code": "HCC 21", "description": "Hyperthyroidism"}},
            
            # Electrolytes
            "sodium": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "na": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "potassium": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "k": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "calcium": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "ca": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "chloride": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "cl": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "bicarbonate": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "co2": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "magnesium": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "mg": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "phosphorus": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            "phos": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 22", "description": "Metabolic Disorders"}
            },
            
            # Nutritional factors
            "vitamin d": {"low": {"code": "HCC 22", "description": "Metabolic Disorders"}},
            "25-oh": {"low": {"code": "HCC 22", "description": "Metabolic Disorders"}},
            "vitamin b12": {"low": {"code": "HCC 21", "description": "Nutritional Deficiency"}},
            "folate": {"low": {"code": "HCC 21", "description": "Nutritional Deficiency"}},
            "folic": {"low": {"code": "HCC 21", "description": "Nutritional Deficiency"}},
            "ferritin": {
                "high": {"code": "HCC 22", "description": "Metabolic Disorders"},
                "low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}
            },
            "iron": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "transferrin": {"low": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            
            # Other important lab values
            "troponin": {"high": {"code": "HCC 86", "description": "Acute Myocardial Infarction"}},
            "trp": {"high": {"code": "HCC 86", "description": "Acute Myocardial Infarction"}},
            "bnp": {"high": {"code": "HCC 85", "description": "Congestive Heart Failure"}},
            "brain natriuretic peptide": {"high": {"code": "HCC 85", "description": "Congestive Heart Failure"}},
            "nt-probnp": {"high": {"code": "HCC 85", "description": "Congestive Heart Failure"}},
            "crp": {"high": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "c-reactive protein": {"high": {"code": "HCC 2", "description": "Sepsis, Severe Blood Related Conditions"}},
            "esr": {"high": {"code": "HCC 40", "description": "Rheumatoid Arthritis and Inflammatory Connective Tissue Disease"}},
            "erythrocyte sedimentation rate": {"high": {"code": "HCC 40", "description": "Rheumatoid Arthritis and Inflammatory Connective Tissue Disease"}},
            "psa": {"high": {"code": "HCC 12", "description": "Breast, Prostate, Colorectal and Other Cancers and Tumors"}},
            "prostate specific antigen": {"high": {"code": "HCC 12", "description": "Breast, Prostate, Colorectal and Other Cancers and Tumors"}},
            "albumin": {"low": {"code": "HCC 22", "description": "Metabolic Disorders"}},
            "alb": {"low": {"code": "HCC 22", "description": "Metabolic Disorders"}},
            "protein": {"low": {"code": "HCC 21", "description": "Protein-Calorie Malnutrition"}},
            "inr": {"high": {"code": "HCC 28", "description": "Cirrhosis of Liver"}},
            "international normalized ratio": {"high": {"code": "HCC 28", "description": "Cirrhosis of Liver"}},
            "pt": {"high": {"code": "HCC 28", "description": "Cirrhosis of Liver"}},
            "prothrombin time": {"high": {"code": "HCC 28", "description": "Cirrhosis of Liver"}},
            "ptt": {"high": {"code": "HCC 28", "description": "Cirrhosis of Liver"}},
            "partial thromboplastin time": {"high": {"code": "HCC 28", "description": "Cirrhosis of Liver"}}
        }
        
        # Map medical terms to HCC codes
        mapped_codes = []
        
        # Dictionary to track which terms have been mapped
        # This helps avoid duplicate mappings for the same condition
        mapped_terms = set()
        
        for term_data in medical_terms:
            original_term = term_data["term"]
            category = term_data["category"]
            term = original_term.lower()
            
            # Skip if we've already mapped this exact term
            if term in mapped_terms:
                continue
                
            # Add to tracked terms
            mapped_terms.add(term)
            
            # Initialize the matched flag for this term
            matched = False
            
            # Special handling for ICD codes - direct mapping
            if category == "ICD CODE":
                mapped_codes.append({
                    "term": original_term,
                    "hcc_code": "ICD: " + term,
                    "description": "ICD Code",
                    "confidence": "high"
                })
                continue
            
            # Special handling for lab values with abnormal results
            if category in ["LAB VALUE", "ABNORMAL LAB"]:
                # Extract lab test name and status
                lab_parts = term.split(":")
                if len(lab_parts) > 0:
                    lab_name = lab_parts[0].strip().lower()
                    
                    # Get lab value and unit if available
                    lab_value_info = lab_parts[1].strip() if len(lab_parts) > 1 else ""
                    
                    # Determine if high or low
                    status = "normal"
                    # First check explicit labels
                    if "high" in term.lower() or "elevated" in term.lower() or "above range" in term.lower() or "h)" in term.lower() or "(h" in term.lower():
                        status = "high"
                    elif "low" in term.lower() or "decreased" in term.lower() or "below range" in term.lower() or "l)" in term.lower() or "(l" in term.lower():
                        status = "low"
                    elif category == "ABNORMAL LAB":  # If marked as abnormal but no direction specified
                        status = "abnormal"
                    
                    # Check if we have a mapping for this lab test
                    for lab_key in lab_test_mappings:
                        if lab_key in lab_name:
                            if status == "high" and "high" in lab_test_mappings[lab_key]:
                                code_data = lab_test_mappings[lab_key]["high"]
                                mapped_codes.append({
                                    "term": original_term,
                                    "hcc_code": code_data["code"],
                                    "description": code_data["description"],
                                    "confidence": "medium"
                                })
                                matched = True
                                break
                            elif status == "low" and "low" in lab_test_mappings[lab_key]:
                                code_data = lab_test_mappings[lab_key]["low"]
                                mapped_codes.append({
                                    "term": original_term,
                                    "hcc_code": code_data["code"],
                                    "description": code_data["description"],
                                    "confidence": "medium"
                                })
                                matched = True
                                break
                            elif status == "abnormal" and ("high" in lab_test_mappings[lab_key] or "low" in lab_test_mappings[lab_key]):
                                # If marked abnormal but no direction, use the first available mapping
                                code_data = next(iter(lab_test_mappings[lab_key].values()))
                                mapped_codes.append({
                                    "term": original_term,
                                    "hcc_code": code_data["code"],
                                    "description": code_data["description"],
                                    "confidence": "low"  # Lower confidence since we don't know if high or low
                                })
                                matched = True
                                break
                
                # If we've already matched a lab value, continue to the next term
                if matched:
                    continue
            
            # Enhanced category-based mapping for more accurate results
            confidence_level = "medium"
            
            # Adjust confidence based on category
            if category in ["CHRONIC CONDITION", "DIAGNOSTIC FINDING"]:
                confidence_level = "high"
            elif category in ["MEDICATION", "PROCEDURE", "SERVICE DATE"]:
                confidence_level = "low"
                
            # For non-lab values or unmatched lab values, continue with regular mapping
            matched = False
            
            # Try direct mapping first - highest confidence
            if term in hcc_mapping:
                code_data = hcc_mapping[term]
                mapped_codes.append({
                    "term": original_term,
                    "hcc_code": code_data["code"],
                    "description": code_data["description"],
                    "confidence": "high"
                })
                continue
            
            # Try exact word matching for better accuracy
            term_words = set(term.split())
            for key, code_data in hcc_mapping.items():
                key_words = set(key.split())
                # If all words in the dictionary key are in the term, it's a strong match
                if key_words.issubset(term_words):
                    mapped_codes.append({
                        "term": original_term,
                        "hcc_code": code_data["code"],
                        "description": code_data["description"],
                        "confidence": confidence_level
                    })
                    matched = True
                    break
                    
            if matched:
                continue
                
            # Try partial matching as a last resort
            for key, code_data in hcc_mapping.items():
                # Check if the key is contained within the term or term is contained within the key
                if key in term or term in key:
                    mapped_codes.append({
                        "term": original_term,
                        "hcc_code": code_data["code"],
                        "description": code_data["description"],
                        "confidence": "low"  # Lower confidence for partial matches
                    })
                    matched = True
                    break
            
            # If no match is found
            if not matched:
                mapped_codes.append({
                    "term": original_term,
                    "hcc_code": "Unknown",
                    "description": "No matching HCC code found",
                    "confidence": "low"
                })
        
        # Sort mapped codes by confidence level
        mapped_codes.sort(key=lambda x: 0 if x["confidence"] == "high" else 1 if x["confidence"] == "medium" else 2)
        
        logger.debug(f"Mapped {len(mapped_codes)} terms to HCC codes")
        return mapped_codes
    
    except Exception as e:
        logger.error(f"Error during HCC code mapping: {str(e)}")
        raise
