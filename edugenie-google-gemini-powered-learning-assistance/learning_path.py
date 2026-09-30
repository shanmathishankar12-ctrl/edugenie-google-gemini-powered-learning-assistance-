"""
Learning Path Module for EduGenie
Generates structured, step-by-step learning roadmaps with difficulty levels,
a 4-week study schedule, project suggestions, and curated resource recommendations.
"""

from gemini_client import ask_gemini


def get_learning_recommendations(text: str) -> str:
    """
    Generates a personalized, comprehensive learning roadmap for a student.
    """
    cleaned_input = text.strip()
    if not cleaned_input:
        return "Please enter a skill, subject, or topic to generate a learning path."

    prompt = f"""You are EduGenie, an expert AI learning coach and academic mentor.

Create a complete, highly structured learning roadmap for:
{cleaned_input}

Use this exact layout and headers:

LEARNING GOAL
- Clear statement of what the student will achieve and be able to do.

LEVEL 1 - BEGINNER
- Topic 1: Description
- Topic 2: Description
- Topic 3: Description

LEVEL 2 - INTERMEDIATE
- Topic 1: Description
- Topic 2: Description
- Topic 3: Description

LEVEL 3 - ADVANCED
- Topic 1: Description
- Topic 2: Description
- Topic 3: Description

4 WEEK PLAN
- Week 1: Core concepts and foundational practice
- Week 2: Intermediate topics and guided exercises
- Week 3: Advanced techniques and troubleshooting
- Week 4: Capstone project building and portfolio polish

PRACTICE PROJECT
- An engaging, portfolio-worthy project students can build using their knowledge.

REVISION TIPS
- Practical active recall and spaced repetition tips for mastering this subject.

RESOURCE TYPES
- Books, official documentation, interactive sites, and video tutorial recommendations.

Make the roadmap practical, inspiring, and easy for any student to follow.
"""
    return ask_gemini(prompt)


# Alias for compatibility with single-file and legacy scripts
learning_path = get_learning_recommendations
