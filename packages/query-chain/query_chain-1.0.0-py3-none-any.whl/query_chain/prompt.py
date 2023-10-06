class PromptTemplate:
    def __init__(self, role=None, tone=None, style=None, length=None, audience=None):
        self.role = role
        self.tone = tone
        self.style = style
        self.length = length
        self.audience = audience

    def generate_prompt(self, text):
        prompt = ""

        if self.role is not None:
            prompt += f"**Role:** {self.role}\n"

        if self.tone is not None:
            prompt += f"**Tone:** {self.tone}\n"

        if self.style is not None:
            prompt += f"**Style:** {self.style}\n"

        if self.length is not None:
            prompt += f"**Length:** {self.length}\n"

        if self.audience is not None:
            prompt += f"**Audience:** {self.audience}\n"

        prompt += "\n"
        prompt += text

        return prompt


prompt_template_academic = PromptTemplate(
    role="Academic with great understanding of both Human-Computer Interaction and postcolonial theory",
    tone="Formal, academic, serious",
    style="Very detailed and specific. Drawing on as many concrete examples as possible to substantiate points",
    audience="Academic audience with vast experience and knowledge in the domain"
)

prompt_template_academic_podcaster = PromptTemplate(
    role="Scriptwriter for academic podcast on postcolonial theory in Human-Computer Interaction",
    tone="Formal, academic, generous, entertaining",
    style="Academic podcast with lots of specific references and examples, very detailed, precise and generous",
    length="5-7 minute script for podcast episode",
    audience="General academic audience, including academics from other fields"
)

prompt1 = prompt_template_academic.generate_prompt("""Summarize the publication and include:
    1. General Summary: 
    2. Key Points:
    3. Relevance for HCI:
    4. Relevance for Postcolonial Theory: 
    5. Main Strengths: 
    5. Main Shortcomings:
    6. Succinct concluding remarks.""")

prompt2 = prompt_template_academic.generate_prompt("""I would like a second pass at that review:
    1. Elaborate on the more vague and abstract points
    2. Add specific and concrete examples when possible
    3. Double check statements for accuracy""")

prompt3 = prompt_template_academic_podcaster.generate_prompt("""Generate script for this specific episode. Keep in mind:
    1. Script is to be read by one person only, no dialogue.
    2. When making a point, draw in as many concrete examples, authors and concepts as possible.
    3. Intro: short, announces paper/authors concisely. Ends with articulate and short introduction to the publication.
    4. Outro: standard podcast outro: short, simple, fun, hopeful, sincere, asking to subscribe.""")

prompt4 = prompt_template_academic_podcaster.generate_prompt("""Generate script for this specific episode. Keep in mind:
    1. Script is to be read by one person only, no dialogue.
    2. When making a point, draw in as many concrete examples, authors and concepts as possible.
    3. Intro: short, announces paper/authors concisely. Ends with articulate and short introduction to the publication.
    4. Outro: standard podcast outro: short, simple, fun, hopeful, sincere, asking to subscribe.
    5. While remaining balanced, and without being unfair, Be quite critical of this publication.""")

prompt5 = prompt_template_academic_podcaster.generate_prompt("""Generate script for this specific episode. Keep in mind:
    1. Script is to be read by one person only, no dialogue.
    2. When making a point, draw in as many concrete examples, authors and concepts as possible.
    3. Intro: short, announces paper/authors concisely. Ends with articulate and short introduction to the publication.
    4. Outro: standard podcast outro: short, simple, fun, hopeful, sincere, asking to subscribe.
    5. While remaining balanced, and without being sycophantic , Be rather sympathetic of this publication.""")
