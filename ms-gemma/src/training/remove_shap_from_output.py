import json
import re

def remove_shap_from_output(output_text):
    """Remove SHAP values from the output text while keeping the rest of the message."""
    # Pattern to match ", SHAP: -X.XXX" where X is any digit
    pattern = r', SHAP: -?\d+\.\d+'
    cleaned_output = re.sub(pattern, '', output_text)
    return cleaned_output

def process_jsonl_file(input_file, output_file):
    """Process the JSONL file and remove SHAP values from outputs."""
    processed_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            if line.strip():  # Skip empty lines
                data = json.loads(line)
                
                # Remove SHAP values from output
                data['output'] = remove_shap_from_output(data['output'])
                
                # Write the modified data
                outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                processed_count += 1
    
    return processed_count

if __name__ == "__main__":
    input_file = "data/lol_coaching_shap_explicit_700.jsonl"
    output_file = "data/lol_coaching_clean_700.jsonl"
    
    print(f"Processing {input_file}...")
    count = process_jsonl_file(input_file, output_file)
    print(f"✓ Processed {count} examples")
    print(f"✓ Output saved to: {output_file}")
    
    # Show a sample before/after
    print("\n--- Sample Comparison ---")
    with open(input_file, 'r', encoding='utf-8') as f:
        original = json.loads(f.readline())
    
    with open(output_file, 'r', encoding='utf-8') as f:
        cleaned = json.loads(f.readline())
    
    print("\nORIGINAL OUTPUT:")
    print(original['output'][:200] + "...")
    print("\nCLEANED OUTPUT:")
    print(cleaned['output'][:200] + "...")
