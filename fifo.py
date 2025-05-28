class FIFOPageReplacement:
    def __init__(self, capacity):
        self.capacity = capacity

    def run(self, reference_string, simulate_only=False):
        memory = []
        page_faults = 0
        page_hits = 0
        log = []

        for page in reference_string:
            if page in memory:
                page_hits += 1
                log.append(f"✅ Hit: {page} | Memory: {memory}")
            else:
                page_faults += 1
                if len(memory) < self.capacity:
                    memory.append(page)
                else:
                    memory.pop(0)
                    memory.append(page)
                log.append(f"❌ Miss: {page} | Memory: {memory}")
        
        if simulate_only:
            return page_faults, page_hits
        else:
            return log, page_faults, page_hits
