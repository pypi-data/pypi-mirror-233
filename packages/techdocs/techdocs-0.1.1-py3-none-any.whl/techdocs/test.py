import argparse
import techdocs


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='subcommands')



def entrypoint():
    args = parser.parse_args()
    if args.subcommands is None:
        parser.print_help()
        return

    args.func(args)



@entrypoint
def main():
    print(f"Welcome to Techdocs {techdocs.__version__}")




if __name__ == "__main__":
    main()