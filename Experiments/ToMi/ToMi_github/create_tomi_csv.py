#!/usr/bin/env python3
import pandas as pd
import os
import re

def parse_tomi_data(file_path):
    """Parse ToMi dataset where each story has 6 question variants"""
    stories = []
    current_story_group = []
    current_story = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Extract step number and content
            match = re.match(r'\s*(\d+)\s+(.*)', line)
            if match:
                step_num = int(match.group(1))
                content = match.group(2)
                
                # If this is step 1, we're starting a new story
                if step_num == 1:
                    # If we have a complete story group (6 stories), process it
                    if len(current_story_group) == 6:
                        stories.append(current_story_group)
                        current_story_group = []
                    
                    # If we have a previous story, add it to the group
                    if current_story:
                        current_story_group.append(current_story)
                    
                    current_story = []
                
                current_story.append({
                    'step_num': step_num,
                    'content': content
                })
        
        # Add the last story to the group
        if current_story:
            current_story_group.append(current_story)
        
        # Add the last story group
        if len(current_story_group) == 6:
            stories.append(current_story_group)
    
    return stories

def extract_story_with_numbers(story):
    """Extract story with numbered sentences"""
    story_sentences = []
    question = ""
    answer = ""
    
    for step in story:
        content = step['content']
        step_num = step['step_num']
        
        # Check if this is a question (contains tab and question mark)
        if '\t' in content and '?' in content:
            parts = content.split('\t')
            question = parts[0]
            answer = parts[1] if len(parts) > 1 else ""
        else:
            # Add sentence with number
            story_sentences.append(f"{step_num}. {content}")
    
    return {
        'numbered_story': '\n'.join(story_sentences),
        'question': question,
        'answer': answer
    }

def categorize_question(question):
    """Categorize question type based on content"""
    if 'at the beginning' in question:
        return 'memory'
    elif 'really' in question:
        return 'reality'
    elif 'think that' in question:
        return 'second_order_belief'
    elif 'will' in question and 'look for' in question:
        return 'first_order_belief'
    else:
        return 'unknown'

def create_csv_data(story_groups):
    """Create structured CSV data from story groups"""
    csv_data = []
    
    for story_group in story_groups:
        if len(story_group) != 6:
            continue  # Skip incomplete story groups
        
        # Initialize row with empty values
        row = {
            'Story': '',
            'Reality Question': '',
            'Reality Answer': '',
            'Memory Question': '',
            'Memory Answer': '',
            'First-Order Belief A Question': '',
            'First-Order Belief A Answer': '',
            'First-Order Belief B Question': '',
            'First-Order Belief B Answer': '',
            'Second-Order Belief A Question': '',
            'Second-Order Belief A Answer': '',
            'Second-Order Belief B Question': '',
            'Second-Order Belief B Answer': ''
        }
        
        # Counters for multiple questions of same type
        first_order_count = 0
        second_order_count = 0
        
        # Process each story variant in the group
        for story in story_group:
            components = extract_story_with_numbers(story)
            
            # Set the story (same for all variants)
            if not row['Story']:
                row['Story'] = components['numbered_story']
            
            # Categorize and assign questions
            question_type = categorize_question(components['question'])
            question = components['question']
            answer = components['answer']
            
            if question_type == 'reality':
                row['Reality Question'] = question
                row['Reality Answer'] = answer
            elif question_type == 'memory':
                row['Memory Question'] = question
                row['Memory Answer'] = answer
            elif question_type == 'first_order_belief':
                if first_order_count == 0:
                    row['First-Order Belief A Question'] = question
                    row['First-Order Belief A Answer'] = answer
                    first_order_count += 1
                else:
                    row['First-Order Belief B Question'] = question
                    row['First-Order Belief B Answer'] = answer
            elif question_type == 'second_order_belief':
                if second_order_count == 0:
                    row['Second-Order Belief A Question'] = question
                    row['Second-Order Belief A Answer'] = answer
                    second_order_count += 1
                else:
                    row['Second-Order Belief B Question'] = question
                    row['Second-Order Belief B Answer'] = answer
        
        csv_data.append(row)
    
    return csv_data

def main():
    # Parse train, val, and test datasets
    data_dir = '/Users/taeyoonkwack/Documents/Multi-Agent/ENV/ToMi/data'
    all_data = []
    
    for dataset in ['train', 'val', 'test']:
        file_path = os.path.join(data_dir, f'{dataset}.txt')
        if os.path.exists(file_path):
            print(f"Processing {dataset} dataset...")
            story_groups = parse_tomi_data(file_path)
            print(f"Found {len(story_groups)} complete story groups in {dataset}")
            csv_data = create_csv_data(story_groups)
            all_data.extend(csv_data)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV
    output_path = '/Users/taeyoonkwack/Documents/Multi-Agent/ENV/ToMi/tomi_dataset_final.csv'
    df.to_csv(output_path, index=False)
    print(f"CSV file created: {output_path}")
    print(f"Total story groups: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Display first few rows
    if len(df) > 0:
        print("\nFirst row sample:")
        first_row = df.iloc[0]
        print(f"Story: {first_row['Story']}")
        print(f"Memory Q: {first_row['Memory Question']}")
        print(f"Memory A: {first_row['Memory Answer']}")
        print(f"Reality Q: {first_row['Reality Question']}")
        print(f"Reality A: {first_row['Reality Answer']}")
        print(f"First-Order A Q: {first_row['First-Order Belief A Question']}")
        print(f"First-Order A A: {first_row['First-Order Belief A Answer']}")
        print(f"First-Order B Q: {first_row['First-Order Belief B Question']}")
        print(f"First-Order B A: {first_row['First-Order Belief B Answer']}")
        print(f"Second-Order A Q: {first_row['Second-Order Belief A Question']}")
        print(f"Second-Order A A: {first_row['Second-Order Belief A Answer']}")
        print(f"Second-Order B Q: {first_row['Second-Order Belief B Question']}")
        print(f"Second-Order B A: {first_row['Second-Order Belief B Answer']}")

if __name__ == "__main__":
    main()