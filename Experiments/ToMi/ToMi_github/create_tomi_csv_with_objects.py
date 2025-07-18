#!/usr/bin/env python3
import pandas as pd
import os
import re
import random
import copy

def get_random_inanimate_object():
    """Generate a random inanimate object name suitable for pretend play"""
    objects = [
        "Teddy bear with blue hat", "Doll with pink dress", "Stuffed bunny with bow",
        "Toy robot with painted face", "Wooden puppet with strings", "Rag doll with button eyes",
        "Plush cat with whiskers", "Baby doll with bonnet", "Toy soldier with helmet",
        "Stuffed elephant with trunk", "Marionette with smile", "Sock puppet with yarn hair",
        "Toy horse with mane", "Plush dog with collar", "Stuffed owl with wings",
        "Toy dinosaur with spots", "Rag bunny with floppy ears", "Doll with curly hair",
        "Teddy with red scarf", "Puppet with big nose", "Plush bear with vest",
        "Toy mouse with whiskers", "Stuffed pig with tail", "Doll with freckles",
        "Toy monkey with banana", "Plush sheep with wool", "Stuffed duck with hat",
        "Toy cow with bell", "Rag cat with stripes", "Doll with pigtails"
    ]
    return random.choice(objects)

def extract_characters_from_story(story):
    """Extract the three main characters from the story"""
    characters = []
    for step in story:
        content = step['content']
        # Skip questions
        if '\t' in content and '?' in content:
            continue
        
        # Look for "X entered" pattern to identify characters
        match = re.search(r'(\w+)\s+entered\s+', content)
        if match:
            char_name = match.group(1)
            if char_name not in characters:
                characters.append(char_name)
    
    return characters

def replace_character_in_content(content, old_char, new_char):
    """Replace character name in content, handling various grammatical forms"""
    # Replace at word boundaries
    content = re.sub(r'\b' + re.escape(old_char) + r'\b', new_char, content)
    return content

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

def extract_story_with_numbers_and_replacement(story_group):
    """Extract story with numbered sentences and replace second character with object"""
    # Use the first story to extract characters and create the base story
    base_story = story_group[0]
    characters = extract_characters_from_story(base_story)
    
    # If we have at least 2 characters, replace the second one
    if len(characters) >= 2:
        second_char = characters[1]  # This is the "B" character
        replacement_object = get_random_inanimate_object()
        
        # Process all stories in the group
        processed_stories = []
        for story in story_group:
            processed_story = []
            for step in story:
                new_step = copy.deepcopy(step)
                new_step['content'] = replace_character_in_content(
                    step['content'], second_char, replacement_object
                )
                processed_story.append(new_step)
            processed_stories.append(processed_story)
        
        return processed_stories, second_char, replacement_object
    
    return story_group, None, None

def extract_story_components(story, original_char_b, replacement_object):
    """Extract story components with character replacement"""
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

def should_exclude_question(question, original_char_b):
    """Check if question should be excluded (asks about B's thoughts or actions)"""
    if not original_char_b:
        return False
    
    # Exclude questions about B's beliefs or thoughts
    if f"Where will {original_char_b} look for" in question:
        return True
    if f"Where does {original_char_b} think that" in question:
        return True
    if f"think that {original_char_b} searches for" in question:
        return True
    
    return False

def create_csv_data(story_groups):
    """Create structured CSV data from story groups"""
    csv_data = []
    
    for story_group in story_groups:
        if len(story_group) != 6:
            continue  # Skip incomplete story groups
        
        # Replace second character with object
        processed_stories, original_char_b, replacement_object = extract_story_with_numbers_and_replacement(story_group)
        
        # Initialize row with empty values (including B-related columns)
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
        for story in processed_stories:
            components = extract_story_components(story, original_char_b, replacement_object)
            
            # Set the story (same for all variants)
            if not row['Story']:
                row['Story'] = components['numbered_story']
            
            # No longer skip questions about B's thoughts - include all questions
            
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
    # Set random seed for reproducibility
    random.seed(42)
    
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
    output_path = '/Users/taeyoonkwack/Documents/Multi-Agent/ENV/ToMi/tomi_dataset_with_objects.csv'
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