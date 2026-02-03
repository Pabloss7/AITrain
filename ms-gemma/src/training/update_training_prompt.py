import json
import re

def create_enhanced_prompt(role, features_text):
    """Create an enhanced system prompt with more context and instructions."""
    
    enhanced_prompt = f"""You are an expert League of Legends coach.

Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

Use the information below to:
- Explain WHY each aspect negatively impacts the player's performance
- Provide concrete in-game advice
- Adapt recommendations to the player's role

Avoid generic tips. Be specific and practical.

ANALYSIS DATA:
Player analyzed:
- Role: {role}

In-game aspects with negative impact detected:
{features_text}"""
    
    return enhanced_prompt

def parse_existing_input(input_text):
    """Parse the existing input format to extract role and features."""
    # Extract role
    role_match = re.search(r'Role: (\w+)', input_text)
    role = role_match.group(1) if role_match else "UNKNOWN"
    
    # Extract features section
    features_section = re.search(
        r'In-game aspects with negative impact detected:\n(.*)',
        input_text,
        re.DOTALL
    )
    
    if features_section:
        features_text = features_section.group(1).strip()
    else:
        features_text = ""
    
    return role, features_text

def process_jsonl_file(input_file, output_file):
    """Process the JSONL file and update the input prompts."""
    processed_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            if line.strip():  # Skip empty lines
                data = json.loads(line)
                
                # Parse the existing input
                role, features_text = parse_existing_input(data['input'])
                
                # Create enhanced prompt
                data['input'] = create_enhanced_prompt(role, features_text)
                
                # Write the modified data
                outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                processed_count += 1
    
    return processed_count

if __name__ == "__main__":
    input_file = "data/lol_coaching_clean_700.jsonl"
    output_file = "data/lol_coaching_enhanced_700.jsonl"
    
    print(f"Processing {input_file}...")
    count = process_jsonl_file(input_file, output_file)
    print(f"✓ Processed {count} examples")
    print(f"✓ Output saved to: {output_file}")
    
    # Show a sample
    print("\n--- Sample Enhanced Input ---")
    with open(output_file, 'r', encoding='utf-8') as f:
        sample = json.loads(f.readline())
    
    print(sample['input'])
    print("\n--- Sample Output ---")
    print(sample['output'][:300] + "...")
