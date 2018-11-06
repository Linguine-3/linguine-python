import json
import random

import linguistica as lxa

from linguine.ops.remove_punct import RemovePunct


class UnsupervisedMorphology:
    def run(self, data):
        results = []

        data = RemovePunct().run(data)

        for corpus in data:
            lxa_object = lxa.from_corpus(corpus.contents)
            sigs_to_stems = lxa_object.signatures_to_stems()
            results.append(self.output_to_results(sigs_to_stems))

        return json.dumps(results)

    def output_to_results(self, sigs_to_stems):
        results = []
        for sig, stems in sorted(sigs_to_stems.items(), key=lambda x: len(x[1]), reverse=True):
            results.append({"affixes": list(sig), "roots": sorted(random.sample(stems, min(15, len(stems))))})
        return results
