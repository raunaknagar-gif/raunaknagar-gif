# Hindi AI Quality Evaluation — Personalization & Grounding

**Independent portfolio demonstration | Synthetic examples only | Not affiliated with Turing or Google.**

This reproducible project compares two Hindi-language personalized assistant responses using **Grounding**, **Integration** and **Helpfulness**. It demonstrates how to identify unsupported personalization, compare responses side by side (SxS) and write evidence-based rating rationales.

## Evaluation rubric
Each criterion is rated 1–5:
- **Grounding:** Does the response make claims supported by conversation evidence?
- **Integration:** Is relevant personal context applied naturally without forcing it?
- **Helpfulness:** Does the response meet the user's request and provide clear next steps?

Scores are **human-provided**. The Python CLI validates annotation fields and ranks responses based on submitted scores; it does not automatically assess model quality.

## Run
Python 3.10+ (standard library only):

```bash
python review.py examples/hindi_recipe.json
```

The demo contains fictional personal context, not real Google account information, and does not connect to Gemini, Gmail or employer systems.

**Status:** Runnable synthetic portfolio demonstration; not a deployed AI model or comprehensive professional QA platform.
