class OptimalPageReplacement:
    def __init__(self, capacity):
        self.capacity = capacity

    def run(self, reference_string, simulate_only=False):
        memory = []
        page_faults = 0
        page_hits = 0
        log = []

        for i in range(len(reference_string)):
            page = reference_string[i]
            if page in memory:
                page_hits += 1
                log.append(f"✅ Hit: {page} | Memory: {memory}")
            else:
                page_faults += 1
                if len(memory) < self.capacity:
                    memory.append(page)
                else:
                    future = reference_string[i+1:]
                    index_map = {}
                    for mem_page in memory:
                        if mem_page in future:
                            index_map[mem_page] = future.index(mem_page)
                        else:
                            index_map[mem_page] = float('inf')
                    if index_map:
                        farthest = max(index_map, key=index_map.get)
                        if farthest in memory:
                            memory.remove(farthest)
                    memory.append(page)
                log.append(f"❌ Miss: {page} | Memory: {memory}")

        if simulate_only:
            return page_faults, page_hits
        else:
            return log, page_faults, page_hits