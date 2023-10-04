import os
import json
from linguist.sha256 import SHA256 as sha256
from linguist.classifier import Classifier
from linguist.shebang import Shebang


class Samples:
    # Path to samples root directory
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))

    # Path for serialized samples db
    PATH = os.path.abspath(os.path.join(ROOT, 'samples.json'))

    @staticmethod
    def cache():
        if not hasattr(Samples, "_cache"):
            Samples._cache = Samples.load_samples()
        return Samples._cache

    @staticmethod
    def load_samples():
        try:
            import yajl as serializer
        except ImportError:
            import json as serializer

        print("Loading samples from %s" % Samples.PATH)

        if os.path.getsize(Samples.PATH) <= 2:
            sample_data = Samples.data()
            json_str = json.dumps(sample_data, ensure_ascii=False)

            with open(Samples.PATH, 'w', encoding='utf-8') as file:
                file.write(json_str)
        print("Loading samples from %s" % Samples.PATH)
        with open(Samples.PATH, 'r', encoding='utf-8') as file:
            return serializer.load(file)

    @staticmethod
    def each(callback):
        for category in sorted(os.listdir(Samples.ROOT)):
            if category in ['.', '..', 'samples.json']:
                print("Skipping %s" % category)
                continue

            dirname = os.path.join(Samples.ROOT, category)
            for filename in os.listdir(dirname):
                if filename in ['.', '..', 'samples.json']:
                    continue

                if filename == 'filenames':
                    subdirname = os.path.join(dirname, filename)
                    for subfilename in os.listdir(subdirname):
                        if subfilename in ['.', '..']:
                            continue

                        callback({
                            'path': os.path.join(subdirname, subfilename),
                            'language': category,
                            'filename': subfilename
                        })
                else:
                    path = os.path.join(dirname, filename)
                    extname = os.path.splitext(filename)[1]

                    try:
                        with open(path, 'r') as file:
                            data = file.read()
                    except UnicodeDecodeError:
                        print("UnicodeDecodeError: %s" % path)
                        continue
                    callback({
                        'path': path,
                        'language': category,
                        'interpreter': Shebang.interpreter(data),
                        'extname': extname if extname else None
                    })

    @staticmethod
    def data():
        db = {}
        db['extnames'] = {}
        db['interpreters'] = {}
        db['filenames'] = {}

        def callback(sample):
            language_name = sample['language']

            if sample.get('extname'):
                db['extnames'].setdefault(language_name, [])
                if sample['extname'] not in db['extnames'][language_name]:
                    db['extnames'][language_name].append(sample['extname'])
                    db['extnames'][language_name].sort()

            if sample.get('interpreter'):
                db['interpreters'].setdefault(language_name, [])
                if sample['interpreter'] not in db['interpreters'][language_name]:
                    db['interpreters'][language_name].append(sample['interpreter'])
                    db['interpreters'][language_name].sort()

            if sample.get('filename'):
                db['filenames'].setdefault(language_name, [])
                db['filenames'][language_name].append(sample['filename'])
                db['filenames'][language_name].sort()
            with open(sample['path'], 'r', encoding='utf-8') as file:
                data = file.read()

            Classifier.train(db, language_name, data)

        Samples.each(callback)
        db['sha256'] = sha256.hexdigest(db)

        return db
