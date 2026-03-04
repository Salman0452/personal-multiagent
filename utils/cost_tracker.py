import time

class CostTracker:
    # Groq llama3-70b pricing (per 1M tokens)
    COST_PER_1K_INPUT_TOKENS  = 0.00059   # $0.59 per 1M
    COST_PER_1K_OUTPUT_TOKENS = 0.00079   # $0.79 per 1M

    def __init__(self):
        self.reset()

    def reset(self):
        self.llm_calls      = 0
        self.total_tokens   = 0
        self.start_time     = None
        self.end_time       = None

    def start(self):
        self.reset()
        self.start_time = time.time()
    
    def stop(self):
        self.end_time = time.time()
    
    def add_call(self, tokens: int = 500):
        """Estimate per call — Groq doesn't return token count easily"""
        self.llm_calls += 1
        self.total_tokens += tokens
    
    def get_summary(self) -> dict:
        elapsed = (
            round(self.end_time - self.start_time, 2)
            if self.end_time else 0
        )
        estimated_cost = (
            self.total_tokens / 1000
        ) * self.COST_PER_1K_INPUT_TOKENS

        return {
            "llm_calls"      : self.llm_calls,
            "total_tokens"   : self.total_tokens,
            "estimated_cost" : round(estimated_cost, 6),
            "elapsed_seconds": elapsed
        }