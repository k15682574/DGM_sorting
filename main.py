import scoring_BOS
import scoring_DGM
import morningstar_export
import argparse

def main(args):
    if args.arg1 == "export":
        morningstar_export.export(args.arg2)

    if args.arg1 == "BOS":
        scoring_BOS.scoring(args.arg2)

    if args.arg1 == "DGM":
        scoring_DGM.scoring(args.arg2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1")
    parser.add_argument("arg2")
    args = parser.parse_args()
    main(args)