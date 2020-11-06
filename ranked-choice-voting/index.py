import sys
from generate_ballots import ballots_main
from intermediate_master import create_intermediate_master_file
from final_master_feature_extraction import feature_extraction_main


def create_dataset_for_modeling(num_ballots_to_generate):
    ballots_main(num_ballots_to_generate)
    create_intermediate_master_file()
    feature_extraction_main()


if __name__ == "__main__":
    num_ballots_to_generate = int(sys.argv[1])
    create_dataset_for_modeling(num_ballots_to_generate)