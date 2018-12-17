class Corpus:

    def __init__(self, corpus_id, title, contents, tags=None, tokenized_contents=None):
        self.id = corpus_id
        self.title = title
        self.contents = contents
        self.tags = tags if tags is not None else []
        self.tokenized_contents = tokenized_contents

    def to_dict(self):
        return {'title': self.title, 'tags': self.tags, 'contents': self.contents,
                'tokenized_contents': self.tokenized_contents, 'id': self.id}
