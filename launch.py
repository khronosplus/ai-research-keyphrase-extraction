from preprocessing.postagging import PosTaggingStanford
from model.input_representation import InputTextObj
from model.method import MMRPhrase
from configparser import ConfigParser
from embeddings.emb_distrib_local import EmbeddingDistributorLocal
import argparse


def extract_keyphrases(embedding_distrib, ptagger, raw_text, N, lang):
    """
    Method that extract a set of keyphrases

    :param embedding_distrib: An Embedding Distributor object see @EmbeddingDistributor
    :param ptagger: A Pos Tagger object see @PosTagger
    :param raw_text: A string containing the raw text to extract
    :param N: The number of keyphrases to extract
    :param lang: The language
    :return: the list of N keyphrases (or less if there is not enough candidates)
    """
    tagged = ptagger.pos_tag_raw_text(raw_text)
    text_obj = InputTextObj(tagged, lang)
    return MMRPhrase(embedding_distrib, text_obj, N=N)


def load_local_embedding_distributor(lang):
    if lang == 'en':
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        sent2vec_bin = config_parser.get('SENT2VEC', 'bin_path')
        sent2vec_model = config_parser.get('SENT2VEC', 'model_path')
        return EmbeddingDistributorLocal(sent2vec_bin, sent2vec_model)


def load_local_pos_tagger(lang):
    if lang == 'en':
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        jar_path = config_parser.get('STANFORDTAGGER', 'jar_path')
        model_directory_path = config_parser.get('STANFORDTAGGER', 'model_directory_path')
        return PosTaggingStanford(jar_path, model_directory_path, lang=lang)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract keyphrases from raw text')
    parser.add_argument('raw_text', help='raw text to process')
    parser.add_argument('-N', help='number of keyphrases to extract', required=True)
    args = parser.parse_args()
    embedding_distributor = load_local_embedding_distributor('en')
    pos_tagger = load_local_pos_tagger('en')
    print(extract_keyphrases(embedding_distributor, pos_tagger, args.raw_text, args.N, 'en'))