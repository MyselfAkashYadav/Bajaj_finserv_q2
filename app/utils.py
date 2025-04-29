import re

def parse_lab_tests(text):
 
    lines = text.split('\n')
    results = []
   
#    regex expression 
    pattern = r"(?P<test_name>[A-Za-z\s\(\)]+)\s+(?P<value>\d+\.?\d*)\s+(?P<unit>[A-Za-z%/]+)?\s*(?P<range>\d+\.?\d*\s*-\s*\d+\.?\d*)"
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        match = re.search(pattern, line)
        if match:

            test_name = match.group("test_name").strip()
            value = match.group("value")
            
    
            unit = match.group("unit") if match.group("unit") else ""
            
            range_str = match.group("range").replace(" ", "")
            
            try:
                lower, upper = map(float, range_str.split('-'))
                value_float = float(value)
                out_of_range = not (lower <= value_float <= upper)
                
                results.append({
                    "test_name": test_name,
                    "test_value": value,
                    "bio_reference_range": range_str,
                    "test_unit": unit,
                    "lab_test_out_of_range": out_of_range
                })
            except (ValueError, TypeError):
                continue
    return results

def preprocess_text(text):

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'[^\w\s\.\-\(\)/%]', '', text)
    
    return text

