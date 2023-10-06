import argparse
import json
import os
import shutil

from stanza.utils.datasets.ner.simplify_ontonotes_to_worldwide import simplify_ontonotes_to_worldwide

def convert_ontonotes_file(filename, simplify, bigger_first):
    assert "en_ontonotes" in filename
    if not os.path.exists(filename):
        raise FileNotFoundError("Cannot convert missing file %s" % filename)
    new_filename = filename.replace("en_ontonotes", "en_ontonotes-multi")

    with open(filename) as fin:
        doc = json.load(fin)

    for sentence in doc:
        for word in sentence:
            ner = word['ner']
            if simplify:
                simplified = simplify_ontonotes_to_worldwide(ner)
            else:
                simplified = "-"
            if bigger_first:
                word['multi_ner'] = (ner, simplified)
            else:
                word['multi_ner'] = (simplified, ner)

    with open(new_filename, "w") as fout:
        json.dump(doc, fout, indent=2)

def convert_worldwide_file(filename, bigger_first):
    assert "en_worldwide-8class" in filename
    if not os.path.exists(filename):
        raise FileNotFoundError("Cannot convert missing file %s" % filename)

    new_filename = filename.replace("en_worldwide-8class", "en_worldwide-8class-multi")

    with open(filename) as fin:
        doc = json.load(fin)

    for sentence in doc:
        for word in sentence:
            ner = word['ner']
            if bigger_first:
                word['multi_ner'] = ("-", ner)
            else:
                word['multi_ner'] = (ner, "-")

    with open(new_filename, "w") as fout:
        json.dump(doc, fout, indent=2)

def combine_files(output_filename, *input_filenames):
    doc = []

    for filename in input_filenames:
        with open(filename) as fin:
            new_doc = json.load(fin)
            doc.extend(new_doc)

    with open(output_filename, "w") as fout:
        json.dump(doc, fout, indent=2)

def build_multitag_dataset(simplify, bigger_first):
    convert_ontonotes_file("data/ner/en_ontonotes.train.json", simplify, bigger_first)
    convert_ontonotes_file("data/ner/en_ontonotes.dev.json", simplify, bigger_first)
    convert_ontonotes_file("data/ner/en_ontonotes.test.json", simplify, bigger_first)

    convert_worldwide_file("data/ner/en_worldwide-8class.train.json", bigger_first)
    convert_worldwide_file("data/ner/en_worldwide-8class.dev.json", bigger_first)
    convert_worldwide_file("data/ner/en_worldwide-8class.test.json", bigger_first)

    combine_files("data/ner/en_ontonotes-ww-multi.train.json",
                  "data/ner/en_ontonotes-multi.train.json",
                  "data/ner/en_worldwide-8class-multi.train.json")
    shutil.copyfile("data/ner/en_ontonotes-multi.dev.json",
                    "data/ner/en_ontonotes-ww-multi.dev.json")
    shutil.copyfile("data/ner/en_ontonotes-multi.test.json",
                    "data/ner/en_ontonotes-ww-multi.test.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no_simplify', dest='simplify', action='store_false', help='By default, this script will simplify the OntoNotes 18 classes to the 8 WorldWide classes in a second column.  Turning that off will leave that column blank.  Initial experiments with that setting were very bad, though')
    parser.add_argument('--no_bigger_first', dest='bigger_first', action='store_false', help='By default, this script will put the 18 class tags in the first column and the 8 in the second.  This flips the order')
    args = parser.parse_args()

    build_multitag_dataset(args.simplify, args.bigger_first)

if __name__ == '__main__':
    main()

