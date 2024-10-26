"""
Lab 2.

Text retrieval with BM25
"""
# pylint:disable=too-many-arguments, unused-argument
import math


def tokenize(text: str) -> list[str] | None:
    """
    Tokenize the input text into lowercase words without punctuation, digits and other symbols.

    Args:
        text (str): The input text to tokenize.

    Returns:
        list[str] | None: A list of words from the text.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(text, str):
        return None
    list_of_tokens = []
    for unit in text:
        if not unit.isalpha():
            text = text.replace(unit, ' ')
    for token in text.lower().split():
        if token.isalpha():
            list_of_tokens.append(token)
            continue
        corrected_token = ''
        for symbol in token:
            if symbol.isalpha():
                corrected_token += symbol
        if corrected_token.isalpha():
            list_of_tokens.append(corrected_token)
    return list_of_tokens


def remove_stopwords(tokens: list[str], stopwords: list[str]) -> list[str] | None:
    """
    Remove stopwords from the list of tokens.

    Args:
        tokens (list[str]): List of tokens.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[str] | None: Tokens after removing stopwords.

    In case of corrupt input arguments, None is returned.
    """
    if (not tokens or not stopwords
            or not isinstance(tokens, list) or not isinstance(stopwords, list)
            or not all(isinstance(token, str) for token in tokens)
            or not all(isinstance(word, str) for word in stopwords)):
        return None
    tokens_cleared = []
    for token in tokens:
        if token not in stopwords:
            tokens_cleared.append(token)
    if all(isinstance(tokens, str) for tokens in tokens_cleared) or tokens_cleared is not None:
        return tokens_cleared
    return None


def build_vocabulary(documents: list[list[str]]) -> list[str] | None:
    """
    Build a vocabulary from the documents.

    Args:
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        list[str] | None: List with unique words from the documents.

    In case of corrupt input arguments, None is returned.
    """
    if (not documents or not isinstance(documents, list)
            or not all(isinstance(d, list) for d in documents)
            or not all(isinstance(d, str) for document in documents for d in document)):
        return None
    unique_words = []
    for document in documents:
        unique_words += list(set(document))
    return unique_words


def calculate_tf(vocab: list[str], document_tokens: list[str]) -> dict[str, float] | None:
    """
    Calculate term frequency for the given tokens based on the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        document_tokens (list[str]): Tokenized document.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to their term frequency.

    In case of corrupt input arguments, None is returned.
    """
    if (not vocab or not document_tokens or not isinstance(vocab, list)
        or not all(isinstance(word, str) for word in vocab)
        or not isinstance(document_tokens, list)
        or not all(isinstance(token, str) for token in document_tokens)):
        return None
    term_frequency = {}
    for word in vocab:
        if word not in document_tokens:
            term_frequency[word] = 0.0
            continue
        term_frequency[word] = document_tokens.count(word) / len(document_tokens)
    for token in document_tokens:
        if token not in vocab:
            term_frequency[token] = document_tokens.count(token) / len(document_tokens)
    return term_frequency


def calculate_idf(vocab: list[str], documents: list[list[str]]) -> dict[str, float] | None:
    """
    Calculate inverse document frequency for each term in the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to its IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if (not vocab or not documents or not isinstance(vocab, list)
        or not all(isinstance(word, str) for word in vocab)
        or not isinstance(documents, list)
        or not all(isinstance(d, list) for d in documents)
        or not all(isinstance(d, str) for document in documents for d in document)):
        return None
    idf = {}
    for word in vocab:
        word_count = 0.0
        for document in documents:
            if word in document:
                word_count += 1
        idf[word] = math.log(((len(documents)) - word_count + 0.5) / (word_count + 0.5))
    for word in sum(documents, []):
        word_count = 0.0
        if word not in idf:
            for document in documents:
                if word in document:
                    word_count += 1
            idf[word] = math.log(((len(documents)) - word_count + 0.5) / (word_count + 0.5))
    return idf


def calculate_tf_idf(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float] | None:
    """
    Calculate TF-IDF scores for a document.

    Args:
        tf (dict[str, float]): Term frequencies for the document.
        idf (dict[str, float]): Inverse document frequencies.

    Returns:
        dict[str, float] | None: Mapping from terms to their TF-IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if (not tf or not idf or not isinstance(tf, dict) or not isinstance(idf, dict)
        or not any([True for word, value in tf.items() if isinstance(word, str)
                                                       and isinstance(value, float)])
        or not any([True for word, value in idf.items() if isinstance(word, str)
                                                        and isinstance(value, float)])):
        return None
    tf_idf = {}
    for word, value in tf.items():
        for same_word, its_value in idf.items():
            if word == same_word:
                tf_idf[word] = value * its_value
    for word, value in idf.items():
        if word not in tf_idf:
            for same_word, its_value in tf.items():
                if word == same_word:
                    tf_idf[word] = value * its_value
    return tf_idf


def calculate_bm25(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores.

    In case of corrupt input arguments, None is returned.
    """


def rank_documents(
    indexes: list[dict[str, float]], query: str, stopwords: list[str]
) -> list[tuple[int, float]] | None:
    """
    Rank documents for the given query.

    Args:
        indexes (list[dict[str, float]]): List of BM25 or TF-IDF indexes for the documents.
        query (str): The query string.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[tuple[int, float]] | None: Tuples of document index and its score in the ranking.

    In case of corrupt input arguments, None is returned.
    """


def calculate_bm25_with_cutoff(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    alpha: float,
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document with IDF cutoff.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        alpha (float): IDF cutoff threshold.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores with cutoff applied.

    In case of corrupt input arguments, None is returned.
    """


def save_index(index: list[dict[str, float]], file_path: str) -> None:
    """
    Save the index to a file.

    Args:
        index (list[dict[str, float]]): The index to save.
        file_path (str): The path to the file where the index will be saved.
    """


def load_index(file_path: str) -> list[dict[str, float]] | None:
    """
    Load the index from a file.

    Args:
        file_path (str): The path to the file from which to load the index.

    Returns:
        list[dict[str, float]] | None: The loaded index.

    In case of corrupt input arguments, None is returned.
    """


def calculate_spearman(rank: list[int], golden_rank: list[int]) -> float | None:
    """
    Calculate Spearman's rank correlation coefficient between two rankings.

    Args:
        rank (list[int]): Ranked list of document indices.
        golden_rank (list[int]): Golden ranked list of document indices.

    Returns:
        float | None: Spearman's rank correlation coefficient.

    In case of corrupt input arguments, None is returned.
    """
