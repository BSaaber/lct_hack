from sqlalchemy import create_engine
from app.database import db_models  # noqa - for db initialization
from app.database import schemas as db_schemas
from sklearn.metrics.pairwise import cosine_similarity
from heapq import heappush, heappop
from collections import defaultdict
from app.scripts.TextAnalyzer import BertBasedAnalyzer, BertBasedTokenizer
import numpy as np
import app.database.api as db_api
import os
from dotenv import load_dotenv
import psycopg2  # noqa - driver for db
from sqlalchemy.orm import sessionmaker
import asyncio


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

engine = create_engine(os.environ["DATABASE_URL"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
bert_tokenizer = BertBasedTokenizer()
bert_analyzer = BertBasedAnalyzer()


def get_document_info_from_raw(raw_data, type='tsn'):
    data_ids = [doc.id for doc in raw_data]
    tokenized_data = bert_tokenizer.get_tokens([doc.text if type == 'tsn' else doc.name for doc in raw_data])
    data_embeddings = bert_analyzer.get_sentence_embeddings(tokenized_data)
    return zip(data_ids, data_embeddings)

# pipenv run python -m app.scripts.make_tsn_mapping


async def make_tsn_mapping():
    print("make_hypothesises started to work")
    with SessionLocal() as db:
        raw_spgz = np.array_split([spgz for spgz in (await db_api.sprav_edit.get_all_spgz(db))], 1000)
        raw_tsn = np.array_split([tsn for tsn in (await db_api.sprav_edit.get_all_tsn(db))], 1000)
        print(len(raw_spgz))
        print(len(raw_tsn))
        spgz_info = []
        tsn_info = []
        for i, c in enumerate(raw_spgz):
            print((i / 10), '%')
            spgz_info.extend(get_document_info_from_raw(c, 'spgz'))
        for i, c in enumerate(raw_tsn):
            print(i / 10, "%")
            spgz_info.extend(get_document_info_from_raw(c, 'tsn'))

        for tsn_id, tsn_embedding in tsn_info:
            best_spgz = 0
            best_score = 0

            for spgz_id, spgz_embedding in spgz_info:
                score = cosine_similarity(tsn_embedding.reshape(1, -1), spgz_embedding.reshape(1, -1))
                if score > best_score:
                    best_score = score
                    best_spgz = spgz_id
            print("score:", best_score)
            print("tsn:", tsn_id)
            print("spgz:", best_spgz)

        # for curr_tsn in (await db_api.sprav_edit.get_all_tsn(db)):
        #     p_queue = []
        #     heappush(p_queue, 1)
        #     metric = 0
        #     tsn_info = set(curr_tsn.tsn_mapping_info.split(','))
        #     print(curr_tsn.text)
        #     best_spgz = {}
        #     for curr_spgz in all_spgz:
        #         spgz_info = set(curr_spgz.mapping_info.split(','))
        #         new_metric = jaccard_metric_between_tsn_and_spgz(tsn_info, spgz_info)
        #         if new_metric > metric:
        #             metric = new_metric
        #             best_spgz = curr_spgz.name
        #     print(best_spgz)
        #     print(metric)


loop = asyncio.get_event_loop()
loop.run_until_complete(make_tsn_mapping())
loop.close()
