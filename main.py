import scoring
import morningstar_export
import argparse

def main(args):
    if args.arg1 == "export":
        morningstar_export.export(args.arg2)
    elif args.arg1 == "scoring":
        scoring.scoring(args.arg2)
    elif args.arg1 == "runall":
        morningstar_export.export(args.arg2)
        scoring.scoring(args.arg2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1")
    parser.add_argument("arg2")
    args = parser.parse_args()
    main(args)