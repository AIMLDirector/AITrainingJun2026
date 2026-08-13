from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

# 1. Define a regex pattern for passwords following labels
# This looks for terms like "password" followed by spaces, symbols, and then the actual password
password_pattern = Pattern(
    name="password_pattern",
    regex=r"(?i)\b(password|pwd|pass|secret)\b\s*[:\s=\-]\s*([^\s,;]+)",
    score=0.85
)

# 2. Create the custom recognizer
password_recognizer = PatternRecognizer(
    supported_entity="PASSWORD", 
    patterns=[password_pattern]
)

# 3. Initialize engines and add your new custom rule
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(password_recognizer)
anonymizer = AnonymizerEngine()

# 4. Test text containing credit cards and passwords
sample_text = "User admin logged in with password: MySecret123! and Visa 4111 1111 1111 1111"

# 5. Analyze and Anonymize
results = analyzer.analyze(text=sample_text, language="en")
final_output = anonymizer.anonymize(text=sample_text, analyzer_results=results)

print(final_output.text)