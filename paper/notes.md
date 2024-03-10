- Use the amr-unknown to filter of already-parsed results
- Mention lack of pragmatics as a hindrance to address the questions (implication)
- Anaphora resolution (AMRdoc)
- Sentence skimming
  - propbank frames do not include named entities
  - extract topical lemmas from question. Extact lemmas from sentences. Take sentences where the intersection of their lemmas with the question's (initially we wanted to do with propbank concept frames)
  - lemmatization does not account for inter-grammatical-class morphology (invent -> inventor / invention - Italy -> Italian), synonyms and anaphora on pronouns and multi-word expressions (maybe pair with NER?).


1. Introduction
  - Semantic representations have been overshadowed by LLMs in the last few years, but some problems of LLMs are naturally addressed by them...
  - In this work we implemented a simple tool for the retrieval of information from English Wikipedia through the use of Abstract Meaning Representations, and used it to explore what advantages and especially challenges such approach brings with it.
2. The Tool
  - Describe pipeline (a paragraph for each step: specify google search criticality) + figure of pipeline + figures of example queries 
3. Advantages
  - References, quote sentences without distortion, no hallucination or exaggerated expression of certainty.
4. Challenges and Solutions (see above) 
  - lack of pragmatics - integrate with formal pragmatics (cite some frameworks)
  - inter-sentence anaphora resolution - AMRdoc
  - speed - skimming (ideal vs our solution: see above)
5. Evaluation
  - Gold vs Smatch vs Skimming + Smatch
6. Conclusion
  - we showed how MRs can be useful for...
  - due to the challenges we faced, it is hard to tell whether meaning representations can take over LLMs for such applications. An interesting scenario to further explore would take into account hybrid systems where LLMs and MRs come together to accomplish such tasks taking the best of each technology. (cite some studies that do so)