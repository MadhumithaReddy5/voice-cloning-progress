import os
import re
from docx import Document
from docx.shared import Inches
import math

def read_docx(file_path):
    """Read Word document and extract text with structure"""
    doc = Document(file_path)
    content = []
    
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            # Check if it's likely a heading/chapter
            is_heading = (
                paragraph.style.name.startswith('Heading') or
                len(paragraph.text) < 100 and 
                (paragraph.text.upper() == paragraph.text or
                 any(word in paragraph.text.lower() for word in ['chapter', 'section', 'part']))
            )
            
            content.append({
                'text': paragraph.text,
                'is_heading': is_heading,
                'style': paragraph.style.name
            })
    
    return content

def find_chapter_boundaries(content):
    """Find chapter/section boundaries in the content"""
    boundaries = [0]  # Start with beginning
    
    for i, item in enumerate(content):
        if item['is_heading'] and any(word in item['text'].lower() 
                                    for word in ['chapter', 'section', 'part', 'unit']):
            boundaries.append(i)
    
    boundaries.append(len(content))  # End with last item
    return list(set(boundaries))  # Remove duplicates and sort

def calculate_text_size(text):
    """Estimate text size in MB (rough approximation)"""
    return len(text.encode('utf-8')) / (1024 * 1024)

def split_document_intelligently(content, target_chunks=3):
    """Split document into chunks while preserving chapter boundaries"""
    boundaries = find_chapter_boundaries(content)
    boundaries.sort()
    
    # Calculate total size
    total_text = '\n'.join([item['text'] for item in content])
    total_size = calculate_text_size(total_text)
    target_size_per_chunk = total_size / target_chunks
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for i in range(len(boundaries) - 1):
        start_idx = boundaries[i]
        end_idx = boundaries[i + 1]
        
        # Get section content
        section_content = content[start_idx:end_idx]
        section_text = '\n'.join([item['text'] for item in section_content])
        section_size = calculate_text_size(section_text)
        
        # If adding this section would exceed target size and we have content
        if current_size + section_size > target_size_per_chunk and current_chunk:
            chunks.append(current_chunk)
            current_chunk = section_content
            current_size = section_size
        else:
            current_chunk.extend(section_content)
            current_size += section_size
    
    # Add remaining content
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def save_chunks(chunks, base_filename):
    """Save chunks as separate Word documents"""
    base_name = os.path.splitext(base_filename)[0]
    
    for i, chunk in enumerate(chunks, 1):
        # Create new document
        doc = Document()
        
        # Add content to document
        for item in chunk:
            if item['is_heading']:
                # Add as heading
                heading = doc.add_heading(item['text'], level=1)
            else:
                # Add as paragraph
                doc.add_paragraph(item['text'])
        
        # Save chunk
        chunk_filename = f"{base_name}_chunk_{i}.docx"
        doc.save(chunk_filename)
        
        # Calculate and display size
        chunk_text = '\n'.join([item['text'] for item in chunk])
        chunk_size = calculate_text_size(chunk_text)
        
        print(f"Chunk {i}: {chunk_filename}")
        print(f"  Size: {chunk_size:.2f} MB")
        print(f"  Paragraphs: {len(chunk)}")
        print(f"  Characters: {len(chunk_text):,}")
        print()

def basic_plagiarism_check(content):
    """Basic plagiarism detection - looks for repetitive patterns"""
    text = ' '.join([item['text'] for item in content])
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    # Check for duplicate sentences
    duplicates = []
    seen = set()
    
    for sentence in sentences:
        if sentence.lower() in seen:
            duplicates.append(sentence)
        else:
            seen.add(sentence.lower())
    
    # Check for repetitive phrases (5+ words)
    words = text.split()
    phrase_counts = {}
    
    for i in range(len(words) - 4):
        phrase = ' '.join(words[i:i+5]).lower()
        phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
    
    repetitive_phrases = {phrase: count for phrase, count in phrase_counts.items() 
                         if count > 2}
    
    return {
        'duplicate_sentences': duplicates,
        'repetitive_phrases': repetitive_phrases,
        'total_sentences': len(sentences),
        'unique_sentences': len(seen)
    }

def main():
    file_path = r"C:\Users\CPU\Downloads\Probability_Lasya.docx"
    
    print("Reading document...")
    content = read_docx(file_path)
    
    print(f"Document loaded: {len(content)} paragraphs")
    
    # Basic plagiarism check
    print("\nPerforming basic plagiarism check...")
    plagiarism_results = basic_plagiarism_check(content)
    
    print(f"Total sentences: {plagiarism_results['total_sentences']}")
    print(f"Unique sentences: {plagiarism_results['unique_sentences']}")
    print(f"Duplicate sentences found: {len(plagiarism_results['duplicate_sentences'])}")
    print(f"Repetitive phrases found: {len(plagiarism_results['repetitive_phrases'])}")
    
    if plagiarism_results['duplicate_sentences']:
        print("\nSample duplicate sentences:")
        for dup in plagiarism_results['duplicate_sentences'][:3]:
            print(f"  - {dup[:100]}...")
    
    if plagiarism_results['repetitive_phrases']:
        print("\nMost repetitive phrases:")
        sorted_phrases = sorted(plagiarism_results['repetitive_phrases'].items(), 
                              key=lambda x: x[1], reverse=True)
        for phrase, count in sorted_phrases[:5]:
            print(f"  - '{phrase}' (appears {count} times)")
    
    # Split document
    print("\nSplitting document into chunks...")
    chunks = split_document_intelligently(content, target_chunks=3)
    
    print(f"Document split into {len(chunks)} chunks")
    
    # Save chunks
    save_chunks(chunks, file_path)
    
    print("Document processing complete!")

if __name__ == "__main__":
    main()