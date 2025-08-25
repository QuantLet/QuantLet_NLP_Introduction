"""
Utility functions for Shakespeare text processing and visualization
BSc-level NLP course - ASE Summer School 2025
"""

import re
import requests
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter, defaultdict
from typing import List, Tuple, Dict
import pickle
import os

def download_shakespeare_sonnets() -> str:
    """
    Download Shakespeare's sonnets from Project Gutenberg.
    Returns cleaned text suitable for NLP tasks.
    """
    # Check if already downloaded
    cache_file = "shakespeare_sonnets.txt"
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    # Download from Project Gutenberg
    url = "https://www.gutenberg.org/files/1041/1041-0.txt"
    response = requests.get(url)
    text = response.text
    
    # Extract just the sonnets (remove header and footer)
    start_marker = "THE SONNETS"
    end_marker = "End of the Project Gutenberg"
    
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        sonnets = text[start_idx:end_idx]
    else:
        sonnets = text
    
    # Clean the text
    sonnets = re.sub(r'\n\s*\n', '\n', sonnets)  # Remove empty lines
    sonnets = re.sub(r'^\s*\d+\s*$', '', sonnets, flags=re.MULTILINE)  # Remove sonnet numbers
    sonnets = sonnets.lower()  # Lowercase
    
    # Cache for future use
    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write(sonnets)
    
    return sonnets

def tokenize(text: str, keep_punctuation: bool = False) -> List[str]:
    """
    Simple tokenization for educational purposes.
    
    Args:
        text: Input text
        keep_punctuation: Whether to keep punctuation as separate tokens
    
    Returns:
        List of tokens
    """
    if keep_punctuation:
        # Keep punctuation as separate tokens
        tokens = re.findall(r'\w+|[.!?,;]', text.lower())
    else:
        # Words only
        tokens = re.findall(r'\b\w+\b', text.lower())
    
    return tokens

def create_vocabulary(tokens: List[str], min_freq: int = 2) -> Dict[str, int]:
    """
    Create vocabulary with word-to-index mapping.
    
    Args:
        tokens: List of tokens
        min_freq: Minimum frequency to include in vocabulary
    
    Returns:
        Dictionary mapping words to indices
    """
    freq = Counter(tokens)
    
    # Special tokens
    vocab = {'<PAD>': 0, '<UNK>': 1, '<START>': 2, '<END>': 3}
    
    # Add words above minimum frequency
    idx = len(vocab)
    for word, count in freq.most_common():
        if count >= min_freq:
            vocab[word] = idx
            idx += 1
        else:
            break
    
    return vocab

def calculate_perplexity(probabilities: List[float]) -> float:
    """
    Calculate perplexity from a list of probabilities.
    
    Perplexity = 2^(-avg(log2(p)))
    
    Args:
        probabilities: List of prediction probabilities
    
    Returns:
        Perplexity score (lower is better)
    """
    # Avoid log(0)
    probs = np.array(probabilities)
    probs = np.clip(probs, 1e-10, 1.0)
    
    # Calculate perplexity
    avg_log_prob = np.mean(np.log2(probs))
    perplexity = 2 ** (-avg_log_prob)
    
    return perplexity

def plot_word_frequencies(tokens: List[str], top_n: int = 20) -> go.Figure:
    """
    Create interactive bar chart of word frequencies.
    
    Args:
        tokens: List of tokens
        top_n: Number of top words to display
    
    Returns:
        Plotly figure
    """
    freq = Counter(tokens)
    top_words = freq.most_common(top_n)
    
    words, counts = zip(*top_words)
    
    fig = go.Figure([go.Bar(
        x=list(words),
        y=list(counts),
        text=list(counts),
        textposition='auto',
        marker_color='lightblue',
        hovertemplate='Word: %{x}<br>Count: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=f'Top {top_n} Most Frequent Words',
        xaxis_title='Word',
        yaxis_title='Frequency',
        font=dict(size=10),
        height=400,
        showlegend=False
    )
    
    return fig

def plot_bigram_heatmap(tokens: List[str], top_n: int = 15) -> go.Figure:
    """
    Create heatmap of bigram frequencies.
    
    Args:
        tokens: List of tokens
        top_n: Number of top words to include
    
    Returns:
        Plotly figure
    """
    # Get top words
    freq = Counter(tokens)
    top_words = [word for word, _ in freq.most_common(top_n)]
    
    # Count bigrams
    bigram_counts = defaultdict(lambda: defaultdict(int))
    for i in range(len(tokens) - 1):
        if tokens[i] in top_words and tokens[i+1] in top_words:
            bigram_counts[tokens[i]][tokens[i+1]] += 1
    
    # Create matrix
    matrix = np.zeros((top_n, top_n))
    for i, word1 in enumerate(top_words):
        for j, word2 in enumerate(top_words):
            matrix[i, j] = bigram_counts[word1][word2]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=top_words,
        y=top_words,
        colorscale='Blues',
        text=matrix.astype(int),
        texttemplate='%{text}',
        textfont={"size": 8},
        hovertemplate='%{y} → %{x}<br>Count: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Bigram Frequency Heatmap',
        xaxis_title='Second Word',
        yaxis_title='First Word',
        font=dict(size=10),
        height=500,
        width=600
    )
    
    return fig

def plot_prediction_probabilities(word_probs: List[Tuple[str, float]], 
                                 title: str = "Next Word Probabilities") -> go.Figure:
    """
    Create bar chart of prediction probabilities.
    
    Args:
        word_probs: List of (word, probability) tuples
        title: Chart title
    
    Returns:
        Plotly figure
    """
    if not word_probs:
        return go.Figure()
    
    words, probs = zip(*word_probs)
    
    fig = go.Figure([go.Bar(
        x=list(probs),
        y=list(words),
        orientation='h',
        text=[f'{p:.1%}' for p in probs],
        textposition='auto',
        marker_color=px.colors.sequential.Viridis[:len(words)],
        hovertemplate='%{y}: %{x:.2%}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title='Probability',
        yaxis_title='Word',
        font=dict(size=10),
        height=max(300, len(words) * 30),
        showlegend=False,
        xaxis=dict(tickformat='.0%')
    )
    
    return fig

def generate_text_comparison(methods_outputs: Dict[str, str]) -> go.Figure:
    """
    Create side-by-side comparison of text generation methods.
    
    Args:
        methods_outputs: Dictionary mapping method name to generated text
    
    Returns:
        Plotly figure with text comparison
    """
    fig = go.Figure()
    
    # Create table data
    methods = list(methods_outputs.keys())
    outputs = list(methods_outputs.values())
    
    # Wrap long text
    wrapped_outputs = []
    for text in outputs:
        if len(text) > 80:
            wrapped = '<br>'.join([text[i:i+80] for i in range(0, len(text), 80)])
            wrapped_outputs.append(wrapped)
        else:
            wrapped_outputs.append(text)
    
    fig.add_trace(go.Table(
        header=dict(
            values=['Method', 'Generated Text'],
            fill_color='lightblue',
            align='left',
            font=dict(size=12)
        ),
        cells=dict(
            values=[methods, wrapped_outputs],
            fill_color=['white', 'whitesmoke'],
            align='left',
            font=dict(size=10),
            height=30
        )
    ))
    
    fig.update_layout(
        title='Text Generation Comparison',
        font=dict(size=10),
        height=400,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return fig

def save_model(model, filename: str):
    """Save a model to disk using pickle."""
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {filename}")

def load_model(filename: str):
    """Load a model from disk."""
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded from {filename}")
    return model

# Color scheme for consistency
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8'
}

def print_section_header(title: str):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60 + "\n")