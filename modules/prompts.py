single_prompt = """
Write a comprehensive summary of the following text. The summary should:
1. Highlight the main points and key ideas
2. Include important details and supporting evidence
3. Maintain the original meaning and intent
4. Be well-structured and coherent

Text to summarize:
{text}

Comprehensive Summary:
"""

map_prompt = """
Write a concise summary of the following text, focusing on the key points:
{text}

Concise Summary:
"""

combine_prompt = """
You are provided with multiple summaries from different sections of a document or article.
Your task is to create a comprehensive, well-structured final summary that:
1. Integrates all the important information from the individual summaries
2. Presents a coherent overview of the entire content
3. Organizes the information logically with appropriate headings and structure
4. Eliminates redundancy while preserving important details

Individual summaries:
{text}

Comprehensive Final Summary:
"""
