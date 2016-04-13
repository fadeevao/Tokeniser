# Tokeniser

This project is an attempt to implement a simple tokeniser in Python as a natural language pre-processing step.  

I am aware that there are libraries that can do it for me, but I wanted to give it a try and implement one myself.  

Cases that this tokeniser deals with:
  - possessive pronouns (both plural and singular, we indicate possessive pronoun by appending "(p)" to it (eg John(p))
  - negations (like "doesn't", "can't")
  - apostrophes (like in the "O'Neill" case - it separates 2 parts)
  - distinguishes double numbers and does not separate them (eg 5.5 remains as 5.5 and doesn't get separated into 3 tokens: 5, ., 5)
