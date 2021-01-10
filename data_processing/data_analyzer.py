from datetime import datetime
from typing import Dict, List

import pandas as pd


class DataAnalyzer:

    def analyze_data(self,
                     data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        data = self._calculate_indicators(data)
        data = self._calculate_grouped_data(data)
        return data

    def _calculate_grouped_data(self, data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        output = {
            'by_event': data,
            'by_year': self._group_data_by_columns(data, ['year']),
            'by_year_and_month': self._group_data_by_columns(data, ['year', 'month']),
        }
        return output

    @staticmethod
    def _calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
        data['cumulative_value'] = data['value'].cumsum()
        data['income'] = data['value']
        data['income'][data['income'] < 0] = 0
        data['outcome'] = data['value']
        data['outcome'][data['outcome'] > 0] = 0
        data['outcome'] = abs(data['outcome'])
        data['cumulative_income'] = data['income'].cumsum()
        data['cumulative_outcome'] = data['outcome'].cumsum()
        data['cumulative_ratio'] = data['cumulative_outcome'] / data['cumulative_income']
        return data

    def _group_data_by_columns(self, data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        grouped_data = pd.DataFrame()
        grouped_data['total'] = data.groupby(columns).sum()['value']
        grouped_data['income'] = data.groupby(columns).sum()['income']
        grouped_data['outcome'] = data.groupby(columns).sum()['outcome']
        grouped_data['ratio'] = grouped_data['outcome'] / grouped_data['income']
        grouped_data['total_cumulative'] = grouped_data['total'].cumsum()
        return grouped_data
