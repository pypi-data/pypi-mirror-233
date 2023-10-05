import pandas as pd
from api.mapper.algo_functions import ( ai4_merge, ai_merge, fuzzy_merge,
                                rapid_fuzzy_merge, stringmetric_merge, stringmetric_with_chatgpt_merge,
                                stringmetric_with_gpt4_merge, fuzzywuzzy_with_gpt4_merge,
                                recursive_algo
                                )
from api.mapper.algos.harmonization_with_suggestion_service import SampleBasedHarmonizationService


class DataHarmonizer:
    def __init__(self, key, file1_path, file2_path, option):
        self.key = key
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.option = option

    def merge_files(self):
        df1 = pd.read_csv(self.file1_path)
        df2 = pd.read_csv(self.file2_path)

        merge_options = {
            'ChatGPT': ai_merge,
            'GPT4': ai4_merge,
            'Fuzzy Wuzzy': fuzzy_merge,
            'Rapidfuzz': rapid_fuzzy_merge,
            'Jaro Winkler': stringmetric_merge,
            'JW Layered with ChatGPT': stringmetric_with_chatgpt_merge,
            'JW Layered with GPT4': stringmetric_with_gpt4_merge,
            'FW Layered with GPT4': fuzzywuzzy_with_gpt4_merge,
            'Recursive Data Harmonization': recursive_algo
        }

        merge_func = merge_options.get(self.option)
        if merge_func:
            merged_text = merge_func(self.key, df1, df2)
            return merged_text
        else:
            raise ValueError('Invalid merge option')


class DataHarmonizationWithSuggestion:
    def __init__(self, key, sample_file_path, file1_path, file2_path):
        self.key = key
        self.sample_file_path = sample_file_path
        self.file1_path = file1_path
        self.file2_path = file2_path

    def harmonize_data(self):
        # Read the sample harmonized data from the sample file
        sample_data = pd.read_csv(self.sample_file_path)

        # Read the two files that need to be harmonized
        data1 = pd.read_csv(self.file1_path)
        data2 = pd.read_csv(self.file2_path)
        print(data1.head())
        print(data2.head())
        # Invoke the SampleBasedHarmonizationService to harmonize the data
        harmonized_data = SampleBasedHarmonizationService(self.key).invoke(sample_data, data1, data2)

        return harmonized_data