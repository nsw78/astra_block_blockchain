import argparse
from analyzer.contract_analyzer import analyze_contract
from embeddings.indexer import build_index_from_texts

SAMPLE_DOCS = [
    "ERC20 token with owner-only mint and blacklist",
    "Liquidity pool pair contract example",
    "Contract that can renounce ownership",
]


def demo_analyze(address: str):
    print('Analyzing contract', address)
    res = analyze_contract(address)
    print('Result:')
    print(res)


def demo_rag(query: str):
    idx = build_index_from_texts(SAMPLE_DOCS)
    print('Query:', query)
    print('Top results:', idx.search(query))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--address', type=str, default=None)
    p.add_argument('--query', type=str, default=None)
    args = p.parse_args()
    if args.address:
        demo_analyze(args.address)
    if args.query:
        demo_rag(args.query)
    if not args.address and not args.query:
        print('Run with --address <0x..> or --query "text"')
