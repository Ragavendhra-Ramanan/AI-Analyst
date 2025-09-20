MULTIMODAL_EXTRACTION_PROMPT = """
You will be provided with an image of a PDF page or a slide. Your task is to create a detailed, engaging, and beginner-friendly explanation of the content, formatted in Markdown with a clear hierarchy of title, subtitles, and descriptions. The output should be suitable for a 101-level audience who cannot see the image.

Instructions:

1. Title
   - If there is a clear title, use it as the main heading in Markdown (# {{TITLE}}).
   - If no title is present, skip the main heading and start directly with subtitles.

2. Subtitles and Descriptions
   - Organize the content into 2-4 subtitles (## {{Subtitle}}) that group related ideas.
   - Under each subtitle, write a concise but thorough description of the content.
   - Explain all visual elements in simple language:
     - Diagrams: Describe each component and how they interact. Example: “The process begins with X, which leads to Y and results in Z.”
     - Tables: Present information logically in sentences. Example: “Product A costs X dollars, while Product B costs Y dollars.”
     - Charts/Graphs: Explain axes, trends, and insights.
     - Text or Concepts: Summarize key points and define technical terms simply.

3. Style Guidelines
   - Focus on the content, not the format.
   - Do NOT mention the type of material (slide, page) or the physical layout (e.g., top-left corner).
   - Include all important details while remaining concise.
   - Add interpretations and insights where relevant to help the audience understand the significance.

Required Output Format (Markdown):

If a title exists:
# {{TITLE}}

## {{Subtitle 1}}
{{Description 1}}

## {{Subtitle 2}}
{{Description 2}}

## {{Subtitle 3}}
{{Description 3}}

If there is no title:
## {{Subtitle 1}}
{{Description 1}}

## {{Subtitle 2}}
{{Description 2}}

## {{Subtitle 3}}
{{Description 3}}

Example Output:

# Digital Transformation Roadmap

## Vision and Goals
The plan starts by defining a clear vision to improve customer experience, streamline operations, and foster innovation.

## Key Enablers
Three main enablers support the transformation: upgrading infrastructure, adopting cloud platforms, and ensuring data security.

## Phased Approach
The transformation occurs in three stages: modernizing current systems, integrating new digital tools, and implementing long-term innovation through analytics and AI.
"""
