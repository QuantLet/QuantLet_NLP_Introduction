# Natural Language Processing Introduction - QuantLet Collection

## ASE Summer School 2025

A comprehensive BSc-level introduction to Natural Language Processing through interactive Jupyter notebooks. This collection provides a progressive learning journey from classical N-gram models to modern transformer architectures, all with minimal mathematical complexity and maximum intuitive understanding.

## Course Structure

### Module 1: NLP_Ngrams
**Simple N-gram Models**
- Character and word-level N-gram construction
- Probabilistic text generation
- Count-based language modeling
- Visualization of N-gram frequencies

### Module 2: NLP_Embeddings
**Word Embeddings and Vector Spaces**
- Word2Vec implementation
- Semantic relationships in vector space
- 3D visualization of word embeddings
- Similarity calculations and clustering

### Module 3: NLP_Neural
**Simple Neural Networks for NLP**
- 2-layer neural network implementation
- Backpropagation for language modeling
- Training visualization and loss curves
- Perplexity metrics

### Module 4: NLP_Compare
**Comparing NLP Methods**
- Performance benchmarks across approaches
- Perplexity comparisons
- Generation quality analysis
- Computational requirements

### Module 5: NLP_TokenJourney
**Token's Journey Through a Transformer**
- Step-by-step token processing
- Embedding and positional encoding
- Multi-head attention visualization
- Layer normalization effects

### Module 6: NLP_Transformers3D
**Transformers in 3D: Visual Journey**
- 3-dimensional geometric interpretation
- Attention as angles in 3D space
- Layer normalization as sphere projection
- Interactive 3D visualizations

### Module 7: NLP_TransformersSimple
**Simplified Transformer Implementation**
- Minimal, educational implementation
- Core components breakdown
- Self-attention mechanism
- Feed-forward networks

### Module 8: NLP_TransformersTraining
**How Transformers Learn**
- Training process visualization in 3D
- Gradient flow and weight updates
- Loss landscape navigation
- Attention pattern evolution

## Key Features

- **Progressive Learning Path**: Each module builds on previous concepts
- **Interactive Visualizations**: All notebooks include interactive plots and animations
- **Minimal Mathematics**: Focus on intuition over formulas
- **Self-Contained**: Each notebook can run independently
- **Shakespeare Dataset**: Classic text for all examples
- **3D Visualizations**: Unique geometric interpretations for deep understanding

## Technical Requirements

```python
# Core dependencies
numpy
matplotlib
plotly
tensorflow
scikit-learn
gensim
pandas
```

## Dataset

All modules use Shakespeare's sonnets (`shakespeare_sonnets.txt`) as the primary dataset, providing:
- Rich vocabulary (~5000 unique words)
- Poetic structure for interesting patterns
- Cultural familiarity
- Sufficient size for meaningful models

## Learning Objectives

By completing these modules, students will understand:
1. Evolution from count-based to neural language models
2. How word embeddings capture semantic meaning
3. Transformer architecture components and their functions
4. Attention mechanisms and their geometric interpretation
5. Training dynamics of modern language models

## Usage

Each notebook is designed to be run sequentially within its module. Start with Module 1 (NLP_Ngrams) and progress through to Module 8 (NLP_TransformersTraining) for the complete learning experience.

```python
# Example: Running the first module
cd NLP_Ngrams
jupyter notebook 1_simple_ngrams.ipynb
```

## Educational Philosophy

These materials emphasize:
- **Visual Learning**: Complex concepts through visualizations
- **Hands-On Experience**: Interactive code examples
- **Intuitive Understanding**: Geometric and visual interpretations
- **Practical Implementation**: Working code over theory

## Author

**Joerg Osterrieder**  
ASE Summer School 2025

## License

Educational use permitted. Please cite when using these materials.

## Acknowledgments

Created for the ASE Summer School 2025, these materials represent a modern approach to teaching NLP concepts through visualization and interaction rather than mathematical formalism.