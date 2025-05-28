class LRUPageReplacement:
    def __init__(self, capacity):
        self.capacity = capacity

    def run(self, reference_string, simulate_only=False):
        memory = []
        recent = {}
        page_faults = 0
        page_hits = 0
        log = []

        for i, page in enumerate(reference_string):
            if page in memory:
                page_hits += 1
                log.append(f"✅ Hit: {page} | Memory: {memory}")
            else:
                page_faults += 1
                if len(memory) < self.capacity:
                    memory.append(page)
                else:
                    # Only consider recently used pages that are still in memory
                    valid_recent = {p: recent[p] for p in memory if p in recent}
                    lru_page = min(valid_recent, key=valid_recent.get)
                    if lru_page in memory:
                        memory.remove(lru_page)
                    memory.append(page)
                log.append(f"❌ Miss: {page} | Memory: {memory}")
            
            recent[page] = i
            # Clean unused recent pages
            for p in list(recent):
                if p not in memory:
                    del recent[p]

        if simulate_only:
            return page_faults, page_hits
        else:
            return log, page_faults, page_hits