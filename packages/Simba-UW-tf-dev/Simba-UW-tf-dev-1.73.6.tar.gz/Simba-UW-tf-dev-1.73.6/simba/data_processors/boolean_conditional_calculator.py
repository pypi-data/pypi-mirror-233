import pandas as pd

from simba.mixins.config_reader import ConfigReader
from typing import Dict
import os
from simba.utils.checks import check_if_filepath_list_is_empty
from simba.utils.read_write import read_df, read_video_info, get_fn_ext, str_2_bool
from simba.utils.printing import stdout_success
from simba.utils.errors import MissingColumnsError, InvalidInputError
from copy import deepcopy


class BooleanConditionalCalculator(ConfigReader):

    def __init__(self,
                 config_path: str,
                 rules: Dict[str, bool]):

        ConfigReader.__init__(self, config_path=config_path)
        self.save_path = os.path.join(self.logs_path, f'Conditional_aggregate_statistics_{self.datetime}.csv')
        check_if_filepath_list_is_empty(filepaths=self.feature_file_paths, error_msg=f'No data found in {self.features_dir}')
        self.rules = rules
        self.output_df = pd.DataFrame(columns=['VIDEO'] + list(self.rules.keys()) + ['TIME (s)', 'FRAMES (count)'])


    def _check_integrity_of_rule_columns(self):
        for behavior in self.rules.keys():
            if behavior not in self.df.columns:
                raise MissingColumnsError(msg=f'File is missing the column {behavior} which is required for your conditional aggregate statistics {self.file_path}', source=self.__class__.__name__)
            other_col_vals = [x for x in list(set(self.df[behavior])) if x not in [0, 1]]
            if len(other_col_vals) > 0:
                raise InvalidInputError(msg=f'Invalid values found in column {behavior} of file {self.file_path}: SimBA expects only 0 and 1s.', source=self.__class__.__name__)

    def run(self):
        for file_cnt, file_path in enumerate(self.feature_file_paths):
            self.file_path = file_path
            _, self.video_name, _ = get_fn_ext(filepath=file_path)
            _, _, self.fps = read_video_info(vid_info_df=self.video_info_df, video_name=self.video_name)
            self.df = read_df(file_path=file_path, file_type=self.file_type)
            self._check_integrity_of_rule_columns()
            self.df = self.df[list(self.rules.keys())]

            self.sliced_df = deepcopy(self.df)
            values_str = []
            for k, v in self.rules.items():
                if str_2_bool(v):
                    self.sliced_df = self.sliced_df[self.sliced_df[k] == 1]
                else:
                    self.sliced_df = self.sliced_df[self.sliced_df[k] == 0]
                values_str.append(v)
            time_s = round(len(self.sliced_df) / self.fps, 4)
            self.output_df.loc[len(self.output_df)] = [self.video_name] + list(self.rules.values()) + [time_s] + [len(self.sliced_df)]


    def save(self):
        self.output_df.to_csv(self.save_path, index=False)
        self.timer.stop_timer()
        stdout_success(msg=f'Boolean conditional data saved at at {self.save_path}!', elapsed_time=self.timer.elapsed_time_str, source=self.__class__.__name__)

# rules = {'Rectangle_1 Simon in zone': 'TRUE', 'Polygon_1 JJ in zone': 'TRUE'}
# runner = BooleanConditionalCalculator(rules=rules, config_path='/Users/simon/Desktop/envs/troubleshooting/two_animals_16bp_032023/project_folder/project_config.ini')
# runner.run()
# runner.save()